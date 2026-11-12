"""
ChronoMap // FastAPI Backend & AI Historian Engine
Case 08 — Interactive 3D History Globe & ChronoQuiz
"""
import math
from typing import List, Dict, Any, Optional
from pathlib import Path
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="ChronoMap API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "web"


# Historical Events Database
HISTORY_EVENTS = [
    {"id": 1, "year": -2560, "lat": 29.97, "lon": 31.13, "name": "Строительство Великой пирамиды в Гизе", "epoch": "Бронзовый век", "loc": "Гиза, Древний Египет", "desc": "Фараон Хеопс воздвиг крупнейшую пирамиду античного мира."},
    {"id": 2, "year": -1750, "lat": 32.53, "lon": 44.42, "name": "Свод законов Хаммурапи", "epoch": "Бронзовый век", "loc": "Вавилон, Месопотамия", "desc": "Один из древнейших правовых памятников человечества ('око за око')."},
    {"id": 3, "year": -753, "lat": 41.90, "lon": 12.49, "name": "Основание Рима", "epoch": "Античность", "loc": "Лациум, Италия", "desc": "Ромул и Рем основали вечный город на холмах Тибра."},
    {"id": 4, "year": -490, "lat": 38.11, "lon": 23.97, "name": "Марафонская битва", "epoch": "Античность", "loc": "Аттика, Древняя Греция", "desc": "Греческие гоплиты разбили персидскую армию Дария I."},
    {"id": 5, "year": -331, "lat": 36.36, "lon": 43.25, "name": "Битва при Гавгамелах", "epoch": "Античность", "loc": "Ассирия, Империя Ахеменидов", "desc": "Александр Македонский разбил войско Дария III."},
    {"id": 6, "year": -44, "lat": 41.89, "lon": 12.48, "name": "Мартовские иды: Убийство Цезаря", "epoch": "Античность", "loc": "Рим, Римская республика", "desc": "Группа сенаторов во главе с Брутом и Кассием убила Юлия Цезаря."},
    {"id": 7, "year": 330, "lat": 41.00, "lon": 28.97, "name": "Основание Константинополя", "epoch": "Античность", "loc": "Босфор, Византия", "desc": "Император Константин Великий основал столицу Византии на Босфоре."},
    {"id": 8, "year": 622, "lat": 24.46, "lon": 39.61, "name": "Хиджра Пророка Мухаммада", "epoch": "Средневековье", "loc": "Медина, Аравия", "desc": "Переселение мусульманской общины из Мекки в Медину."},
    {"id": 9, "year": 862, "lat": 58.52, "lon": 31.27, "name": "Призвание варягов на Русь", "epoch": "Средневековье", "loc": "Новгород, Древняя Русь", "desc": "Князь Рюрик сел княжить в Новгороде, положив начало династии."},
    {"id": 10, "year": 1066, "lat": 50.91, "lon": 0.48, "name": "Битва при Гастингсе", "epoch": "Средневековье", "loc": "Суссекс, Англия", "desc": "Вильгельм Завоеватель начал нормандское завоевание Англии."},
    {"id": 11, "year": 1242, "lat": 58.68, "lon": 27.86, "name": "Ледовое побоище", "epoch": "Средневековье", "loc": "Чудское озеро, Русь", "desc": "Александр Невский разбил ливонских рыцарей на льду."},
    {"id": 12, "year": 1453, "lat": 41.01, "lon": 28.97, "name": "Падение Константинополя", "epoch": "Возрождение", "loc": "Константинополь, Османская империя", "desc": "Султан Мехмед II Фатих взял штурмом столицу Византии."},
    {"id": 13, "year": 1492, "lat": 24.06, "lon": -74.53, "name": "Экспедиция Колумба достигла Америки", "epoch": "Возрождение", "loc": "Багамы, Новый Свет", "desc": "Христофор Колумб открыл путь в Новый Свет."},
    {"id": 14, "year": 1703, "lat": 59.93, "lon": 30.31, "name": "Основание Санкт-Петербурга", "epoch": "Возрождение", "loc": "Балтика, Российская империя", "desc": "Петр I заложил Петропавловскую крепость на Неве."},
    {"id": 15, "year": 1789, "lat": 48.85, "lon": 2.35, "name": "Взятие Бастилии: Французская революция", "epoch": "Промышленный век", "loc": "Париж, Франция", "desc": "Падение крепости-тюрьмы Бастилии положило начало революции."},
    {"id": 16, "year": 1812, "lat": 55.51, "lon": 35.82, "name": "Бородинское сражение", "epoch": "Промышленный век", "loc": "Бородино, Российская империя", "desc": "Крупнейшая битва войны 1812 года между Кутузовым и Наполеоном."},
    {"id": 17, "year": 1914, "lat": 43.85, "lon": 18.41, "name": "Сараевское покушение", "epoch": "Новейшее время", "loc": "Сараево, Босния", "desc": "Убийство Франца Фердинанда стало поводом к Первой мировой войне."},
    {"id": 18, "year": 1945, "lat": 52.52, "lon": 13.40, "name": "Знамя Победы над Рейхстагом", "epoch": "Новейшее время", "loc": "Берлин, Германия", "desc": "Водружение Знамени Победы ознаменовало разгром нацизма."},
    {"id": 19, "year": 1961, "lat": 45.92, "lon": 63.30, "name": "Полет Юрия Гагарина в космос", "epoch": "Новейшее время", "loc": "Байконур, СССР", "desc": "Первый в истории пилотируемый полет на корабле 'Восток-1'."},
    {"id": 20, "year": 1969, "lat": 0.67, "lon": 23.47, "name": "Высадка на Луну (Аполлон-11)", "epoch": "Новейшее время", "loc": "Море Спокойствия, Луна", "desc": "Нил Армстронг сделал первый шаг человека по поверхности Луны."}
]


