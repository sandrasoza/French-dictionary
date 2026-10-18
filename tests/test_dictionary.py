from unittest.mock import Mock
import os
import src.french_dictionary as dictionary

def test_connect_to_bd_prints_success(monkeypatch, capsys):
    mock_client = Mock()
    mock_collection = Mock()

    monkeypatch.setattr(dictionary, "client", mock_client)
    monkeypatch.setattr(dictionary, "vocab_collection", mock_collection)

    dictionary.connect_to_db()

    captured = capsys.readouterr()

    assert "Success, you are connected with MongoDB" in captured.out
    mock_client.admin.command.assert_called_once_with("ping")


def test_normalize_removes_whitespace_and_lowercases():
    assert dictionary.normalize("  Bonjour  ") == "bonjour"


def test_translate_from_english_to_french(monkeypatch):
    mock_collection = Mock()
    mock_collection.find_one.return_value = {
        "french": "bonjour",
        "english": "hello",
    }

    monkeypatch.setattr(dictionary, "vocab_collection", mock_collection)

    assert dictionary.translate("hello") == "bonjour"
    mock_collection.find_one.assert_called_once()


def test_translate_from_french_to_english(monkeypatch):
    mock_collection = Mock()
    mock_collection.find_one.return_value = {
        "french": "bonjour",
        "english": "hello",
    }

    monkeypatch.setattr(dictionary, "vocab_collection", mock_collection)

    assert dictionary.translate("bonjour") == "hello"
    mock_collection.find_one.assert_called_once()

