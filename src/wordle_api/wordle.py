import binascii
from datetime import date
from enum import Enum
from string import ascii_lowercase
from typing import List, Optional

from fastapi_camelcase import CamelModel
from numpy.random import RandomState

from wordle_api.exceptions import InvalidGuess
from wordle_api.words import candidate_words


class ResultKind(str, Enum):
    ABSENT = "absent"
    PRESENT = "present"
    CORRENT = "correct"

    def square(self):
        if self == ResultKind.CORRENT:
            return "🟧"
        elif self == ResultKind.PRESENT:
            return "🟦"
        else:
            return "⬛"


class GuessResult(CamelModel):
    #: Slot
    slot: int

    #: Guess letter
    guess: str

    #: Result
    result: ResultKind


class Wordle(CamelModel):
    """
    A Wordle puzzle
    """

    #: The solution to the puzzle
    solution: str

    @classmethod
    def random(cls, size: int = 5, seed=None):
        """
        Get a random puzzle
        """
        words = candidate_words(size=size)

        random_state = RandomState(seed=seed)
        word = random_state.choice(words)

        return cls(solution=word)

    @classmethod
    def daily(cls, puzzle_date: Optional[date] = None, size: int = 5):
        """
        Get the daily puzzle
        """
        puzzle_date = puzzle_date or date.today()

        date_bytes = puzzle_date.isoformat().encode("utf-8")
        date_hex = binascii.hexlify(date_bytes)

        seed = int(date_hex, base=16) % (2 ** 32 - 1)

        return cls.random(size=size, seed=seed)

    def guess(self, guess_word: str) -> List[GuessResult]:
        """
        Get the result of a single guess
        """
        guess_word = guess_word.lower()

        if len(guess_word) != len(self.solution):
            raise InvalidGuess("Guess must be the same length as the word")

        if not all(letter in ascii_lowercase for letter in guess_word):
            raise InvalidGuess("Guess must only contain letters")

        def classify_guess(guess_letter: str, real_letter: str):
            kind = ResultKind.ABSENT
            if guess_letter == real_letter:
                kind = ResultKind.CORRENT
            elif guess_letter in self.solution:
                kind = ResultKind.PRESENT
            return kind

        return [
            GuessResult(
                slot=i,
                guess=guess_letter,
                result=classify_guess(guess_letter, real_letter),
            )
            for i, (guess_letter, real_letter) in enumerate(
                zip(guess_word, self.solution)
            )
        ]

    def report(self, guesses: List[str]) -> str:
        """
        Get an emoji report of a set of guesses
        """
        return "\n".join(
            "".join([r.result.square() for r in self.guess(g)]) for g in guesses
        )
