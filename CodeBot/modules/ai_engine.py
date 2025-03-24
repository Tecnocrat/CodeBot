from transformers import pipeline

def explain_python_code(code_snippet):
    """
    Explains the given Python code using a Hugging Face AI model.
    """
    try:
        generator = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B")
        response = generator(f"Explain the following Python code:\n{code_snippet}", max_length=100)
        return response[0]["generated_text"]
    except Exception as e:
        print(f"Error with AI engine: {e}")
        return "Unable to process the code snippet."
