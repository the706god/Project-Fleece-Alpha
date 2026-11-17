import os
import sys
import json
import logging
from typing import Generator, List, Dict, Any, Optional

# Load bundled portable TurboQuant native dylibs and C-struct ABI alignment
from engine.turboquant_loader import configure_turboquant_runtime
TURBOQUANT_LIB_DIR = configure_turboquant_runtime()

KV_CACHE_TYPE_MAP = {
    "f16": 1,
    "q8_0": 8,
    "turbo2": 43,  # GGML_TYPE_TURBO2_0
    "turbo3": 44,  # GGML_TYPE_TURBO3_0
    "turbo4": 47,  # GGML_TYPE_TURBO4_0 (Optimal default on M1 Pro)
    "turbo5": 51,  # GGML_TYPE_TURBO5_0
    "turbo6": 52,  # GGML_TYPE_TURBO6_0
}

logging.basicConfig(level=logging.INFO, format="[Fleece-Alpha] %(levelname)s: %(message)s")
logger = logging.getLogger("FleeceEngine")

class FleeceEngine:
    """
    Core execution engine for Project: Fleece Alpha.
    Wraps llama.cpp GGUF inference with native TurboQuant KV caching (turbo4/turbo4)
    and automated device offloading (Apple Silicon Metal / CUDA / CPU).
    """

    def __init__(self, config_path: str = "fleece_config.json"):
        self.base_dir = os.path.dirname(os.path.abspath(config_path))
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        raw_model_path = self.config.get("model_path", "models/model.gguf")
        self.model_path = os.path.normpath(os.path.join(self.base_dir, raw_model_path))
        
        # Handle broken symlink or missing model file via automated download
        is_broken_link = os.path.islink(self.model_path) and not os.path.exists(self.model_path)
        is_missing_or_empty = not os.path.exists(self.model_path) or os.path.getsize(self.model_path) < 1_000_000

        if is_broken_link or is_missing_or_empty:
            logger.info("Model file not found locally. Initiating automated first-run setup...")
            sys.path.insert(0, self.base_dir)
            from setup_models import download_model
            self.model_path = download_model()

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at: {self.model_path}")

        engine_cfg = self.config.get("engine", {})
        self.n_ctx = engine_cfg.get("n_ctx", 65536)
        self.n_threads = engine_cfg.get("n_threads", os.cpu_count() or 4)
        self.n_gpu_layers = engine_cfg.get("n_gpu_layers", -1)
        self.default_temp = engine_cfg.get("temperature", 0.2)
        self.default_top_p = engine_cfg.get("top_p", 0.95)
        self.flash_attn = engine_cfg.get("flash_attn", True)
        self.kv_cache_type_k = engine_cfg.get("kv_cache_type_k", "turbo4")
        self.kv_cache_type_v = engine_cfg.get("kv_cache_type_v", "turbo4")
        self.kv_fallback_type = engine_cfg.get("kv_fallback_type", "q8_0")
        self.turbo_sparse_v = engine_cfg.get("turbo_sparse_v", True)
        self.turbo_auto_asymmetric = engine_cfg.get("turbo_auto_asymmetric", True)

        self.llm = None
        self._init_backend()

    def _init_backend(self):
        # Configure TurboQuant environment guards before loading backend
        if self.turbo_sparse_v:
            os.environ.setdefault("TURBO_SPARSE_V", "1")
        if self.turbo_auto_asymmetric:
            os.environ.setdefault("TURBO_AUTO_ASYMMETRIC", "1")
        if self.kv_cache_type_v == "turbo2":
            os.environ.setdefault("TURBO_LAYER_ADAPTIVE", "7")

        k_code = KV_CACHE_TYPE_MAP.get(self.kv_cache_type_k.lower(), 47)
        v_code = KV_CACHE_TYPE_MAP.get(self.kv_cache_type_v.lower(), 47)

        try:
            from llama_cpp import Llama
            logger.info(
                "Initializing llama_cpp backend with GGUF: %s (n_ctx=%d, flash_attn=%s, type_k=%s, type_v=%s)",
                self.model_path, self.n_ctx, self.flash_attn, self.kv_cache_type_k, self.kv_cache_type_v
            )
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=self.n_ctx,
                n_threads=self.n_threads,
                n_gpu_layers=self.n_gpu_layers,
                type_k=k_code,
                type_v=v_code,
                flash_attn=self.flash_attn,
                verbose=False
            )
            logger.info("Model loaded successfully into memory. Context capacity: %d tokens", self.n_ctx)
        except Exception as e:
            fallback_k = KV_CACHE_TYPE_MAP.get(self.kv_fallback_type.lower(), 8)
            fallback_v = KV_CACHE_TYPE_MAP.get(self.kv_fallback_type.lower(), 8)
            logger.warning(
                "TurboQuant KV cache initialization error: %s. Falling back to %s/%s KV cache...",
                e, self.kv_fallback_type, self.kv_fallback_type
            )
            try:
                from llama_cpp import Llama
                self.llm = Llama(
                    model_path=self.model_path,
                    n_ctx=self.n_ctx,
                    n_threads=self.n_threads,
                    n_gpu_layers=self.n_gpu_layers,
                    type_k=fallback_k,
                    type_v=fallback_v,
                    flash_attn=self.flash_attn,
                    verbose=False
                )
                logger.info("Fallback model loaded successfully. Context capacity: %d tokens", self.n_ctx)
            except Exception as e2:
                logger.error("Failed to initialize llama_cpp engine: %s", e2)
                logger.warning("Ensure llama-cpp-python is installed with matching system architecture.")
                raise

    def count_tokens(self, text: str) -> int:
        """Accurately count tokens using the model's native tokenizer."""
        if not self.llm:
            return len(text.split()) * 4 // 3
        tokens = self.llm.tokenize(text.encode("utf-8"))
        return len(tokens)

    def generate(
        self,
        prompt: str,
        max_tokens: int = 2048,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        stop: Optional[List[str]] = None,
        stream: bool = False
    ) -> Any:
        """Run inference on a pre-budgeted prompt."""
        if not self.llm:
            raise RuntimeError("Engine not initialized.")

        temp = temperature if temperature is not None else self.default_temp
        tp = top_p if top_p is not None else self.default_top_p
        stop_tokens = stop or ["<|im_end|>", "<|endoftext|>"]

        if stream:
            return self._stream_response(prompt, max_tokens, temp, tp, stop_tokens)
        
        response = self.llm(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temp,
            top_p=tp,
            stop=stop_tokens
        )
        return response["choices"][0]["text"]

    def _stream_response(self, prompt, max_tokens, temp, tp, stop_tokens) -> Generator[str, None, None]:
        stream = self.llm(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temp,
            top_p=tp,
            stop=stop_tokens,
            stream=True
        )
        for chunk in stream:
            delta = chunk["choices"][0]["text"]
            if delta:
                yield delta

    def chat_format(self, messages: List[Dict[str, str]]) -> str:
        """Apply ChatML format native to Qwen 3.5."""
        formatted = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            formatted += f"<|im_start|>{role}\n{content}<|im_end|>\n"
        formatted += "<|im_start|>assistant\n"
        return formatted
