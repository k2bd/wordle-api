from datetime import datetime

from fastapi.testclient import TestClient
from freezegun import freeze_time


def test_daily_200(api_client: TestClient):
    """
    GET /daily?size=5&guess=scale OK
    """
    with freeze_time(datetime(1992, 1, 16, 1, 1, 1)):
        # Daily 5-letter puzzle answer for 16 Jan 1992 is 'scaly'
        response = api_client.get("/daily?size=5&guess=scale")

    assert response.status_code == 200
    assert response.json() == [
        {"guess": "s", "result": "correct", "slot": 0},
        {"guess": "c", "result": "correct", "slot": 1},
        {"guess": "a", "result": "correct", "slot": 2},
        {"guess": "l", "result": "correct", "slot": 3},
        {"guess": "e", "result": "absent", "slot": 4},
    ]


def test_daily_400_too_short(api_client: TestClient):
    """
    GET /daily?size=5&guess=bad Guess too short
    """
    with freeze_time(datetime(1992, 1, 16, 1, 1, 1)):
        response = api_client.get("/daily?size=5&guess=bad")

    assert response.status_code == 400
    assert response.content == b"Guess must be the same length as the word"


def test_daily_400_nonalpha(api_client: TestClient):
    """
    GET /daily?size=5&guess=hell0 Guess not alphabetical
    """
    with freeze_time(datetime(1992, 1, 16, 1, 1, 1)):
        response = api_client.get("/daily?size=5&guess=hell0")

    assert response.status_code == 400
    assert response.content == b"Guess must only contain letters"


def test_random_200(api_client: TestClient):
    """
    GET /random?size=3&seed=12345&guess=toe OK
    """
    # Seed 12345 size 3 answer is 'out'
    response = api_client.get("/random?size=3&seed=12345&guess=toe")

    assert response.status_code == 200
    assert response.json() == [
        {"guess": "t", "result": "present", "slot": 0},
        {"guess": "o", "result": "present", "slot": 1},
        {"guess": "e", "result": "absent", "slot": 2},
    ]


def test_word_200(api_client: TestClient):
    """
    GET /word/hello?guess=aloha OK
    """
    response = api_client.get("/word/hello?guess=aloha")

    assert response.status_code == 200
    assert response.json() == [
        {"guess": "a", "result": "absent", "slot": 0},
        {"guess": "l", "result": "present", "slot": 1},
        {"guess": "o", "result": "present", "slot": 2},
        {"guess": "h", "result": "present", "slot": 3},
        {"guess": "a", "result": "absent", "slot": 4},
    ]
