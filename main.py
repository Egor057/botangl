import asyncio
import datetime
import json
import logging
import os
import time
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    PreCheckoutQuery,
    ReplyKeyboardMarkup,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

TOKEN = "9084719584:AAHwV1IsqQGThsoHCJw_sCkvz5ayfnCvMD8"
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

DB_FILE = "users_database.json"

def load_database():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Ошибка загрузки базы данных: {e}")
    return {}

def save_database():
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(USERS_DB, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Ошибка сохранения базы данных: {e}")

USERS_DB = load_database()

def get_user(user_id: int):
    str_id = str(user_id)
    if str_id not in USERS_DB:
        USERS_DB[str_id] = {
            "is_premium": False,
            "level": "A1",
            "points": 0,
            "words": 0,
            "tests": 0,
            "refs": 0,
            "streak": 1,
            "last_word_time": 0,
            "reg_date": datetime.date.today().strftime("%d.%m.%Y"),
        }
        save_database()
    return USERS_DB[str_id]

try:
    import vocabulary_a1
    import vocabulary_a2
    import vocabulary_adventure
    import vocabulary_b1
    import vocabulary_b2
    import vocabulary_c1
    import vocabulary_chat_simulator
    import vocabulary_detective
    import vocabulary_grammar
    import vocabulary_homework
    import vocabulary_premium
    import vocabulary_radin_b1
    import vocabulary_radin_b2
    import vocabulary_radin_c1
    import vocabulary_reading
    import vocabulary_sprint_a1
    import vocabulary_sprint_a2
    import vocabulary_sprint_b1
    import vocabulary_sprint_b2
    import vocabulary_sprint_c1
    import vocabulary_travel
except ImportError as e:
    logger.warning(f"Предупреждение при импорте модуля: {e}")


import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        pass

threading.Thread(target=lambda: HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 10000))), SimpleHandler).serve_forever(), daemon=True).start()

# Простейший HTTP-сервер для удержания сервера бодрствующим
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")
    def log_message(self, format, *args):
        pass # Отключаем лишний спам в логах

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()


 
# Запускаем веб-сервер в отдельном потоке, чтобы он не мешал боту
threading.Thread(target=run_server, daemon=True).start()
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📚 Учить слова"),
                KeyboardButton(text="🎯 Тесты и Блиц"),
            ],
            [
                KeyboardButton(text="📖 Чтение текстов"),
                KeyboardButton(text="🎮 Игры и Чат-бот"),
            ],
            [
                KeyboardButton(text="🏆 Лидерборд (500⭐)"),
                KeyboardButton(text="👤 Профиль"),
            ],
            [
                KeyboardButton(text="⭐ Купить Премиум *")
            ],
        ],
        resize_keyboard=True,
    )

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    get_user(user_id)

    args = message.text.split()
    if len(args) > 1 and args[1].startswith("ref_"):
        try:
            referrer_id = int(args[1].replace("ref_", ""))
            if referrer_id != user_id and str(referrer_id) in USERS_DB:
                USERS_DB[str(referrer_id)]["refs"] += 1
                USERS_DB[str(referrer_id)]["points"] += 100
                save_database()
                await bot.send_message(
                    referrer_id,
                    "🎉 По твоей реферальной ссылке перешел новый ученик!\n🎁 Тебе начислено +100 очков в лидерборде 🚀",
                )
        except ValueError:
            pass

    welcome_text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "🚀 Добро пожаловать в элитный образовательный бот по английскому языку.\n"
        "🔥 **Участвуй в битве за призы!** Приглашай друзей, учи слова из твоих баз и забирай награды:\n"
        "🥇 **1 место:** Уникальная NFT за 500 звезд!\n"
        "🥈 **2 и 🥉 3 места:** Премиум-доступ на 1 месяц бесплатно!\n\n"
        "Выбери нужный раздел в меню на клавиатуре снизу 👇"
    )
    await message.answer(
        welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown"
    )

@dp.message(F.text == "🏠 Главное меню")
async def main_menu(message: types.Message):
    await message.answer(
        "🏠 Вы вернулись в главное меню:", reply_markup=get_main_keyboard()
    )

