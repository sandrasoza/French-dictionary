import json
from pathlib import Path
from typing import Optional


DEFAULT_WORDS = {
    "hello": "bonjour",
    "goodbye": "au revoir",
    "thank you": "merci",
    "please": "s'il vous plaît",
    "yes": "oui",
    "no": "non",
}
DATA_FILE = Path(__file__).resolve().parent.parent / "dictionary.json"


# Builds the default dictionary and adds any translations saved from earlier runs.
def create_dictionary(file_path: Path = DATA_FILE) -> dict[str, str]:
    """Create a dictionary that can translate in either direction."""
    dictionary = {}
    for english, french in DEFAULT_WORDS.items():
        add_word(dictionary, english, french)
    if file_path.exists():
        try:
            saved_words = json.loads(file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            saved_words = {}
        for english, french in saved_words.items():
            add_word(dictionary, english, french)
    return dictionary


# Adds an English/French pair and both directions of its translation.
def add_word(dictionary: dict[str, str], english: str, french: str) -> None:
    """Add an English/French pair and its reverse lookup."""
    english = english.strip().lower()
    french = french.strip().lower()
    if not english or not french:
        raise ValueError("Both words are required.")
    dictionary[english] = french
    dictionary[french] = english


# Writes the current translations to the JSON data file.
def save_dictionary(dictionary: dict[str, str], file_path: Path = DATA_FILE) -> None:
    """Save all translations so they are available the next time the program runs."""
    file_path.write_text(json.dumps(dictionary, ensure_ascii=False, indent=2), encoding="utf-8")


# Looks up a word and returns its translation when it exists.
def translate(word: str, dictionary: dict[str, str]) -> Optional[str]:
    """Return a translation, or None when the word is not in the dictionary."""
    return dictionary.get(word.strip().lower())


# Runs the interactive command-line dictionary program.
def main() -> None:
    dictionary = create_dictionary()
    print("English/French dictionary")
    print("Type a word to translate, 'add' to add a pair, or 'exit' to quit.")

    while True:
        command = input("> ").strip()
        if command.lower() == "exit":
            print("Goodbye!")
            return
        if command.lower() == "add":
            english = input("English word: ")
            french = input("French translation: ")
            try:
                add_word(dictionary, english, french)
            except ValueError as error:
                print(error)
            else:
                save_dictionary(dictionary)
                print(f"Added: {english.strip()} <-> {french.strip()}")
            continue

        result = translate(command, dictionary)
        if result is None:
            french = input("Word not found. Enter its French translation (or press Enter to skip): ")
            if french.strip():
                try:
                    add_word(dictionary, command, french)
                except ValueError as error:
                    print(error)
                else:
                    save_dictionary(dictionary)
                    print(f"Added: {command} <-> {french.strip()}")
            else:
                print("Word not added.")
        else:
            print(result)


if __name__ == "__main__":
    main()
