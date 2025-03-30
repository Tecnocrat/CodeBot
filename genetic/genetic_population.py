# filepath: c:\dev\CodeBot\self_improvement.py
import os
import random
import shutil
import logging
import hashlib
import autopep8
import ast
import requests
import json
from core.analyze_structure import analyze_folder_structure, save_structure_to_json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Base directories
BASE_DIR = "c:\\dev"
CODEBOT_DIR = os.path.join(BASE_DIR, "CodeBot")
ADN_TRASH_CODE_DIR = os.path.join(CODEBOT_DIR, "adn_trash_code")
STORAGE_DIR = os.path.join(CODEBOT_DIR, "storage")

def request_population(source_file, population_size, dimensions, bounds, output_dir):
    """
    Generates a complex population based on the source file and various parameters.

    Args:
        source_file (str): Path to the source file to replicate and mutate.
        population_size (int): Number of individuals in the population.
        dimensions (int): Number of dimensions for each individual.
        bounds (tuple): Bounds for each dimension (min, max).
        output_dir (str): Directory to store the generated population.

    Returns:
        list: A list of paths to the generated individuals.
    """
    os.makedirs(output_dir, exist_ok=True)
    population = []

    for i in range(population_size):
        individual_path = os.path.join(output_dir, f"individual_{i}.py")
        shutil.copy(source_file, individual_path)

        # Apply mutations based on dimensions and bounds
        with open(individual_path, 'a') as f:
            for dim in range(dimensions):
                mutation = random.uniform(bounds[0], bounds[1])
                f.write(f"# Mutation {dim}: {mutation}\n")

        # Auto-format the individual for consistency
        with open(individual_path, 'r') as f:
            code = f.read()
        formatted_code = autopep8.fix_code(code)
        with open(individual_path, 'w') as f:
            f.write(formatted_code)

        population.append(individual_path)

    logging.info(f"Generated population of size {population_size} in {output_dir}")
    return population

def log_to_os(namespace, level, message):
    """
    Sends a log message to OS/main.py for centralized logging.
    """
    try:
        # Example: Replace with actual inter-process communication if needed
        requests.post(
            "http://localhost:5000/log",  # Assuming OS/main.py runs a logging server
            json={"namespace": namespace, "level": level, "message": message}
        )
    except Exception as e:
        print(f"Failed to send log to OS: {e}")

def analyze_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    tree = ast.parse(code)
    # Analyze the AST for improvements (e.g., unused imports, redundant code)
    # Add logic to identify areas for improvement
    return "Analysis complete. Suggestions: [...]"

def auto_format_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    formatted_code = autopep8.fix_code(code)
    with open(file_path, 'w') as file:
        file.write(formatted_code)
    return "Code formatted successfully."

