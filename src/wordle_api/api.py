import logging
from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from wordle_api.exceptions import InvalidGuess
from wordle_api.wordle import GuessResult, Wordle

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(InvalidGuess)
def handle_invalid_guess(equest: Request, exc: InvalidGuess):
    return PlainTextResponse(str(exc), status_code=400)


@app.get(
    "/daily",
    response_model=List[GuessResult],
)
async def guess_daily(guess: str, size: int = 5):
    """
    Guess against the daily puzzle
    """
    return Wordle.daily(size=size).guess(guess)


@app.get(
    "/random",
    response_model=List[GuessResult],
)
async def guess_random(guess: str, size: int = 5, seed: int = None):
    """
    Guess against a random word
    """
    return Wordle.random(size=size, seed=seed).guess(guess)


@app.get(
    "/word/{word}",
    response_model=List[GuessResult],
)
async def guess_word(word: str, guess: str):
    """
    Guess against a selected word
    """
    return Wordle(solution=word.lower()).guess(guess)
