from llama_cpp import Llama
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "sarashina2.2-3b-instruct-v0.1-Q8_0.gguf")

llm = Llama(
    MODEL_PATH,
    n_ctx=4000,
    verbose=False
)
