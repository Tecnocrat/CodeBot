# Functionality Map for CodeBot

## **1. Module Overview**

### **1.1 `codebot_core.py`**
- **Purpose**: Main entry point for CodeBot. Initializes the system, starts the web UI server, and manages core functionality.
- **Key Functions**:
  - `initialize_codebot`: Initializes the AI engine, logging, and metadata generation.
  - `main`: Starts the web UI server.

### **1.2 `ui_server.py`**
- **Purpose**: Handles web UI requests and routes commands to the appropriate functions.
- **Key Functions**:
  - `start_ui_server`: Starts the Flask server and launches the browser.
  - `handle_command`: Processes commands sent from the web UI.

### **1.3 `genetic/genetic_population.py`**
- **Purpose**: Manages genetic populations, including generation, evaluation, and deduplication.
- **Key Functions**:
  - `generate_population`: Creates a population of Python scripts by replicating and mutating a source file.
  - `evaluate_population`: Evaluates the fitness of individuals in a population.
  - `deduplicate_population`: Removes duplicate individuals from a population.

#### **Updated Logic**
- **`generate_population`**:
  - Validates the source file before generating individuals.
  - Prevents overwriting existing individuals unless explicitly instructed.
  - Supports growing an existing population by starting from the last individual.

- **`handle_command`**:
  - Processes "Delete" and "Grow" actions for population initialization.
  - Ensures the AI engine remains ON after initialization.

### **1.4 `core/analyze_structure.py`**
- **Purpose**: Analyzes the folder structure and generates metadata about the codebase.
- **Key Functions**:
  - `generate_knowledge_base`: Extracts metadata from all `.py` files in the project.
  - `analyze_folder_structure`: Generates a JSON representation of the folder structure.

---

## **2. Function List**

### **2.1 `codebot_core.py`**
#### `initialize_codebot`
- **Purpose**: Initializes the AI engine, logging, and metadata generation.
- **Inputs**: None.
- **Outputs**: Generates `knowledge_base.json` and `folder_structure.json`.

#### `main`
- **Purpose**: Starts the web UI server.
- **Inputs**: None.
- **Outputs**: None.

---

### **2.2 `ui_server.py`**
#### `start_ui_server`
- **Purpose**: Starts the Flask server and launches the browser.
- **Inputs**: None.
- **Outputs**: None.

#### `handle_command`
- **Purpose**: Processes commands sent from the web UI.
- **Inputs**: `command` (str), `args` (dict).
- **Outputs**: JSON response.

---

### **2.3 `genetic/genetic_population.py`**
#### `generate_population`
- **Purpose**: Creates a population of Python scripts by replicating and mutating a source file.
- **Inputs**: `source_file` (str), `population_size` (int), `dimensions` (int), `bounds` (tuple), `output_dir` (str).
- **Outputs**: List of file paths for the generated population.

#### `evaluate_population`
- **Purpose**: Evaluates the fitness of individuals in a population.
- **Inputs**: `population_dir` (str), `ai_engine` (callable).
- **Outputs**: Dictionary mapping individuals to their fitness scores.

#### `deduplicate_population`
- **Purpose**: Removes duplicate individuals from a population.
- **Inputs**: `population_dir` (str).
- **Outputs**: None.

---

## **3. Inter-Function Relationships**

| **Function**               | **Depends On**                     | **Used By**                     |
|-----------------------------|-------------------------------------|----------------------------------|
| `initialize_codebot`        | `generate_knowledge_base`          | `main`                          |
| `start_ui_server`           | None                               | `main`                          |
| `handle_command`            | `generate_population`, `evaluate_population` | Web UI                          |
| `generate_population`       | None                               | `handle_command`                |
| `evaluate_population`       | None                               | `handle_command`                |

---

## **4. Integration Points**

### **4.1 `codebot_core.py` and `ui_server.py`**
- `codebot_core.py` calls `start_ui_server` to start the Flask server.

### **4.2 `ui_server.py` and `genetic/genetic_population.py`**
- `ui_server.py` calls functions like `generate_population` and `evaluate_population` to process commands.

---

## **5. Change Log**

| **Date**       | **Module**               | **Change**                                                                 |
|-----------------|--------------------------|-----------------------------------------------------------------------------|
| 2025-04-13     | `ui_server.py`           | Added `start_ui_server` to launch the browser after starting the server.   |
| 2025-04-13     | `codebot_core.py`        | Refactored `main` to call `start_ui_server`.                               |
| 2025-04-12     | `genetic/genetic_population.py` | Added `deduplicate_population` to remove duplicate individuals.           |

---

## **6. Pending Tasks**
- [ ] Ensure dark theme toggle persists across sessions.
- [ ] Add error handling for missing `knowledge_base.json`.
- [ ] Document all functions in `genetic/genetic_optimizer.py`.