@dp.message(F.text == "📚 Учить слова")
async def learn_words_handler(message: types.Message):
    user_data = get_user(message.from_user.id)
    status = "⭐ Премиум активен" if user_data["is_premium"] else "🔒 Базовый"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🟢 Уровень A1 (Базовый)", callback_data="word_a1")],
            [InlineKeyboardButton(text="🟢 Уровень A2 (Элементарный)", callback_data="word_a2")],
            [InlineKeyboardButton(text="⭐ Уровень B1 (Продвинутый) *", callback_data="word_b1")],
            [InlineKeyboardButton(text="⭐ Уровень B2 (Высокий) *", callback_data="word_b2")],
            [InlineKeyboardButton(text="⭐ Уровень C1 (Профи + 2k слов) *", callback_data="word_c1")],
            [InlineKeyboardButton(text="⚡ Словарный спринт (A1)", callback_data="word_sprint_a1")],
            [InlineKeyboardButton(text="⚡ Словарный спринт (B1) *", callback_data="word_sprint_b1")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")],
        ]
    )
    await message.answer(
        f"📚 **Словарный тренажер** (Модули на 300+ слов)\nТвой статус: {status}\n\nВыбери уровень для тренировки:",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

@dp.callback_query(F.data.startswith("word_"))
async def callback_words(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user(user_id)
    data_type = callback.data.replace("word_", "")

    current_time = time.time()
    last_time = user_data.get("last_word_time", 0)
    if current_time - last_time < 3:
        remaining = int(3 - (current_time - last_time)) + 1
        await callback.answer(
            f"⏳ Нельзя так быстро! Подождите {remaining} сек. перед следующей карточкой.",
            show_alert=True,
        )
        return

    user_data["last_word_time"] = current_time

    if data_type in ["b1", "b2", "c1", "sprint_b1"] and not user_data["is_premium"]:
        await callback.answer(
            "⭐ Этот уровень доступен только по Премиум подписке!", show_alert=True
        )
        return

    user_data["words"] += 5
    user_data["points"] += 50
    save_database()

    target_words = 300
    current_words = user_data["words"]
    percent = min(100, int((current_words / target_words) * 100))
    filled = int(percent / 10)
    progress_bar = "█" * filled + "░" * (10 - filled)

    content = f"📖 Урок уровня **{data_type.upper()}** загружен из твоего модуля!"
    try:
        if data_type == "a1" and "vocabulary_a1" in globals():
            content = vocabulary_a1.get_lesson()
        elif data_type == "a2" and "vocabulary_a2" in globals():
            content = vocabulary_a2.get_lesson()
        elif data_type == "b1" and "vocabulary_b1" in globals():
            content = vocabulary_b1.get_lesson()
        elif data_type == "b2" and "vocabulary_b2" in globals():
            content = vocabulary_b2.get_lesson()
        elif data_type == "c1" and "vocabulary_c1" in globals():
            content = vocabulary_c1.get_lesson()
        elif data_type == "sprint_a1" and "vocabulary_sprint_a1" in globals():
            content = vocabulary_sprint_a1.get_sprint()
        elif data_type == "sprint_b1" and "vocabulary_sprint_b1" in globals():
            content = vocabulary_sprint_b1.get_sprint()
    except Exception as e:
        logger.error(f"Ошибка вызова модуля словаря: {e}")

    await callback.message.edit_text(
        f"✅ **Тренировка лексики ({data_type.upper()}):**\n\n{content}\n\n"
        f"📊 **Прогресс:** {current_words}/{target_words} слов ({percent}%)\n"
        f"[{progress_bar}]\n\n🚀 +50 очков зачислено в рейтинг!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="⬅️ К выбору уровней", callback_data="back_words"
                )
            ]]
        ),
        parse_mode="Markdown",
    )
    await callback.answer()

@dp.callback_query(F.data == "back_words")
async def back_to_words(callback: types.CallbackQuery):
    await callback.message.delete()
    await learn_words_handler(callback.message)

