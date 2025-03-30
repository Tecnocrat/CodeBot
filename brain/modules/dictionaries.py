import os
import nltk

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

# modules/dictionaries.py
def word_recognition(input_text, dictionary_path="C:\\dev\\adn_trash_code\\dictionaries\\english_words.txt"):
    """
    Checks if the input contains valid English words from the dictionary.
    """
    try:
        with open(dictionary_path, "r", encoding="utf-8") as f:
            word_list = set(f.read().splitlines())
        input_words = set(input_text.lower().split())
        recognized_words = input_words.intersection(word_list)
        return recognized_words
    except FileNotFoundError:
        print("Error: Dictionary file not found.")
        return set()

def suggest_word(input_word, dictionary_path="C:\\dev\\adn_trash_code\\dictionaries\\english_words.txt"):
    """
    Suggests words from the dictionary that start with the same letters as the input word.
    """
    try:
        with open(dictionary_path, "r", encoding="utf-8") as f:
            word_list = [word.strip() for word in f.readlines()]
        suggestions = [word for word in word_list if word.startswith(input_word.lower())]
        return suggestions[:5]  # Return up to 5 suggestions
    except FileNotFoundError:
        print("Error: Dictionary file not found.")
        return []


# CodeBot_Tracking
