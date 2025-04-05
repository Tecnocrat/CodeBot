# CodeBot Project (AI-Oriented Documentation)

## **Overview**
CodeBot is an AI-driven tool designed to automate code analysis, mutation, and optimization. It uses genetic algorithms, recursive chaos generation, and external AI engines to iteratively improve its own codebase. The system is designed to evolve through self-improvement, leveraging both controlled knowledge bases and emergent behaviors from experimental code.

---

## **Core Features**
1. **Genetic Algorithms**:
   - Handles population generation, mutation, crossover, and selection.
   - Evaluates code quality using fitness functions, including fractal-inspired fitness functions for complex optimization landscapes.

2. **AI Integration**:
   - Leverages external AI tools (e.g., Hugging Face Transformers) for advanced code analysis and mutation guidance.
   - Provides natural language explanations and suggestions for Python code.

3. **Self-Improvement**:
   - Iteratively rewrites its own codebase to improve functionality and performance.
   - Interfaces with the AI engine to analyze genetic outputs and runtime logs.

4. **Logging and Debugging**:
   - Maintains detailed runtime logs for debugging and performance monitoring.
   - Centralized logging via `log_to_os` for inter-process communication.

5. **Folder Management**:
   - Manages and flattens recursive folder structures in `adn_trash_code`.
   - Generates and processes JSON files for folder structures.

6. **Knowledge Base Integration**:
   - Combines controlled knowledge bases with emergent behaviors from experimental code.
   - Extracts metadata from files and generates a snapshot of the CodeBot structure.

---

## **Folder Structure**
The `CodeBot` folder is organized as follows:
```
c:\dev\CodeBot\
├── codebot_core.py
├── core\
│   ├── ai_engine.py
│   ├── self_improvement.py
│   ├── analyze_structure.py
├── genetic\
│   ├── genetic_algorithm.py
│   ├── genetic_iteration.py
│   ├── genetic_optimizer.py
│   ├── genetic_structure.py
│   ├── genetic_population.py
├── storage\
│   ├── folder_codebot_structure.json
│   ├── knowledge_base.json
├── README.md
```

---

## **How to Run**
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run CodeBot:
   ```bash
   python codebot_core.py
   ```
3. Generate Metadata:
   ```bash
   python core/analyze_structure.py
   ```

---

## **Recent Changes**

### **1. JSON Metadata Generation**
- **Location**: `core/analyze_structure.py`
- **Purpose**:
  - Generates JSON files for folder structures, imports, and module definitions.
  - Detects AI-related behaviors in the codebase.

### **2. Improved `fitness_function`**
- **Location**: `genetic/genetic_optimizer.py`
- **Enhancements**:
  - Evaluates code quality based on syntax validity and length.
  - Logs fitness scores for debugging.

### **3. Expanded `sanitize_input`**
- **Location**: `genetic/genetic_optimizer.py`
- **Enhancements**:
  - Added JSON validation logic.
  - Improved error handling for invalid inputs.

---

## **Command Reference**

### **Chatbot Commands**
1. **Generate Metadata**:
   - Command: `generate metadata`
   - Description: Generates JSON metadata for the codebase.

2. **Run Genetic Algorithm**:
   - Command: `run genetic algorithm`
   - Description: Executes the genetic algorithm to optimize the codebase.

3. **Explain Python Code**:
   - Command: `explain python <code_snippet>`
   - Example:
     ```bash
     explain python def add(a, b): return a + b
     ```

---

## **Future Goals**

1. **Enhanced Genetic Algorithms**:
   - Improve fitness functions to evaluate code quality more comprehensively.
   - Add support for multi-objective optimization.

2. **AI Integration**:
   - Integrate with external AI engines for advanced code analysis and optimization.

3. **Scalability**:
   - Optimize CodeBot to handle larger codebases and more complex workflows.

4. **Documentation**:
   - Expand this README with detailed explanations of each module and function.

---

## **Contact**
For further assistance, please interact with the CodeBot system or consult the runtime logs.