@dp.message(F.text == "🎯 Тесты и Блиц")
async def tests_handler(message: types.Message):
    user_data = get_user(message.from_user.id)
    user_data["tests"] += 1
    user_data["points"] += 25
    save_database()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="A) Apple", callback_data="test_wrong"),
                InlineKeyboardButton(text="B) Success", callback_data="test_correct"),
            ],
            [
                InlineKeyboardButton(text="C) Window", callback_data="test_wrong"),
                InlineKeyboardButton(text="D) Running", callback_data="test_wrong"),
            ],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")],
        ]
    )
    await message.answer(
        "🎯 **Блиц-тест на словарный запас:**\n\nКак правильно переводится слово *«Успех»*?",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

@dp.callback_query(F.data.startswith("test_"))
async def callback_test(callback: types.CallbackQuery):
    if callback.data == "test_correct":
        await callback.answer("🎉 Абсолютно верно! +25 очков", show_alert=True)
    else:
        await callback.answer(
            "❌ Неверно. Правильный вариант: Success.", show_alert=True
        )
    await callback.message.edit_text(
        "🎯 Блиц-тест завершен!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")]
            ]
        ),
    )

@dp.message(F.text == "📖 Чтение текстов")
async def reading_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Истории и Статьи", callback_data="read_stories")],
            [InlineKeyboardButton(text="✈️ Путешествия (Базовые)", callback_data="read_travel")],
            [InlineKeyboardButton(text="⭐ VIP-Путешествия (Премиум) *", callback_data="read_prem_travel")],
            [InlineKeyboardButton(text="📰 Радио-материалы (Radin)", callback_data="read_radin")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")],
        ]
    )
    await message.answer(
        "📖 **Библиотека текстов и материалов:**",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

@dp.callback_query(F.data == "read_stories")
async def read_stories_cb(callback: types.CallbackQuery):
    text = "📖 **Статья:** Загрузка из модуля..."
    try:
        if "vocabulary_reading" in globals() and hasattr(vocabulary_reading, "get_text"):
            text = vocabulary_reading.get_text()
    except Exception:
        pass
    user_data = get_user(callback.from_user.id)
    user_data["points"] += 30
    save_database()
    await callback.message.edit_text(
        f"{text}\n\n✅ Материал прочитан! +30 очков.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")
            ]]
        ),
        parse_mode="Markdown",
    )
    await callback.answer()

@dp.callback_query(F.data == "read_travel")
async def read_travel_cb(callback: types.CallbackQuery):
    text = "✈️ **Путешествия:** Загрузка из модуля..."
    try:
        if "vocabulary_travel" in globals() and hasattr(vocabulary_travel, "get_dialog"):
            text = vocabulary_travel.get_dialog()
    except Exception:
        pass
    user_data = get_user(callback.from_user.id)
    user_data["points"] += 30
    save_database()
    await callback.message.edit_text(
        f"{text}\n\n✅ Пройдено! +30 очков.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")
            ]]
        ),
        parse_mode="Markdown",
    )
    await callback.answer()

@dp.callback_query(F.data == "read_prem_travel")
async def read_prem_travel_cb(callback: types.CallbackQuery):
    user_data = get_user(callback.from_user.id)
    if not user_data["is_premium"]:
        await callback.answer(
            "⭐ Элитные истории про путешествия доступны только по Премиум подписке!",
            show_alert=True,
        )
        return

    prem_text = "⭐ **VIP-Путешествия:** Загрузка из премиум-модуля..."
    try:
        if "vocabulary_преmium" in globals() and hasattr(vocabulary_преmium, "get_vip_travel"):
            prem_text = vocabulary_преmium.get_vip_travel()
    except Exception:
        pass

    user_data["points"] += 75
    save_database()
    await callback.message.edit_text(
        f"{prem_text}\n\n✅ VIP-материал проработан! +75 очков зачислено 🚀",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")
            ]]
        ),
        parse_mode="Markdown",
    )
    await callback.answer()

@dp.callback_query(F.data == "read_radin")
async def read_radin_cb(callback: types.CallbackQuery):
    text = "📰 **Радио-материал:** Загрузка из модуля..."
    try:
        if "vocabulary_radin_b1" in globals() and hasattr(vocabulary_radin_b1, "get_material"):
            text = vocabulary_radin_b1.get_material()
    except Exception:
        pass
    user_data = get_user(callback.from_user.id)
    user_data["points"] += 35
    save_database()
    await callback.message.edit_text(
        f"{text}\n\n✅ Прочитано! +35 очков.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")
            ]]
        ),
        parse_mode="Markdown",
    )
    await callback.answer()

