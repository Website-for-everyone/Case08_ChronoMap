"""
ChronoMap // ChronoQuiz Telegram Bot (Aiogram 3.x)
Case 08 — Interactive 3D History Globe & Historical Trivia Engine
"""
import os
import random
import logging
from typing import Dict, Any
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from api.server import HISTORY_EVENTS, compute_quiz_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ChronoQuizBot")

TOKEN = os.getenv("BOT_TOKEN", "TEST_TOKEN_CHRONOMAP")
dp = Dispatcher()

# In-memory user state & leaderboard
# user_state[user_id] = { "current_event": {...}, "score": int, "attempts": int }
user_sessions: Dict[int, Dict[str, Any]] = {}
leaderboard: Dict[str, int] = {
    "@Idrisov_prod": 4850,
    "@ChronosMaster": 3920,
    "@HistorianAI": 2840
}


def get_quiz_keyboard(event: Dict[str, Any]) -> InlineKeyboardMarkup:
    actual_year = event["year"]
    # Generate 1 correct and 3 plausible distractors
    offsets = [-150, -30, 0, 80, 210]
    random.shuffle(offsets)
    years = [actual_year + off for off in offsets[:4]]
    if actual_year not in years:
        years[0] = actual_year
    random.shuffle(years)

    buttons = []
    for y in years:
        label = f"{abs(y)} до н.э." if y < 0 else f"{y} г. н.э."
        buttons.append(InlineKeyboardButton(text=label, callback_data=f"guess_{event['id']}_{y}"))

    # 2 rows of 2 buttons
    return InlineKeyboardMarkup(inline_keyboard=[buttons[:2], buttons[2:]])


@dp.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "🏛 **Добро пожаловать в ChronoQuiz 3D!**\n\n"
        "Проверьте свои знания 5000 лет мировой истории!\n"
        "Я загадываю великое историческое событие, а ваша задача — "
        "угадать точный год и географическую локацию.\n\n"
        "⚡ За точность начисляются баллы (максимум 1000 за вопрос) с учетом формулы геодезического расстояния и временной дельты.\n\n"
        "Команды:\n"
        "• `/quiz` — начать раунд викторины\n"
        "• `/leaderboard` — посмотреть таблицу лидеров\n"
        "• `/help` — правила и расчет очков"
    )
    await message.answer(welcome_text, parse_mode="Markdown")


@dp.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "📜 **Правила ChronoQuiz:**\n\n"
        "1. Нажмите `/quiz` для получения вопроса.\n"
        "2. Выберите год на интерактивной клавиатуре или отправьте число сообщением (например, `1453`).\n"
        "3. Чем ближе ваш ответ к реальному году и месту события, тем выше балл:\n"
        "   `Score = max(0, 1000 - 4 * YearDelta - DistanceDelta / 12)`\n"
        "4. Все очки сохраняются в глобальной таблице лидеров!"
    )
    await message.answer(text, parse_mode="Markdown")


@dp.message(Command("quiz"))
async def cmd_quiz(message: Message):
    user_id = message.from_user.id
    event = random.choice(HISTORY_EVENTS)

    user_sessions[user_id] = {
        "event": event,
        "score": user_sessions.get(user_id, {}).get("score", 0),
        "username": message.from_user.username or message.from_user.first_name or f"User_{user_id}"
    }

    kb = get_quiz_keyboard(event)
    quiz_msg = (
        f"⏳ **Раунд ChronoQuiz**\n\n"
        f"🏛 **Событие:** *{event['name']}*\n"
        f"📍 **Локация:** {event['loc']}\n"
        f"📖 **Описание:** {event['desc']}\n\n"
        f"В каком году произошло это событие? Выберите вариант ниже или отправьте число сообщением:"
    )
    await message.answer(quiz_msg, reply_markup=kb, parse_mode="Markdown")


