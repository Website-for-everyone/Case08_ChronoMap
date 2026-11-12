# ChronoMap (Case 08) — Interactive 3D History Globe & AI Historian

> **5,000-Year Historical Timeline (3000 BCE – Present) • 3D WebGL Globe • Contextual AI Historian • ChronoQuiz Telegram Bot**

![3D Globe](https://img.shields.io/badge/Aesthetic-Cosmic%20Obsidian%20%26%20Gold-D4AF37?style=flat-square)
![Timeline](https://img.shields.io/badge/Epoch-3000%20BCE%20--%202026%20CE-1E3A8A?style=flat-square)
![Telegram Quiz](https://img.shields.io/badge/Aiogram%203.x-ChronoQuiz%20Bot-blue?style=flat-square)

---

## 🎯 Features
1. **Interactive 3D Earth Globe:** WebGL/Canvas spherical globe with continents, latitude/longitude grid, rotation and zoom controls, starfield particle galaxy.
2. **5,000-Year Temporal Scrubber:**
   - Smooth continuous scrubbing across 3000 BCE to 2026 CE.
   - Snap-to-epoch presets:
     - **Bronze Age** (3000–1200 BCE)
     - **Classical Antiquity** (800 BCE–500 CE)
     - **Middle Ages** (500–1500 CE)
     - **Renaissance & Exploration** (1400–1750 CE)
     - **Industrial Revolution** (1760–1914 CE)
     - **Modern & Space Age** (1914–2026 CE)
3. **Geo-Dataset Milestone Markers:** Interactive pins rendered directly on the globe surface with geographic coordinates, empire affiliations, artifact imagery, and summaries.
4. **Contextual AI Historian Panel:** Ask any historical question contextualized to the currently selected year and region; receives scholarly responses from the backend engine.
5. **ChronoQuiz Telegram Bot (Угадай год и место):**
   - Presents historical events and artwork.
   - Users guess the year and location coordinates.
   - Real-time scoring using geographical geodesic distance & year delta formulas.
   - Persistent SQLite leaderboard.

---

## 🚀 Quick Start

### 1. Web & API Server
```bash
cd Case08_ChronoMap
pip install -r requirements.txt
python api/server.py
```
Open [http://localhost:8008](http://localhost:8008) in your browser.

### 2. Telegram Bot
```bash
python bot/bot.py
```

### 3. Run Tests
```bash
pytest tests/test_chronomap.py -v
```
