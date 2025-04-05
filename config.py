import os

# Base directory for the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Debugging: Print BASE_DIR to verify correctness
print(f"BASE_DIR is set to: {BASE_DIR}")

# Storage directory inside CodeBot
STORAGE_DIR = os.path.join(BASE_DIR, "storage")

# Knowledge base and genetic population directories
KNOWLEDGE_BASE_DIR = os.path.join(STORAGE_DIR, "knowledge_base")
GENETIC_POPULATION_DIR = os.path.join(STORAGE_DIR, "genetic_population")

# Ensure the directories exist
os.makedirs(STORAGE_DIR, exist_ok=True)
os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
os.makedirs(GENETIC_POPULATION_DIR, exist_ok=True)