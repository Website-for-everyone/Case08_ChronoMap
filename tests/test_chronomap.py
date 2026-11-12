"""
Test Suite for ChronoMap (Case 08)
Verifies:
1. Geodesic distance Haversine formula calculation
2. Quiz scoring algorithm (temporal and spatial delta)
3. Historical dataset integrity
4. FastAPI routes (/health, /api/events, /api/historian/ask, /api/quiz/score)
5. Bot dispatcher and keyboard generator
"""
import pytest
from fastapi.testclient import TestClient

import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
for mod in list(sys.modules.keys()):
    if mod.startswith("api") or mod.startswith("bot"):
        sys.modules.pop(mod, None)
if str(PROJECT_ROOT) in sys.path:
    sys.path.remove(str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT))

from api.server import (
    app,
    HISTORY_EVENTS,
    calculate_geodesic_distance,
    compute_quiz_score
)
from bot.bot import dp, get_quiz_keyboard

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "ChronoMap"


def test_geodesic_distance_haversine():
    # Moscow (55.75, 37.61) to St. Petersburg (59.93, 30.31) is ~630 km
    dist = calculate_geodesic_distance(55.75, 37.61, 59.93, 30.31)
    assert 600 < dist < 700

    # Same coordinates should be 0 distance
    dist_zero = calculate_geodesic_distance(41.9, 12.5, 41.9, 12.5)
    assert dist_zero == 0.0


def test_compute_quiz_score():
    # Exact guess
    res_exact = compute_quiz_score(1453, 1453, 41.0, 28.9, 41.0, 28.9)
    assert res_exact["score"] == 1000
    assert res_exact["year_delta"] == 0
    assert res_exact["rating"] == "ИДЕАЛЬНО"

    # Close guess (5 years off, 100 km off)
    res_close = compute_quiz_score(1453, 1448, 41.0, 28.9, 41.5, 29.5)
    assert 850 <= res_close["score"] < 1000

    # Very distant guess
    res_far = compute_quiz_score(-2560, 2026, 29.97, 31.13, -33.86, 151.20)
    assert res_far["score"] == 0


def test_api_events():
    response = client.get("/api/events")
    assert response.status_code == 200
    events = response.json()
    assert len(events) >= 15
    for ev in events:
        assert "year" in ev
        assert "lat" in ev
        assert "lon" in ev
        assert "name" in ev


def test_api_historian_ask():
    payload = {
        "query": "Кто был правителем в эту эпоху?",
        "year": -44,
        "epoch": "Античность"
    }
    response = client.post("/api/historian/ask", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "44 до н.э." in data["context_year"]


def test_api_quiz_score_route():
    payload = {
        "event_id": 6,  # Caesar 44 BCE
        "guessed_year": -40,
        "guessed_lat": 41.89,
        "guessed_lon": 12.48
    }
    response = client.post("/api/quiz/score", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["year_delta"] == 4
    assert data["score"] > 900


def test_bot_dispatcher_and_quiz_keyboard():
    assert dp is not None
    assert len(dp.message.handlers) >= 3

    event = HISTORY_EVENTS[0]
    kb = get_quiz_keyboard(event)
    assert len(kb.inline_keyboard) == 2
    buttons = [btn for row in kb.inline_keyboard for btn in row]
    assert len(buttons) == 4
