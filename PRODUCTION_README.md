# CINEMATIC AI SUPERBOT - PRODUCTION READY

> A modern, professional Telegram AI bot for anime/manga post creation with ultra-premium design templates, intelligent rating system, and optional OpenAI integration.

## System Status

```
SYSTEM MODE: CINEMATIC AI SUPERBOT
DESIGN ENGINE: 15 THEMES × 30 VARIATIONS
RATING ENGINE: 100-POINT VERIFIED
AI STYLE: ACTIVE (or FALLBACK)
CHANNEL DETECTION: READY
FSM: STABLE
ERROR HANDLER: SAFE
DATABASE: INITIALIZED
PRODUCTION STATUS: READY
```

## Core Features (11 Systems)

### 1️⃣ Rating Engine V2
- **Input**: Accept numbers in any messy format (85, 90+, ~75, -20, abc)
- **Output**: Normalized 0-100 with visual stars (⭐⭐⭐⭐⭐⭐⭐⭐) and progress bar (■■■■■■■■□□)
- **Validation**: Safe parsing, no crashes, automatic clamping

### 2️⃣ Inline Design Selector V3
- **Features**: 
  - Browse designs with ◀ Prev / Next ▶ navigation
  - 🎨 Random theme selector
  - 🔥 AI Style mode
  - Live preview before confirmation
- **Storage**: Selection persisted in FSM state

### 3️⃣ 15 Premium Master Themes
Each theme includes 30 internal layout variations:
1. Neo Minimal
2. Royal Gold Frame
3. Cyber Edge
4. Glass Soft UI
5. Manga Editorial
6. Luxury Classic
7. Neon Frame
8. Card Layout
9. Prestige Outline
10. Ultra Modern
11. Elegant Serif
12. Dark Diamond
13. Hero Banner
14. Epic Showcase
15. Supreme Collector

### 4️⃣ AI Style Generator
- **Smart Mode**: Calls OpenAI API if `OPENAI_API_KEY` is set
- **Fallback Mode**: Uses local emotional hooks in 6 moods:
  - Dark, Epic, Romantic, Revenge, Fantasy, Drama
- **Output**: Cinematic captions under Telegram limits

### 5️⃣ Cinematic Caption Engine
Structure:
```
HOOK (emotional)
─────────────────
Title (centered)

Type: [content]
Rating: ⭐⭐⭐ 85/100
  ■■■■■■■■□□

#Genre1  #Genre2  #Genre3

╭──── TAVSIF ────╮
Description text
╰─────────────────╯

#hashtags
```

### 6️⃣ Channel Admin Auto-Detect
- Uses Telegram `get_chat_member()` API
- Validates bot admin status
- Checks message send permissions
- Handles forbidden errors gracefully
- Storage in SQLite

### 7️⃣ Safe Error System
- aiogram 3.x compatible `ErrorEvent` handler
- Logs all exceptions
- User-friendly error messages in Uzbek
- No crashes, graceful degradation

### 8️⃣ Database System
- Async SQLite (aiosqlite)
- Auto-initialization on startup
- Tables: users, drafts, channels, published_posts, preferences
- 100% non-blocking

### 9️⃣ Retry Logic
- Internal `_simple_retry` async helper (no external deps)
- 3 attempts with exponential backoff
- 0.5s base delay, 2x multiplier
- Works across ChannelManager and publish flows

### 🔟 Input Smart Parser
**Accepts flexible formats and normalizes:**
- Genres: "romantika drama" → ['Romantika', 'Drama']
- Chapters: "150+", "100-200", "~350" → parsed tuples
- Ratings: "85", "90+", "~75" → integers
- Auto-cleans duplicates, removes spam

### 1️⃣1️⃣ Performance
- No blocking awaits in FSM transitions
- All I/O is async
- Response time target: <300ms per user
- Handles concurrent users without freezing

## Project Structure

```
GOkuu/
├── src/
│   ├── config.py                      # .env loader + settings
│   ├── routers.py                     # FSM handlers
│   ├── states.py                      # FSM state definitions
│   ├── keyboards.py                   # Telegram keyboards
│   ├── services/
│   │   ├── database.py                # Async SQLite
│   │   ├── rating_engine.py           # 0-100 rating system
│   │   ├── input_parser.py            # Genre/chapter normalization
│   │   ├── design_engine_v7.py        # 15 premium themes
│   │   ├── design_selector.py         # Inline design picker
│   │   ├── ai_caption_generator.py    # OpenAI + fallback
│   │   ├── channel_manager.py         # Retry logic + publish
│   │   ├── channel_validator.py       # Admin detection
│   │   ├── ai_layer.py                # OpenAI wrapper
│   │   └── cinema_builder.py          # Caption composition
│   └── ui/
│       └── (UI components)
├── run.py                             # Main entry point
├── requirements.txt                   # Dependencies
├── .env                               # Configuration (BOT_TOKEN, OPENAI_API_KEY, etc.)
└── scripts/
    ├── simulate_production.py         # Full system simulation
    └── final_production_verify.py     # Verification checklist (11 systems)
```

