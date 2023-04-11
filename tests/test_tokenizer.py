import pytest

from lambda_function import lambda_handler


@pytest.mark.parametrize(
    "input_string,expected_output",
    (
        # The empty string tokenizes to no tokens
        ("", []),

        # Strings containing only whitespace tokenize to no tokens
        (" ", []),
        (" \t\n\r", []),

        # A basic string tokenizes as expected
        ("hello niall", ["hello", "niall"]),

        # Leading and trailing whitespace is stripped
        (" hello niall", ["hello", "niall"]),
        ("hello niall ", ["hello", "niall"]),

        # Multiple whitespace counts as one whitespace
        ("\r\r hello \t\t\nniall ", ["hello", "niall"]),

        # Tokens are lowercase
        ("Hello Niall", ["hello", "niall"]),
        ("HELLO NIALL", ["hello", "niall"]),
        ("hEllO NiALl", ["hello", "niall"]),

        # Punctuation is stripped
        ("hello niall!", ["hello", "niall"]),
        ("hello, world!", ["hello", "world"]),
        ("¡Hola, mundo!", ["hola", "mundo"]),
        ("Olá, Mundo!", ["olá", "mundo"]),

        # Apostrophes are not stripped
        ("don't worry be happy", ["don't", "worry", "be", "happy"]),
    ))
def test_tokenizer(input_string, expected_output):
    assert lambda_handler.tokenize(input_string) == expected_output
