from transformers import pipeline

# Initialize generator globally for session-level loading
generator = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

def explain_python_code(code_snippet):
    """
    Explains the given Python code using Hugging Face AI model.
    """
    try:
        response = generator(f"Explain the following Python code:\n{code_snippet}", max_length=100)
        return response[0]["generated_text"]
    except Exception as e:
        return f"Error with AI engine: {e}"
