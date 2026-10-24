# French Dictionary

A command-line English ↔ French dictionary written in Python and backed by MongoDB.
Type a word in either language to get its translation. If the word isn't in the
dictionary yet, the app asks for the translation and saves it.

**Status:** in progress

## Features
- Translates in both directions (English → French and French → English)
- Adds new word pairs from user input, or with the `add` command
- Normalizes input (trims spaces, ignores case)
- Unique indexes in MongoDB prevent duplicate entries
- Connection string is read from an environment variable, never stored in code

## Tech stack
- Python 3
- MongoDB (via `pymongo`)
- `python-dotenv` for configuration
- `pytest` with mocks for unit tests, plus a Bash script for input validation

## Getting started
1. Clone the repository and install dependencies:
   ```bash
   git clone https://github.com/sandrasoza/French-dictionary.git
   cd French-dictionary
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the project root with your MongoDB connection string:
   ```
   MONGODB_URI=your-connection-string-here
   ```
3. Run the app:
   ```bash
   python src/french_dictionary.py
   ```
   Type a word to translate it, `add` to add a pair, or `exit` to quit.

## Running the tests
```bash
python -m pytest
bash tests/test_dictionary.sh "hello"
```
The pytest tests use mocks, so they don't need a live database.

## Project structure
```
src/french_dictionary.py    # app logic and command-line interface
tests/test_dictionary.py    # pytest unit tests (mocked MongoDB)
tests/test_dictionary.sh    # Bash input-validation checks
dictionary.json             # starter word list
```

## Planned improvements
- Load `dictionary.json` into MongoDB as starter data
- GitHub Actions pipeline to run tests on every push
- Docker setup for running locally with MongoDB