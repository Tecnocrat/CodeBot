import time
import os
from modules.compression import compress_libraries

def summarize_runtime(start_time, actions, filename="runtime_summary.txt", library="runtime_library.txt"):
    """
    Summarizes runtime by writing start/end times, elapsed time, and actions taken.
    Appends the summary to two files and compresses the result.
    """
    end_time = time.time()
    elapsed_time = end_time - start_time

    target_folder = os.path.join(os.path.dirname(os.getcwd()), "adn_trash_code")
    os.makedirs(target_folder, exist_ok=True)

    summary_path = os.path.join(target_folder, filename)
    with open(summary_path, "a", encoding="utf-8") as file:
        file.write("Runtime Summary:\n")
        file.write(f"Start Time: {time.ctime(start_time)}\n")
        file.write(f"End Time: {time.ctime(end_time)}\n")
        file.write(f"Elapsed Time: {elapsed_time:.2f} seconds\n")
        file.write("Actions Taken:\n")
        for action in actions:
            file.write(f"- {action}\n")
        file.write("\n")
    
    library_path = os.path.join(target_folder, library)
    with open(library_path, "a", encoding="utf-8") as file:
        file.write(f"Runtime {time.ctime(start_time)}:\n")
        for action in actions:
            file.write(f"- {action}\n")
        file.write(f"Elapsed Time: {elapsed_time:.2f} seconds\n")
        file.write("\n")
    
    compress_libraries(target_folder=target_folder)
    print(f"Runtime summary saved to {filename} and appended to {library}.")

# CodeBot_Tracking
