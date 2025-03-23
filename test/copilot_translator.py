
# CodeBot_Tracking
def retrieve_python_concept(concept, knowledge_dir="C:\\dev\\adn_trash_code\\knowledge_base\\python"):
    """
    Searches for a Python concept across multiple files in the knowledge directory.
    """
    for file in os.listdir(knowledge_dir):
        if file.endswith(".txt"):
            file_path = os.path.join(knowledge_dir, file)
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                explanations = {line[1:].strip(): "" for line in lines if line.startswith("#")}
                for line in lines:
                    if line.startswith("#"):
                        current_key = line[1:].strip()
                    elif current_key:
                        explanations[current_key] += line
                if concept.capitalize() in explanations:
                    return explanations[concept.capitalize()]
    return "Concept not found in knowledge base."
