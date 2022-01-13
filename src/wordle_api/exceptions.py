class WordleException(Exception):
    """
    Root Wordle exception
    """


class InvalidGuess(WordleException):
    """
    A guess is not valid
    """