## Installation & Setup

### 1. Install Python 3.11

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure `.env`
```env
BOT_TOKEN=your_telegram_bot_token
ADMIN_ID=your_telegram_user_id
OPENAI_API_KEY=optional_openai_key
PERSONALITY_MODE=friendly
EMOJI_LEVEL=2
DEFAULT_TEMPLATE=t01
```

### 4. Initialize database & start bot
```bash
py -3.11 run.py
```

## Dependencies

```
aiogram==3.7.0
python-dotenv==1.0.1
aiohttp>=3.8.0
openai>=1.0.0
```

**No tenacity required — internal async retry helper is used.**

## Verification

Run the production verification to check all 11 systems:

```bash
$env:PYTHONPATH = "$(Resolve-Path .)"
py -3.11 scripts/final_production_verify.py
```

Expected output:
```
SYSTEM MODE: CINEMATIC AI SUPERBOT
DESIGN ENGINE: 15 THEMES × 30 VARIATIONS
RATING ENGINE: 100-POINT VERIFIED
AI STYLE: ACTIVE
CHANNEL DETECTION: READY
FSM: STABLE
ERROR HANDLER: SAFE
DATABASE: INITIALIZED
PRODUCTION STATUS: READY
```

## Testing

Simulation with sample data:
```bash
$env:PYTHONPATH = "$(Resolve-Path .)"
py -3.11 scripts/simulate_production.py
```

## FSM Flow

1. `/start` → main menu
2. `📚 POST YARATISH` → begin creation
3. Step 1: Title (nomi)
4. Step 2: Type (turi)
5. Step 3: Rating (reyting) — accepts 0-100
6. Step 4: Status (holati)
7. Step 5: Chapters (boblar)
8. Step 6: Genres (janrlar)
9. Step 7: Description (tavsif)
10. Step 8: Media (photo/video)
11. Step 9: Design template — **inline selector with preview**
12. Step 10: Font selection
13. Confirm & publish to selected channels

## Design Templates

Each of the 15 themes automatically generates 30 layout variations.

**Example (Theme #1 - Neo Minimal):**
```
      ── KURO NO HIKARI ──
Turi: Manhwa
⭐⭐⭐⭐⭐⭐⭐⭐ 85/100
■■■■■■■■□□
Boblar: 150+
#Action   #Drama   #Romance

╭──── TAVSIF ────╮
Bir yosh qahramon va uning qorongu o'tmishi haqida epik hikoya...
╰─────────────────╯

#KuroSeries
```

## Configuration

### `.env` Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `BOT_TOKEN` | ✅ Yes | — | Telegram bot token |
| `ADMIN_ID` | No | `[]` | Admin user IDs (comma-separated) |
| `OPENAI_API_KEY` | No | — | Enable AI captions (if provided) |
| `PERSONALITY_MODE` | No | `friendly` | AI personality: professional, friendly, energetic, minimal |
| `EMOJI_LEVEL` | No | `2` | How many emojis to use: 1=minimal, 3=extreme |
| `DEFAULT_TEMPLATE` | No | `t01` | Starting template |

### Rating Input Formats

All accepted and normalized to 0-100:
- `85` → 85
- `90+` → 90
- `~75` → range 67-82
- `-20` → 0 (auto-clamp)
- `150` → 100 (auto-clamp)
- `abc` → 0 (fallback)

## Error Handling

**Telegram rate limit?** - Exponential backoff (up to 3 attempts)
**Invalid channel?** - Graceful fallback, user-friendly message
**OpenAI quota exceeded?** - Switch to fallback cinematic generator
**Database error?** - Logged but bot continues running

## Performance Targets

- **Response time**: <300ms per message
- **Concurrent users**: 100+ simultaneously
- **Memory**: <200MB baseline
- **No blocking awaits**: ✅ Verified

## Production Checklist

- [x] aiogram 3.x compatible
- [x] Zero external retry libraries (internal async retry helper)
- [x] Async database (aiosqlite)
- [x] Safe error handler
- [x] No unawaited coroutines
- [x] All imports verified (import re, etc.)
- [x] 15 premium design templates
- [x] 100-point rating system
- [x] AI caption generator (active + fallback)
- [x] Channel admin detection
- [x] Rating validation with messy input support
- [x] Inline design selector with preview
- [x] FSM transitions clean and logged

## License

Private use only.

---

**Build Date**: February 21, 2026  
**Status**: Production Ready  
**Version**: 1.0.0 (Enterprise)
