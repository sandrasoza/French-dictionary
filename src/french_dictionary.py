import os
import sys
from typing import Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError, PyMongoError
from dotenv import load_dotenv

load_dotenv()


CONNECTION_STRING = os.environ["MONGODB_URI"]
client = MongoClient(CONNECTION_STRING)
database = client["FrenchDictionary"]
vocab_collection: Collection = database["translations"]

def connect_to_db() -> None:
    try:
        #Connects to the cluster
        client.admin.command("ping")

        vocab_collection.create_index("english", unique=True)
        vocab_collection.create_index("french", unique=True)

        print("Success, you are connected with MongoDB")
    except PyMongoError as error:
        print(f"Failure, unable to establish connection with MongoDB: {error}")
        sys.exit(1)


def normalize(value: str) -> str:
    """ Normalize user input"""
    return value.strip().lower()


def add_word(english: str, french: str) -> None:
    """Store one pair of english & french word"""
    english = normalize(english)
    french = normalize(french)

    if not english or not french:
        raise ValueError("Both words are required")
    
    try:
        vocab_collection.insert_one({
            "english": english,
            "french": french
        })
    except DuplicateKeyError:
        raise ValueError("Translation already exist")



# Looks up a word and returns its translation when it exists.
def translate(word: str) -> Optional[str]:
    """Return a translation, or None when the word is not in the dictionary."""
    word = normalize(word)

    document = vocab_collection.find_one({
        "$or": [
            {"english": word},
            {"french": word}
        ]
    })

    if document is None:
        return None

    if document["english"] == word:
        return document["french"]

    return document["english"]


# Runs the interactive command-line dictionary program.
def main() -> None:
    connect_to_db()
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
                add_word(english, french)
            except ValueError as error:
                print(error)
            else:
                print(f"Added: {english.strip()} <-> {french.strip()}")
            continue

        result = translate(command)
        if result is not None:
            print(result)
            continue

        
        french = input("Word not found. Enter its French translation (or press Enter to skip): ")
        if french.strip():
            try:
                add_word(command, french)
            except ValueError as error:
                print(error)
            else:
                print(f"Added: {command} <-> {french.strip()}")
        else:
            print("Word not added.")


if __name__ == "__main__":
    main()
