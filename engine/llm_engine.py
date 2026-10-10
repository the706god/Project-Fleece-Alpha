import os
import sys
import json
import logging
from typing import Generator, List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="[Fleece-Alpha] %(levelname)s: %(message)s")
logger = logging.getLogger("FleeceEngine")

class FleeceEngine:
    """
    Core execution engine for Project: Fleece Alpha.
    Wraps llama.cpp GGUF inference with automated device detection (Metal/CUDA/CPU).
    """

    def __init__(self, config_path: str = "fleece_config.json"):
        self.base_dir = os.path.dirname(os.path.abspath(config_path))
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        raw_model_path = self.config.get("model_path", "models/model.gguf")
        self.model_path = os.path.normpath(os.path.join(self.base_dir, raw_model_path))
        
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at: {self.model_path}")

        engine_cfg = self.config.get("engine", {})
        self.n_ctx = engine_cfg.get("n_ctx", 16384)
        self.n_threads = engine_cfg.get("n_threads", os.cpu_count() or 4)
        self.n_gpu_layers = engine_cfg.get("n_gpu_layers", -1)
        self.default_temp = engine_cfg.get("temperature", 0.2)
        self.default_top_p = engine_cfg.get("top_p", 0.95)

        self.llm = None
        self._init_backend()

    def _init_backend(self):
        try:
            from llama_cpp import Llama
            logger.info("Initializing llama_cpp backend with GGUF: %s", self.model_path)
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=self.n_ctx,
                n_threads=self.n_threads,
                n_gpu_layers=self.n_gpu_layers,
                verbose=False
            )
            logger.info("Model loaded successfully into memory. Context capacity: %d tokens", self.n_ctx)
        except Exception as e:
            logger.error("Failed to initialize llama_cpp engine: %s", e)
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
        """Apply ChatML format native to Qwen 2.5 Coder."""
        formatted = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            formatted += f"<|im_start|>{role}\n{content}<|im_end|>\n"
        formatted += "<|im_start|>assistant\n"
        return formatted
