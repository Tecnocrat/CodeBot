import os
import nltk

# Download wordlists from NLTK
nltk.download("words")
nltk.download("stopwords")

from nltk.corpus import words, stopwords

def save_wordlists(output_folder):
    """
    Saves English words and stopwords to separate files in the specified folder.
    """
    os.makedirs(output_folder, exist_ok=True)
    
    # Save English wordlist
    words_path = os.path.join(output_folder, "english_words.txt")
    with open(words_path, "w", encoding="utf-8") as f:
        f.write("\n".join(words.words()))
    print(f"Saved wordlist to {words_path}")
    
    # Save stopwords
    stopwords_path = os.path.join(output_folder, "stopwords.txt")
    with open(stopwords_path, "w", encoding="utf-8") as f:
        f.write("\n".join(stopwords.words("english")))
    print(f"Saved stopwords to {stopwords_path}")

# Usage
save_wordlists("C:\\dev\\adn_trash_code\\dictionaries")

# CodeBot_Tracking
