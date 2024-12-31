from mlx_lm import load, generate
import os
from dotenv import load_dotenv


class PromptGenerator:
    def __init__(self):
        # Load environment variables
        load_dotenv()

        self.base_model_hf = os.getenv("BASE_MODEL_HF")
        self.adapters_path = os.getenv("ADAPTERS_RELATIVE_LOCAL_PATH")

        if not all([self.base_model_hf, self.adapters_path]):
            raise ValueError("Missing environment variables. Please check .env file.")

        # Initialize model and tokenizer
        self.model, self.tokenizer = self._initialize_model()

    def _initialize_model(self):
        """Initialize the model and tokenizer."""
        return load(self.base_model_hf, adapter_path=self.adapters_path)

    def generate_response(self, prompt: str, max_tokens: int = 200) -> str:
        """Generate a response using the initialized model and tokenizer."""
        return generate(
            self.model, tokenizer=self.tokenizer, prompt=prompt, max_tokens=max_tokens
        )
