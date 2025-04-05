import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from analyze_structure import parse_codebase

def self_audit():
    """
    CodeBot generates a snapshot of its own structure and metadata.
    """
    base_dir = "C:\\dev\\CodeBot"
    parse_codebase(base_dir)  # Generate and save the codebase structure

if __name__ == "__main__":
    self_audit()
