from datetime import date
from typing import List

import pytest

from wordle_api.exceptions import InvalidGuess
from wordle_api.wordle import GuessResult, ResultKind, Wordle

EXAMPLE_REPORT = """🟧⬛⬛🟧⬛
⬛⬛🟦🟦⬛
⬛⬛🟦🟦⬛
⬛⬛⬛⬛⬛
🟦⬛🟦⬛⬛
🟧🟧🟧🟧🟧"""


def test_daily():
    """
    Daily puzzle is consistent
    """
    example_date = date(1992, 1, 16)
    assert Wordle.daily(size=4, puzzle_date=example_date) == Wordle(solution="port")
    assert Wordle.daily(size=5, puzzle_date=example_date) == Wordle(solution="scaly")


def test_random():
    """
    A random puzzle is consistent
    """
    seed = 12345
    assert Wordle.random(size=3, seed=seed) == Wordle(solution="ore")
    assert Wordle.random(size=5, seed=seed) == Wordle(solution="cabot")


@pytest.mark.parametrize(
    "guess, expected",
    [
        (
            "kevin",
            [
                ResultKind.CORRENT,
                ResultKind.CORRENT,
                ResultKind.CORRENT,
                ResultKind.CORRENT,
                ResultKind.CORRENT,
            ],
        ),
        (
            "nivek",
            [
                ResultKind.PRESENT,
                ResultKind.PRESENT,
                ResultKind.CORRENT,
                ResultKind.PRESENT,
                ResultKind.PRESENT,
            ],
        ),
        (
            "table",
            [
                ResultKind.ABSENT,
                ResultKind.ABSENT,
                ResultKind.ABSENT,
                ResultKind.ABSENT,
                ResultKind.PRESENT,
            ],
        ),
        (
            "LEveL",
            [
                ResultKind.ABSENT,
                ResultKind.CORRENT,
                ResultKind.CORRENT,
                ResultKind.PRESENT,
                ResultKind.ABSENT,
            ],
        ),
    ],
)
def test_guess(guess: str, expected: List[ResultKind]):
    """
    Guessing works, against the clue "kevin"
    """
    wordle = Wordle(solution="kevin")
    expected = [
        GuessResult(slot=i, guess=letter.lower(), result=expected_kind)
        for i, (letter, expected_kind) in enumerate(zip(guess, expected))
    ]

    assert wordle.guess(guess_word=guess) == expected


def test_guess_wrong_size():
    """
    Wrong size guess raises an exception
    """
    with pytest.raises(InvalidGuess):
        Wordle(solution="grape").guess("lentil")


def test_guess_non_alphabetical():
    """
    Non-alphabetical guess raises an exception
    """
    with pytest.raises(InvalidGuess):
        Wordle(solution="kelp").guess("k2bd")


def test_report():
    """
    Can generate an emoji report of a set of guesses
    """
    report = Wordle(solution="abbey").report(
        [
            "anger",
            "steam",
            "plead",
            "quick",
            "bravo",
            "abbey",
        ]
    )

    assert report == EXAMPLE_REPORT
