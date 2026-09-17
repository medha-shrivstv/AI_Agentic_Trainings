from transformers import pipeline
from langchain_core.runnables import RunnableLambda
 
# Compatibility for mixed LangChain versions in some Colab runtimes.
try:
    import langchain
    langchain.debug = False
    langchain.verbose = False
    langchain.llm_cache = None
except ImportError:
    pass
 
generator = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct",
    max_new_tokens=100,
    do_sample=False,
    return_full_text=False
)
 
def ask_qwen(prompt):
    return generator(str(prompt))[0]["generated_text"]
 
qwen = RunnableLambda(ask_qwen)
print("Qwen loaded")