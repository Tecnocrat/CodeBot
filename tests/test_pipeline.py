import sys
import os
import pytest
from genetic.genetic_algorithm import fractal_genetic_algorithm
from utils.pipeline import save_structure_to_json
from genetic.genetic_algorithm import flatten_directory

# Add CodeBot to the Python path
sys.path.append(os.path.abspath("C:\\dev\\CodeBot"))

@pytest.mark.timeout(10)  # Fail the test if it runs longer than 10 seconds
def test_pipeline():
    base_dir = "c:\\dev\\CodeBot\\adn_trash_code\\replicated_CodeBot"
    output_file = "c:\\dev\\CodeBot\\folder_structure.json"
    optimized_dir = "c:\\dev\\CodeBot\\optimized_code"

    # Step 1: Analyze folder structure
    save_structure_to_json(base_dir, output_file)
    assert os.path.exists(output_file)

    # Step 2: Flatten directory
    flatten_directory(base_dir, optimized_dir)
    assert os.path.exists(optimized_dir)

    # Step 3: Run fractal genetic algorithm
    dimensions = 5  # Number of dimensions in the hyperspatial space
    generations = 10  # Reduced for testing purposes
    population_size = 10  # Reduced for testing purposes
    bounds = (-10, 10)  # Bounds for each dimension

    best_solution = fractal_genetic_algorithm(dimensions, generations, population_size, bounds)
    assert best_solution is not None
    assert isinstance(best_solution, list)
    assert len(best_solution) == dimensions