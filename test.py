import warnings
from core.ai_engine import explain_python_code, suggest_code_improvements

# Suppress Hugging Face warnings
warnings.filterwarnings("ignore", category=UserWarning)

print(explain_python_code("def add(a, b): return a + b"))
print(suggest_code_improvements("def add(a, b): return a + b"))