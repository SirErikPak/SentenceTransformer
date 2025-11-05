from importlib.metadata import version
import sys

print("SentenceTransformer Version:", version("sentence-transformers"))
print("PyTorch Version:", version("torch"))
print("Transformers Version:", version("transformers"))
print("Tokenizers Version:", version("tokenizers"))
print("Datasets Version:", version("datasets"))
print("Numpy Version:", version("numpy"))
print("Python Version:", sys.version)