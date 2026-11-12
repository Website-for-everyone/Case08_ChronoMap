# АРХИТЕКТУРА И СПЕЦИФИКАЦИЯ ПРОЕКТА: ChronoMap

> **Проект:** ChronoMap (Case 08) — Интерактивная 3D-карта истории (3000 до н.э. — наши дни) & AI-Историк  
> **Клиент / Заказчик:** EdTech & Interactive Historical Media / Портфолио Даниэля Идрисова (@Idrisov_prod)  
> **Чек проекта:** 180 000 ₽ | **Срок:** 8 дней (Дедлайн: 2026-11-20)  
> **Дедлайн MVP (80%):** 2026-11-16  
> **Тип договора:** Договор СМЗ с ИП/ООО (Чек «Мой Налог»)

---

## 🛠 Технологический стек
- **Frontend / UI:** Vanilla JS, Three.js / Canvas 3D WebGL Globe, 5000-летний интерактивный скруббер временной шкалы, адаптивный дизайн (космический обсидиан #05070D, античное золото #D4AF37, небесный синий #1E3A8A)
- **Backend & Logic:** Python 3.12, FastAPI, Uvicorn, SQLite (ChronoQuiz Leaderboard), Gemini API Cascade / Knowledge Engine
- **Telegram Bot:** Aiogram 3.x, ChronoQuiz Bot («Угадай год и место»), расчет геодезических расстояний и временной дельты
- **Автоматизация & Интеграции:** AI Historian Endpoint, Global Quiz Leaderboard, Alerting to @Idrisov_prod
- **Тестирование:** Pytest, Unit & Smoke Tests

---

## 🏛 Архитектурная схема
```
[ Клиент / Браузер ] ──► [ 3D History Globe (WebGL/Canvas) ] ──► [ Timeline Scrubber (3000 BC - 2026 AD) ]
         │                                                            │
         ▼                                                            ▼
[ AI Historian Panel ] ──► [ FastAPI / Gemini Knowledge Engine ] ◄──► [ Geo-Dataset Markers ]
                                   │
                                   ▼
                [ ChronoQuiz Bot (Aiogram 3.x) & Leaderboard ]
```

---

## 🔐 Переменные окружения (.env.example)
```env
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
GEMINI_API_KEY=your_gemini_api_key_here
WEB_HOST=0.0.0.0
WEB_PORT=8008
OWNER_TG_ID=1387913438
ENVIRONMENT=production
```

---

## 🔗 Ресурсы и ссылки
- **Репозиторий GitHub:** https://github.com/Website-for-everyone/Case08_ChronoMap
- **Dev-сервер / Preview URL:** http://localhost:8008
- **Чат проекта в Telegram:** @Idrisov_prod