@dp.message(F.text == "🎮 Игры и Чат-бот")
async def games_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔍 Детективное расследование *", callback_data="game_detective")],
            [InlineKeyboardButton(text="🗺️ Приключение (Adventure)", callback_data="game_adventure")],
            [InlineKeyboardButton(text="💬 Симулятор чата", callback_data="game_chat")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")],
        ]
    )
    await message.answer(
        "🎮 **Игровой зал и практика:**",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

@dp.callback_query(F.data == "game_detective")
async def detective_game(callback: types.CallbackQuery):
    user_data = get_user(callback.from_user.id)
    if not user_data["is_premium"]:
        await callback.answer(
            "⭐ Детективный режим доступен только по Премиум подписке!",
            show_alert=True,
        )
        return
    det_text = "🔍 **Детективное расследование:** Загрузка из модуля..."
    try:
        if "vocabulary_detective" in globals() and hasattr(vocabulary_detective, "get_case"):
            det_text = vocabulary_detective.get_case()
    except Exception:
        pass
    await callback.message.edit_text(
        det_text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")
            ]]
        ),
        parse_mode="Markdown",
    )
    await callback.answer()

@dp.callback_query(F.data == "game_adventure")
async def adventure_game(callback: types.CallbackQuery):
    adv_text = "🗺️ **Приключение:** Загрузка из модуля..."
    try:
        if "vocabulary_adventure" in globals() and hasattr(vocabulary_adventure, "get_story"):
            adv_text = vocabulary_adventure.get_story()
    except Exception:
        pass
    await callback.message.edit_text(
        adv_text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")
            ]]
        ),
        parse_mode="Markdown",
    )
    await callback.answer()

@dp.callback_query(F.data == "game_chat")
async def chat_sim_game(callback: types.CallbackQuery):
    chat_text = "💬 **Симулятор чата:** Загрузка из модуля..."
    try:
        if "vocabulary_chat_simulator" in globals() and hasattr(vocabulary_chat_simulator, "get_prompt"):
            chat_text = vocabulary_chat_simulator.get_prompt()
    except Exception:
        pass
    await callback.message.edit_text(
        chat_text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")
            ]]
        ),
        parse_mode="Markdown",
    )
    await callback.answer()

@dp.message(F.text == "🏆 Лидерборд (500⭐)")
async def leaderboard_handler(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user(user_id)
    ref_link = f"https://t.me/English_StudyyBot?start=ref_{user_id}"

    text = (
        "🏆 **Топ-10 участников битвы за призы:**\n\n"
        "1. 🥇 Alex_Coder — 4,250 очков\n"
        "2. 🥈 Sofia_En — 3,890 очков\n"
        "3. 🥉 Max_Pro — 3,450 очков\n"
        f"4. {message.from_user.first_name} (Ты) — {user_data['points']} очков\n"
        "5. CodeNinja — 2,510 очков\n\n"
        "🎁 **Призовой фонд турнира:**\n"
        "🥇 **1 место:** Уникальная NFT за 500 звезд!\n"
        "🥈 **2 место:** Премиум на 1 месяц бесплатно!\n"
        "🥉 **3 место:** Премиум на 1 месяц бесплатно!\n\n"
        "🚀 Приглашай друзей по своей реферальной ссылке (+100 очков) и побеждай!\n\n"
        f"🔗 **Твоя реферальная ссылка:**\n`{ref_link}`"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📤 Поделиться ссылкой",
                    url=(
                        "https://t.me/share/url?url="
                        + ref_link
                        + "&text=Залетай%20в%20бота,%20боремся%20за%20NFT%20и%20Премиум!%20🚀"
                    ),
                )
            ],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")],
        ]
    )
    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.message(F.text == "👤 Профиль")
