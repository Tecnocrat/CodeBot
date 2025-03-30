from core.analyze_structure import save_structure_to_json
from optimize_structure import flatten_directory
from genetic.genetic_optimizer import genetic_algorithm

if __name__ == "__main__":
    base_dir = "c:\\dev\\CodeBot\\adn_trash_code\\replicated_CodeBot"
    output_file = "c:\\dev\\CodeBot\\folder_structure.json"
    optimized_dir = "c:\\dev\\CodeBot\\optimized_code"

    # Step 1: Analyze folder structure
    save_structure_to_json(base_dir, output_file)

    # Step 2: Flatten directory
    flatten_directory(base_dir, optimized_dir)

    # Step 3: Optimize codebase
    best_file = genetic_algorithm(optimized_dir)
    print(f"Best optimized file: {best_file}")