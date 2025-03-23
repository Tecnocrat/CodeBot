from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def ingest_browser_text(log_path="C:\\dev\\adn_trash_code\\knowledge_base\\CodeBot_conversation_log.txt"):
    """
    Captures conversation text from the browser and appends it to the log file.
    """
    try:
        # Set up the Edge WebDriver
        driver = webdriver.Edge()  # Ensure msedgedriver.exe is in PATH
        driver.get("https://your-copilot-browser-instance-url")  # Replace with actual URL

        # Wait for the page to load completely
        time.sleep(5)

        # Locate the conversation container
        conversation_element = driver.find_element(By.CLASS_NAME, "conversation-container")  # Update the class name if needed
        conversation_text = conversation_element.text

        # Append conversation to the log
        with open(log_path, "a", encoding="utf-8") as log:
            log.write(conversation_text + "\n")
        print(f"Browser conversation ingested successfully into {log_path}.")
    except Exception as e:
        print(f"Failed to ingest browser conversation: {e}")
    finally:
        driver.quit()