def fitness_function(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()
        ast.parse(code)  # Check if the code is syntactically valid
        fitness = len(code)  # Example: shorter code is better (adjust as needed)
        log_to_os("codebot", "info", f"Evaluated fitness for {file_path}: {fitness}")
        return fitness
    except Exception as e:
        log_to_os("codebot", "error", f"Error evaluating fitness for {file_path}: {e}")
        return float('inf')  # Invalid code gets the worst score

def analyze_adn_trash_code():
    """
    Recursively analyzes the contents of adn_trash_code and returns insights.
    """
    insights = []
    for root, _, files in os.walk(ADN_TRASH_CODE_DIR):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    code = f.read()
                try:
                    ast.parse(code)  # Ensure the code is syntactically valid
                    insights.append((file_path, len(code)))  # Example: Add more analysis here
                except Exception as e:
                    print(f"Error analyzing {file_path}: {e}")
    return insights

def ingest_knowledge(file_path):
    """
    Ingests external knowledge into the knowledge_base.
    """
    target_path = os.path.join(KNOWLEDGE_BASE_DIR, os.path.basename(file_path))
    os.makedirs(KNOWLEDGE_BASE_DIR, exist_ok=True)
    shutil.copy(file_path, target_path)
    print(f"Ingested knowledge from {file_path} to {target_path}")

def generate_population(source_file, population_size, output_dir):
    """
    Generates the initial population by copying the source file.
    """
    output_dir = os.path.join(ADN_TRASH_CODE_DIR, output_dir)
    os.makedirs(output_dir, exist_ok=True)
    population = []
    insights = analyze_adn_trash_code()  # Use insights to guide randomization
    for i in range(population_size):
        individual_path = os.path.join(output_dir, f"individual_{i}.py")
        shutil.copy(source_file, individual_path)
        # Apply guided randomization based on insights
        if insights:
            with open(individual_path, 'a') as f:
                f.write(f"# Insight-based mutation: {random.choice(insights)}\n")
        population.append(individual_path)
    return population

def deduplicate_population(output_dir):
    """
    Removes duplicate files in the genetic population folder by comparing file hashes.
    """
    output_dir = os.path.join(BASE_DIR, output_dir)  # Ensure output_dir is within BASE_DIR
    file_hashes = {}
    for file_name in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_hash = hashlib.md5(file.read()).hexdigest()
            if file_hash in file_hashes:
                os.remove(file_path)  # Delete duplicate file
            else:
                file_hashes[file_hash] = file_name

def select_parents(population):
    population.sort(key=fitness_function)  # Sort by fitness (lower is better)
    return population[:2]  # Select top 2 individuals

def crossover(parent1, parent2, output_file):
    with open(parent1, 'r') as file1, open(parent2, 'r') as file2:
        code1 = file1.readlines()
        code2 = file2.readlines()
    midpoint = len(code1) // 2
    child_code = code1[:midpoint] + code2[midpoint:]
    with open(output_file, 'w') as file:
        file.writelines(child_code)

def mutate(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    mutated_code = autopep8.fix_code(code)  # Example: auto-format as mutation
    with open(file_path, 'w') as file:
        file.write(mutated_code)

def create_virtual_environment(env_dir):
    """
    Creates a virtual environment in the specified directory.
    """
    venv.create(env_dir, with_pip=True)
    log_to_os("codebot", "info", f"Virtual environment created at {env_dir}")

def execute_in_virtual_environment(script_path, env_dir):
    """
    Executes a Python script in a virtual environment and logs execution time.
    """
    start_time = time.time()
    try:
        python_executable = os.path.join(env_dir, "Scripts", "python") if os.name == "nt" else os.path.join(env_dir, "bin", "python")
        result = subprocess.run([python_executable, script_path], capture_output=True, text=True)
        execution_time = time.time() - start_time
        log_to_os("codebot", "info", f"Executed {script_path} in {execution_time:.2f} seconds")
        if result.returncode == 0:
            log_to_os("codebot", "info", f"Output: {result.stdout}")
        else:
            log_to_os("codebot", "error", f"Error: {result.stderr}")
    except Exception as e:
        log_to_os("codebot", "error", f"Failed to execute {script_path}: {e}")

def run_genetic_algorithm(source_file, generations, initial_population_size, output_dir):
    """
    Runs the genetic algorithm with optimized population management and logging.
    """
    logging.info("Starting genetic algorithm...")
    output_dir = os.path.join(BASE_DIR, output_dir)
    os.makedirs(output_dir, exist_ok=True)
    population = generate_population(source_file, initial_population_size, output_dir)
    for generation in range(generations):
        logging.info(f"Generation {generation + 1}: Population size = {len(population)}")
        parents = select_parents(population)
        new_population = []
        # Limit population growth to avoid resource exhaustion
        for i in range(min(len(population), 10)):  # Limit to 10 children per generation
            child_path = os.path.join(output_dir, f"child_{generation}_{i}.py")
            crossover(parents[0], parents[1], child_path)
            mutate(child_path)
            new_population.append(child_path)
        # Execute and evaluate new population
        for child in new_population:
            execute_in_virtual_environment(child, output_dir)
        # Add new population to the existing one
        population.extend(new_population)
        # Deduplicate population
        deduplicate_population(output_dir)
        logging.info(f"Generation {generation + 1} completed.")
    # Return the best individual
    best_individual = population[0]
    logging.info(f"Best individual: {best_individual} with fitness {fitness_function(best_individual)}")
    return best_individual

def fetch_population_data(api_url):
    """
    Fetches population data from a given API URL.

    Args:
        api_url (str): The URL of the API to fetch data from.

    Returns:
        dict: The JSON response from the API.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Parse and return the JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def manage_adn_trash_code():
    """
    High-level function to manage adn_trash_code folders, prevent unnecessary nesting,
    and integrate functionality from analyze_structure.py to generate and read JSON files.

    This function:
    1. Scans the adn_trash_code directory for nested folders.
    2. Flattens the directory structure to avoid recursive nesting.
    3. Generates JSON files for folder structures using analyze_structure.py.
    4. Reads and processes JSON files from the storage directory.
    """
    # Step 1: Flatten the adn_trash_code directory
    print("Flattening adn_trash_code directory...")
    flatten_directory(ADN_TRASH_CODE_DIR)
    print("Flattening completed.")

    # Step 2: Generate JSON files for folder structures
    print("Generating JSON files for folder structures...")
    save_structure_to_json(ADN_TRASH_CODE_DIR, STORAGE_DIR)
    save_structure_to_json(CODEBOT_DIR, STORAGE_DIR)
    print("JSON generation completed.")

    # Step 3: Read and process JSON files
    print("Reading and processing JSON files...")
    folder_dev_structure_path = os.path.join(STORAGE_DIR, "folder_dev_structure.json")
    folder_codebot_structure_path = os.path.join(STORAGE_DIR, "folder_codebot_structure.json")

    if os.path.exists(folder_dev_structure_path):
        with open(folder_dev_structure_path, "r") as f:
            folder_dev_structure = json.load(f)
            print("Folder Dev Structure:", folder_dev_structure)

    if os.path.exists(folder_codebot_structure_path):
        with open(folder_codebot_structure_path, "r") as f:
            folder_codebot_structure = json.load(f)
            print("Folder CodeBot Structure:", folder_codebot_structure)

    print("adn_trash_code management completed.")

def flatten_directory(base_dir):
    """
    Flattens the directory structure by moving all files from nested directories
    into the base directory and removing empty folders.

    Args:
        base_dir (str): The base directory to flatten.
    """
    for root, dirs, files in os.walk(base_dir, topdown=False):
        for file in files:
            src_path = os.path.join(root, file)
            dest_path = os.path.join(base_dir, file)
            if not os.path.exists(dest_path):
                os.rename(src_path, dest_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):  # Remove empty directories
                os.rmdir(dir_path)

# Example usage
if __name__ == "__main__":
    source_file = os.path.join(BASE_DIR, "CodeBot", "example.py")
    output_dir = os.path.join(BASE_DIR, "CodeBot", "genetic_population")
    best_code = run_genetic_algorithm(source_file, generations=5, initial_population_size=5, output_dir=output_dir)
    print(f"Best code is located at: {best_code}")
    manage_adn_trash_code()