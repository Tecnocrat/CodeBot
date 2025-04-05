import os
import json
from transformers import pipeline
from core.analyze_structure import parse_codebase
from config import KNOWLEDGE_BASE_DIR
from typing import Generator

# Global variable for the text-generation model
generator = None

def preload_model():
    """
    Preloads the text-generation model for AI-driven code analysis.
    """
    global generator
    if generator is None:
        generator = pipeline("text-generation", model="gpt2")
        print("Text-generation model loaded successfully.")

def explain_python_code(code_snippet: str) -> str:
    """
    Explains a Python code snippet using the AI model.

    Args:
        code_snippet (str): The Python code snippet to explain.

    Returns:
        str: The explanation of the code snippet.
    """
    preload_model()
    prompt = f"Explain the following Python code:\n{code_snippet}"
    response = generator(prompt, max_length=100, num_return_sequences=1)
    return response[0]["generated_text"]

def suggest_code_improvements(code_snippet: str) -> str:
    """
    Suggests improvements for a Python code snippet using the AI model.

    Args:
        code_snippet (str): The Python code snippet to analyze.

    Returns:
        str: Suggested improvements for the code snippet.
    """
    preload_model()
    prompt = f"Suggest improvements for the following Python code:\n{code_snippet}"
    response = generator(prompt, max_length=100, num_return_sequences=1)
    return response[0]["generated_text"]

def analyze_file(file_path: str) -> str:
    """
    Analyzes a Python file and provides suggestions for improvement.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        str: Suggestions for improvement.
    """
    with open(file_path, "r") as f:
        code = f.read()
    return suggest_code_improvements(code)

def parse_codebase_and_evaluate(base_dir: str) -> dict:
    """
    Parses the codebase and evaluates genetic populations.
    """
    from genetic.genetic_algorithm import evaluate_population  # Lazy import to avoid circular dependency

    # Parse the codebase
    parsed_structure = parse_codebase(base_dir)

    # Evaluate genetic populations
    genetic_dir = os.path.join(base_dir, "genetic", "populations")
    if os.path.exists(genetic_dir):
        evaluation_results = evaluate_population(genetic_dir)
        parsed_structure["genetic_evaluation"] = evaluation_results

    return parsed_structure

def save_parsed_structure_to_json(parsed_structure: dict, output_file: str):
    """
    Saves the parsed structure of the codebase to a JSON file.

    Args:
        parsed_structure (dict): The parsed structure of the codebase.
        output_file (str): The path to the output JSON file.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(parsed_structure, f, indent=4)
    print(f"Parsed structure saved to {output_file}")

if __name__ == "__main__":
    # Example usage
    base_dir = "c:\\dev\\CodeBot"
    output_file = os.path.join(base_dir, "storage", "parsed_codebase.json")

    # Parse the codebase and evaluate populations
    parsed_structure = parse_codebase_and_evaluate(base_dir)

    # Save the results to a JSON file
    save_parsed_structure_to_json(parsed_structure, output_file)