@dp.callback_query(F.data.startswith("guess_"))
async def handle_quiz_callback(call: CallbackQuery):
    parts = call.data.split("_")
    event_id = int(parts[1])
    guessed_year = int(parts[2])
    user_id = call.from_user.id

    event = next((ev for ev in HISTORY_EVENTS if ev["id"] == event_id), None)
    if not event:
        await call.answer("Событие не найдено.", show_alert=True)
        return

    # User guessed coordinates default to vicinity for inline buttons
    res = compute_quiz_score(
        actual_year=event["year"],
        guessed_year=guessed_year,
        actual_lat=event["lat"],
        actual_lon=event["lon"],
        guessed_lat=event["lat"],
        guessed_lon=event["lon"]
    )

    pts = res["score"]
    username = call.from_user.username or call.from_user.first_name or f"User_{user_id}"
    leaderboard[f"@{username}"] = leaderboard.get(f"@{username}", 0) + pts

    actual_formatted = f"{abs(event['year'])} до н.э." if event['year'] < 0 else f"{event['year']} г. н.э."
    guessed_formatted = f"{abs(guessed_year)} до н.э." if guessed_year < 0 else f"{guessed_year} г. н.э."

    result_text = (
        f"🎯 **РЕЗУЛЬТАТ РАУНДА: [{res['rating']}]**\n\n"
        f"• Ваш ответ: `{guessed_formatted}`\n"
        f"• Правильный год: `{actual_formatted}`\n"
        f"• Погрешность: {res['year_delta']} лет\n"
        f"🏆 **Начислено очков:** +{pts}\n"
        f"Общий счет: {leaderboard[f'@{username}']} очков.\n\n"
        f"Для следующего раунда нажмите /quiz!"
    )

    await call.message.edit_text(result_text, parse_mode="Markdown")
    await call.answer(f"+{pts} очков!")


@dp.message(F.text.regexp(r'^-?\d+$'))
async def handle_direct_year_text(message: Message):
    user_id = message.from_user.id
    if user_id not in user_sessions or "event" not in user_sessions[user_id]:
        await message.answer("Сначала запустите раунд командой /quiz!")
        return

    event = user_sessions[user_id]["event"]
    guessed_year = int(message.text.strip())

    res = compute_quiz_score(
        actual_year=event["year"],
        guessed_year=guessed_year,
        actual_lat=event["lat"],
        actual_lon=event["lon"],
        guessed_lat=event["lat"],
        guessed_lon=event["lon"]
    )

    pts = res["score"]
    username = message.from_user.username or message.from_user.first_name or f"User_{user_id}"
    leaderboard[f"@{username}"] = leaderboard.get(f"@{username}", 0) + pts

    actual_formatted = f"{abs(event['year'])} до н.э." if event['year'] < 0 else f"{event['year']} г. н.э."

    result_text = (
        f"🎯 **ПРЯМОЙ ОТВЕТ: [{res['rating']}]**\n\n"
        f"• Вы назвали: `{guessed_year}`\n"
        f"• Реальный год: `{actual_formatted}`\n"
        f"• Погрешность: {res['year_delta']} лет\n"
        f"🏆 **Начислено очков:** +{pts}\n\n"
        f"Сыграть еще: /quiz"
    )
    await message.answer(result_text, parse_mode="Markdown")


@dp.message(Command("leaderboard"))
async def cmd_leaderboard(message: Message):
    sorted_board = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)[:10]
    lines = ["🏆 **ТОП ИССЛЕДОВАТЕЛЕЙ ИСТОРИИ (CHRONOQUIZ)**\n"]
    medals = ["🥇", "🥈", "🥉", "4.", "5.", "6.", "7.", "8.", "9.", "10."]

    for idx, (uname, score) in enumerate(sorted_board):
        m = medals[idx] if idx < len(medals) else f"{idx+1}."
        lines.append(f"{m} {uname} — **{score}** очков")

    await message.answer("\n".join(lines), parse_mode="Markdown")


async def run_bot():
    bot = Bot(token=TOKEN)
    logger.info("Starting ChronoQuiz Bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_bot())
