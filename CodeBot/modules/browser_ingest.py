from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def ingest_browser_text(log_path="C:\\dev\\adn_trash_code\\knowledge_base\\CodeBot_conversation_log.txt"):
    """
    Captures conversation text from the browser and appends it to the log file.
    """
    try:
        # Set up the Edge WebDriver
        driver = webdriver.Edge()
        driver.get("https://copilot.microsoft.com/chats/hdbdSkjsYJbBF38j6bnhG")  # Replace with your actual URL

        # Wait for the conversation container to load
        wait = WebDriverWait(driver, 10)
        conversation_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "conversation-container")))
        conversation_text = conversation_element.text

        # Append conversation to the log
        with open(log_path, "a", encoding="utf-8") as log:
            log.write(conversation_text + "\n")
        print(f"Browser conversation ingested successfully into {log_path}.")
    except Exception as e:
        print(f"Failed to ingest browser conversation: {e}")
    finally:
        driver.quit()
