import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from core.analyze_structure import parse_codebase

def self_audit():
    """
    CodeBot generates a snapshot of its own structure and metadata.
    """
    base_dir = "C:\\dev\\CodeBot"
    output_file = os.path.join(base_dir, "storage", "codebot_parsed_structure.json")
    parse_codebase(base_dir, output_file)  # Generate and save the codebase structure

if __name__ == "__main__":
    self_audit()