async def profile_handler(message: types.Message):
    user = message.from_user
    user_data = get_user(user.id)
    ref_link = f"https://t.me/English_StudyyBot?start=ref_{user.id}"
    status = "⭐ Премиум (Активен)" if user_data["is_premium"] else "⚪ Базовый"

    target_words = 300
    current_words = user_data["words"]
    percent = min(100, int((current_words / target_words) * 100))
    filled = int(percent / 10)
    progress_bar = "█" * filled + "░" * (10 - filled)

    text = (
        f"📊 **Твой профиль и статистика:**\n\n"
        f"👤 Имя: {user.first_name}\n"
        f"💎 Статус: {status}\n"
        f"🏆 Очки рейтинга: {user_data['points']}\n"
        f"👥 Приглашено друзей: {user_data['refs']}\n"
        f"📚 Выучено карточек: {current_words}/{target_words} ({percent}%)\n"
        f"[{progress_bar}]\n"
        f"🎯 Пройдено тестов: {user_data['tests']}\n"
        f"🔥 Стрик дней: {user_data['streak']}\n"
        f"📅 Регистрация: {user_data['reg_date']}\n\n"
        f"🔗 Рефералка:\n`{ref_link}`"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏆 Открыть лидерборд", callback_data="open_lb")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")],
        ]
    )
    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(F.data == "open_lb")
async def callback_open_lb(callback: types.CallbackQuery):
    await callback.message.delete()
    await leaderboard_handler(callback.message)

@dp.message(F.text == "⚙️ Настройки")
async def settings_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📚 Домашнее задание (500 тем) *", callback_data="homework")],
            [InlineKeyboardButton(text="📖 Справочник грамматики", callback_data="grammar_ref")],
            [InlineKeyboardButton(text="⭐ О Премиум подписке", callback_data="premium_info")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")],
        ]
    )
    await message.answer(
        "⚙️ **Настройки и полезные материалы:**",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

@dp.callback_query(F.data == "homework")
async def setting_hw(callback: types.CallbackQuery):
    user_data = get_user(callback.from_user.id)
    if not user_data["is_premium"]:
        await callback.answer(
            "⭐ Домашние задания (500 тем) доступны по Премиум подписке!",
            show_alert=True,
        )
        return
    hw_text = "📚 **Домашние задания (500 тем):**"
    try:
        if "vocabulary_homework" in globals() and hasattr(vocabulary_homework, "get_topics"):
            hw_text = vocabulary_homework.get_topics()
    except Exception:
        pass
    await callback.message.edit_text(
        hw_text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")
            ]]
        ),
        parse_mode="Markdown",
    )
    await callback.answer()

@dp.callback_query(F.data == "grammar_ref")
async def setting_grammar(callback: types.CallbackQuery):
    gram_text = "📖 **Справочник грамматики:**"
    try:
        if "vocabulary_grammar" in globals() and hasattr(vocabulary_grammar, "get_rules"):
            gram_text = vocabulary_grammar.get_rules()
    except Exception:
        pass
    await callback.message.edit_text(
        gram_text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")
            ]]
        ),
        parse_mode="Markdown",
    )
    await callback.answer()

@dp.callback_query(F.data == "premium_info")
async def setting_premium_info(callback: types.CallbackQuery):
    prem_text = "⭐ **Премиум-доступ:** Открывает все модули и базы слов."
    try:
        if "vocabulary_premium" in globals() and hasattr(vocabulary_premium, "get_info"):
            prem_text = vocabulary_premium.get_info()
    except Exception:
        pass
    await callback.message.edit_text(
        prem_text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")
            ]]
        ),
        parse_mode="Markdown",
    )
    await callback.answer()

@dp.message(F.text == "⭐ Купить Премиум *")
async def premium_handler(message: types.Message):
    prices = [types.LabeledPrice(label="Премиум доступ (B1-C1 + VIP-путешествия + игры)", amount=50)]
    await message.answer_invoice(
        title="Премиум-доступ к боту",
        description="Открой продвинутый уровень B1-C1, VIP-путешествия, детективный режим, симулятор чата и 500 тем домашней работы навсегда!",
        payload="premium_access_50_stars",
        currency="XTR",
        prices=prices,
    )

@dp.pre_checkout_query()
async def pre_checkout_query_handler(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment_handler(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user(user_id)
    user_data["is_premium"] = True
    user_data["points"] += 1000
    save_database()

    await message.answer(
        "🎉 **Успешная оплата! Премиум-доступ активирован!** ⭐\n"
        "Тебе начислено +1000 очков в лидерборд.\n"
        "Все модули словарей, VIP-путешествия и детективы разблокированы!",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown",
    )

@dp.callback_query(F.data == "to_main")
async def callback_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Вы вернулись в главное меню. Используйте клавиатуру внизу 👇"
    )
    await callback.answer()

async def main():
    logger.info("🚀 Бот запущен с защитой от спама карточек и модулями словарей!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())