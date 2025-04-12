# **CodeBot Project**

## **Overview**
CodeBot is an AI-driven system designed to automate code analysis, mutation, and optimization. By leveraging genetic algorithms, recursive chaos generation, and external AI engines, CodeBot iteratively improves its own codebase. The system evolves through self-improvement, combining structured knowledge bases with emergent behaviors from experimental code.

---

## **Core Features**

### 1. **Genetic Algorithms**
- **Population Management**:
  - Generates populations of Python scripts by replicating and mutating a source file.
  - Handles deduplication, parent selection, crossover, and mutation.
- **Fitness Evaluation**:
  - Evaluates code quality using fitness functions, including fractal-inspired fitness functions for complex optimization landscapes.
  - Logs fitness scores for debugging and analysis.
- **Generational Evolution**:
  - Runs multiple generations of genetic algorithms to optimize code quality and functionality.

### 2. **AI Integration**
- **Code Analysis**:
  - Uses AI models (e.g., Hugging Face Transformers) to analyze Python code and suggest improvements.
- **Natural Language Explanations**:
  - Provides human-readable explanations for Python code snippets.
- **Execution Log Analysis**:
  - Analyzes execution logs to generate fitness scores for genetic populations.

### 3. **Self-Improvement**
- **Code Mutation**:
  - Iteratively rewrites its own codebase to improve functionality and performance.
- **Knowledge Base Integration**:
  - Extracts metadata from all `.py` files in the project, including:
    - Function definitions and parameters.
    - Class definitions.
    - Imports and dependencies.
    - File-level metadata (e.g., character length, indentation, loop logic).
  - Stores metadata in `knowledge_base.json` for centralized access.

### 4. **Logging and Debugging**
- **Runtime Logs**:
  - Maintains detailed runtime logs for debugging and performance monitoring.
- **Execution Logs**:
  - Logs execution results for each individual in genetic populations.

### 5. **Folder and File Management**
- **Folder Structure Analysis**:
  - Analyzes and generates JSON representations of folder structures.
- **File Flattening**:
  - Moves files from nested directories into a single target directory for easier management.

---

## **Folder Structure**
The `CodeBot` project is organized as follows:
```
c:\CodeBot\
├── codebot_core.py
├── core\
│   ├── ai_engine.py
│   ├── analyze_structure.py
│   ├── self_audit.py
│   ├── self_improvement.py
│   ├── __init__.py
├── genetic\
│   ├── genetic_algorithm.py
│   ├── genetic_iteration.py
│   ├── genetic_optimizer.py
│   ├── genetic_population.py
│   ├── genetic_structure.py
│   ├── __init__.py
├── storage\
│   ├── knowledge_base\
│   │   ├── knowledge_base.json
│   │   ├── folder_structure.json
│   ├── genetic_population\
│   │   ├── individual_0.py
│   │   ├── individual_0.py_exec.log
│   │   ├── ...
│   │   ├── evaluation_results\
│   │       ├── individual_0.py_exec.log
│   │       ├── individual_0.py_README.md
├── README.md
├── requirements.txt
├── runtime_exec.log
├── ui_server.py
```

---

## **Function Processes**

### **1. `initialize_codebot`**
- **Location**: `codebot_core.py`
- **Description**:
  - Initializes the AI engine and logging.
  - Generates metadata (`knowledge_base.json`) and folder structure (`folder_structure.json`) in the `storage/knowledge_base` folder.
- **Process**:
  1. Preloads the AI engine using `preload_model`.
  2. Creates the `storage/knowledge_base` directory if it doesn't exist.
  3. Calls `generate_knowledge_base` to extract metadata from the codebase.
  4. Calls `analyze_folder_structure` to generate a JSON representation of the folder structure.

---

### **2. `generate_metadata_command`**
- **Location**: `codebot_core.py`
- **Description**:
  - Generates metadata about the codebase and saves it to `knowledge_base.json`.
- **Process**:
  1. Calls `generate_knowledge_base` from `analyze_structure.py`.
  2. Saves the metadata in the `storage/knowledge_base` folder.

---

### **3. `evaluate_population_command`**
- **Location**: `codebot_core.py`
- **Description**:
  - Evaluates genetic populations with pagination.
- **Process**:
  1. Lists available populations in groups of 10.
  2. Allows navigation between pages using `.` (next) and `,` (previous).
  3. Evaluates the selected population using `evaluate_population` from `genetic_population.py`.

---

### **4. `create_subpopulation_command`**
- **Location**: `codebot_core.py`
- **Description**:
  - Creates a new subpopulation from a chosen individual.
- **Process**:
  1. Lists available individuals from the `evaluation_results` folder.
  2. Copies the chosen individual into a new subpopulation folder.
  3. Applies mutations to create 5 variants of the individual.

---

### **5. `generate_knowledge_base`**
- **Location**: `analyze_structure.py`
- **Description**:
  - Extracts metadata from all `.py` files in the project.
- **Process**:
  1. Walks through the project directory.
  2. Extracts imports, functions, classes, and file-level metadata.
  3. Saves the metadata to `knowledge_base.json`.

---

## **Development Diary**

### **April 10, 2025**
- **Added**: `evaluate_population_command` with pagination.
- **Change**: Populations are displayed in groups of 10 with navigation options.

### **April 11, 2025**
- **Added**: `create_subpopulation_command`.
- **Change**: Subpopulations are created with 5 mutated variants of a chosen individual.

### **April 12, 2025**
- **Fixed**: Metadata and folder structure files are now saved in `storage/knowledge_base`.
- **Improved**: `evaluate_population_command` now handles invalid input gracefully.
- **Updated**: README.md with detailed descriptions of functions and processes.

---

## **How to Run**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Run CodeBot**
```bash
python codebot_core.py
```

### **3. Start the Web UI**
```bash
python ui_server.py
```

---

## **Command Reference**

1. **Generate Metadata**:
   - Command: `generate metadata`
   - Description: Generates JSON metadata for the codebase.

2. **Evaluate Population**:
   - Command: `evaluate population`
   - Description: Evaluates a genetic population with pagination.

3. **Create Subpopulation**:
   - Command: `create subpopulation`
   - Description: Creates a new subpopulation from a chosen individual.

4. **Help**:
   - Command: `help`
   - Description: Displays a list of available commands.

5. **Exit**:
   - Command: `exit`
   - Description: Gracefully exits CodeBot.

---

## **Future Goals**

1. **Enhanced Genetic Algorithms**:
   - Add support for multi-objective optimization.
   - Improve mutation and crossover strategies.

2. **AI Integration**:
   - Use AI to predict the impact of mutations on code quality.

3. **Scalability**:
   - Optimize CodeBot to handle larger codebases and more complex workflows.

4. **Documentation**:
   - Expand this README with examples and detailed explanations of each module.

---

## **Contact**
For further assistance, please interact with the CodeBot system or consult the runtime logs.