# Geodesic Haversine Formula for distance between two (lat, lon) points
def calculate_geodesic_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# Scoring formula: 1000 base minus penalty for delta years and delta distance
def compute_quiz_score(actual_year: int, guessed_year: int,
                       actual_lat: float, actual_lon: float,
                       guessed_lat: float, guessed_lon: float) -> Dict[str, Any]:
    year_delta = abs(actual_year - guessed_year)
    dist_km = calculate_geodesic_distance(actual_lat, actual_lon, guessed_lat, guessed_lon)

    year_penalty = year_delta * 4.0
    dist_penalty = dist_km / 12.0

    score = max(0, int(1000 - year_penalty - dist_penalty))
    return {
        "score": score,
        "year_delta": year_delta,
        "distance_km": round(dist_km, 1),
        "rating": "ИДЕАЛЬНО" if score > 800 else ("ОТЛИЧНО" if score > 500 else ("НЕПЛОХО" if score > 200 else "МИМО"))
    }


class HistorianQuery(BaseModel):
    query: str
    year: int = -44
    epoch: str = "Античность"


class QuizScoreRequest(BaseModel):
    event_id: int
    guessed_year: int
    guessed_lat: float
    guessed_lon: float


@app.get("/health")
async def health_check():
    return {"status": "ok", "app": "ChronoMap", "version": "1.0.0"}


@app.get("/api/events")
async def get_events(year: Optional[int] = None, window: int = 300):
    if year is None:
        return JSONResponse(content=HISTORY_EVENTS)
    filtered = [ev for ev in HISTORY_EVENTS if abs(ev["year"] - year) <= window]
    return JSONResponse(content=filtered)


@app.post("/api/historian/ask")
async def ask_historian(req: HistorianQuery):
    formatted_year = f"{abs(req.year)} до н.э." if req.year < 0 else f"{req.year} н.э."
    query_lower = req.query.lower()

    if "правител" in query_lower or "цар" in query_lower or "император" in query_lower:
        answer = f"В эпоху {req.epoch} ({formatted_year}) ключевыми правителями выступали лидеры ведущих держав того периода: их реформы и военные походы определили контуры континентальной геополитики."
    elif "торгов" in query_lower or "путь" in query_lower or "шелк" in query_lower:
        answer = f"Торговые маршруты {formatted_year} года связывали ключевые узлы цивилизаций: морские пути Средиземноморья и караванные трассы обеспечивали транзит специй, металла, шелка и зерна."
    elif "битв" in query_lower or "войн" in query_lower or "сражен" in query_lower:
        answer = f"Военные конфликты периода {formatted_year} знаменовали смену гегемонии: столкновение регулярных армий приводило к аннексии провинций и формированию новых правовых систем."
    else:
        answer = f"Анализируя эпоху {req.epoch} ({formatted_year}): цивилизационный ландшафт характеризовался высокой динамикой институтов власти, развитием монументальной архитектуры и глубоким культурным обменом между регионами."

    return JSONResponse(content={
        "answer": answer,
        "context_year": formatted_year,
        "epoch": req.epoch
    })


@app.post("/api/quiz/score")
async def api_quiz_score(req: QuizScoreRequest):
    event = next((ev for ev in HISTORY_EVENTS if ev["id"] == req.event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    res = compute_quiz_score(
        actual_year=event["year"],
        guessed_year=req.guessed_year,
        actual_lat=event["lat"],
        actual_lon=event["lon"],
        guessed_lat=req.guessed_lat,
        guessed_lon=req.guessed_lon
    )
    res["event_name"] = event["name"]
    res["actual_year"] = event["year"]
    res["actual_location"] = event["loc"]
    return JSONResponse(content=res)


if WEB_DIR.exists():
    app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="web")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8008, reload=False)
