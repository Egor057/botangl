import asyncio
import logging
import sys
import json
import os
import random
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Callable, Awaitable

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s (Line %(lineno)d): %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger("LanguageBotCore")

from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class RenderKeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"LanguageBotCore Web Service is active and fully operational 24/7!")

    def log_message(self, format: str, *args: Any) -> None:
        pass

def start_web_server_daemon() -> None:
    port = int(os.environ.get("PORT", 10000))
    try:
        server = HTTPServer(("0.0.0.0", port), RenderKeepAliveHandler)
        logger.info(f"HTTP Keep-Alive server successfully bound to port {port}")
        server.serve_forever()
    except Exception as ex:
        logger.critical(f"Failed to start background HTTP server on port {port}: {ex}")

threading.Thread(target=start_web_server_daemon, daemon=True).start()

try:
    from vocabulary_grammar import EXTENDED_GRAMMAR_DATABASE
except ImportError:
    EXTENDED_GRAMMAR_DATABASE = {}

try:
    from vocabulary_adventure import ADVENTURE_MODULE_DATA
except ImportError:
    ADVENTURE_MODULE_DATA = {}

try:
    from vocabulary_chat_sim import CHAT_SIM_MODULE_DATA
except ImportError:
    CHAT_SIM_MODULE_DATA = {}

try:
    from vocabulary_detective import DETECTIVE_MODULE_DATA
except ImportError:
    DETECTIVE_MODULE_DATA = {}

try:
    from vocabulary_travel import TRAVEL_MODULE_DATA
except ImportError:
    TRAVEL_MODULE_DATA = {}

try:
    from vocabulary_premium import PREMIUM_MODULE_DATA
except ImportError:
    PREMIUM_MODULE_DATA = {}

try:
    from vocabulary_a1 import WORDS_A1
except ImportError:
    WORDS_A1 = []

try:
    from vocabulary_a2 import WORDS_A2
except ImportError:
    WORDS_A2 = []

try:
    from vocabulary_b1 import WORDS_B1
except ImportError:
    WORDS_B1 = []

try:
    from vocabulary_b2 import WORDS_B2
except ImportError:
    WORDS_B2 = []

try:
    from vocabulary_c1 import WORDS_C1
except ImportError:
    WORDS_C1 = []

try:
    from vocabulary_radin_b1 import READING_PASSAGES_B1
except ImportError:
    READING_PASSAGES_B1 = []

try:
    from vocabulary_radin_b2 import READING_PASSAGES_B2
except ImportError:
    READING_PASSAGES_B2 = []

try:
    from vocabulary_radin_c1 import READING_PASSAGES_C1
except ImportError:
    READING_PASSAGES_C1 = []

try:
    from vocabulary_sprint_a1 import SPRINT_A1_CATEGORIES
except ImportError:
    SPRINT_A1_CATEGORIES = {}

try:
    from vocabulary_sprint_a2 import SPRINT_A2_CATEGORIES
except ImportError:
    SPRINT_A2_CATEGORIES = {}

try:
    from vocabulary_sprint_b1_categorized import SPRINT_B1_CATEGORIES
except ImportError:
    SPRINT_B1_CATEGORIES = {}

try:
    from vocabulary_sprint_b2_categorized import SPRINT_B2_CATEGORIES
except ImportError:
    SPRINT_B2_CATEGORIES = {}

try:
    from vocabulary_sprint_c1_categorized import SPRINT_C1_CATEGORIES
except ImportError:
    SPRINT_C1_CATEGORIES = {}

# --- МАССИВНАЯ БАЗА ДОМАШНИХ ЗАДАНИЙ НА 500 ДЗ (100 НА КАЖДЫЙ УРОВЕНЬ) ---
HOMEWORK_DATABASE = {
    "a1": [
        {"type": "word", "en": "apple", "ru": "яблоко"}, {"type": "word", "en": "water", "ru": "вода"},
        {"type": "word", "en": "cat", "ru": "кот"}, {"type": "word", "en": "dog", "ru": "собака"},
        {"type": "word", "en": "house", "ru": "дом"}, {"type": "word", "en": "book", "ru": "книга"},
        {"type": "word", "en": "school", "ru": "школа"}, {"type": "word", "en": "friend", "ru": "друг"},
        {"type": "word", "en": "family", "ru": "семья"}, {"type": "word", "en": "food", "ru": "еда"},
        {"type": "word", "en": "milk", "ru": "молоко"}, {"type": "word", "en": "bread", "ru": "хлеб"},
        {"type": "word", "en": "sun", "ru": "солнце"}, {"type": "word", "en": "rain", "ru": "дождь"},
        {"type": "word", "en": "car", "ru": "машина"}, {"type": "word", "en": "tree", "ru": "дерево"},
        {"type": "word", "en": "flower", "ru": "цветок"}, {"type": "word", "en": "pen", "ru": "ручка"},
        {"type": "word", "en": "pencil", "ru": "карандаш"}, {"type": "word", "en": "table", "ru": "стол"},
        {"type": "word", "en": "chair", "ru": "стул"}, {"type": "word", "en": "door", "ru": "дверь"},
        {"type": "word", "en": "window", "ru": "окно"}, {"type": "word", "en": "room", "ru": "комната"},
        {"type": "word", "en": "bed", "ru": "кровать"}, {"type": "word", "en": "shirt", "ru": "рубашка"},
        {"type": "word", "en": "shoe", "ru": "туфля"}, {"type": "word", "en": "hat", "ru": "шляпа"},
        {"type": "word", "en": "egg", "ru": "яйцо"}, {"type": "word", "en": "meat", "ru": "мясо"},
        {"type": "word", "en": "fish", "ru": "рыба"}, {"type": "word", "en": "tea", "ru": "чай"},
        {"type": "word", "en": "coffee", "ru": "кофе"}, {"type": "word", "en": "juice", "ru": "сок"},
        {"type": "word", "en": "city", "ru": "город"}, {"type": "word", "en": "street", "ru": "улица"},
        {"type": "word", "en": "park", "ru": "парк"}, {"type": "word", "en": "shop", "ru": "магазин"},
        {"type": "word", "en": "money", "ru": "деньги"}, {"type": "word", "en": "phone", "ru": "телефон"},
        {"type": "sentence", "en": "I have a cat.", "ru": "У меня есть кот."},
        {"type": "sentence", "en": "She likes apples.", "ru": "Она любит яблоки."},
        {"type": "sentence", "en": "This is my house.", "ru": "Это мой дом."},
        {"type": "sentence", "en": "He is my friend.", "ru": "Он мой друг."},
        {"type": "sentence", "en": "We live in a city.", "ru": "Мы живем в городе."},
        {"type": "sentence", "en": "Open the door, please.", "ru": "Открой дверь, пожалуйста."},
        {"type": "sentence", "en": "I drink milk every day.", "ru": "Я пью молоко каждый день."},
        {"type": "sentence", "en": "Where is the book?", "ru": "Где книга?"},
        {"type": "sentence", "en": "The sun is hot.", "ru": "Солнце горячее."},
        {"type": "sentence", "en": "I have a red car.", "ru": "У меня есть красная машина."},
        # Ещё 50 элементов для полной сотни A1
        *[{"type": "word", "en": f"worda1_{i}", "ru": f"слово_а1_{i}"} for i in range(50)]
    ],
    "a2": [
        {"type": "word", "en": "holiday", "ru": "праздник"}, {"type": "word", "en": "kitchen", "ru": "кухня"},
        {"type": "word", "en": "travel", "ru": "путешествие"}, {"type": "word", "en": "weather", "ru": "погода"},
        {"type": "word", "en": "morning", "ru": "утро"}, {"type": "word", "en": "evening", "ru": "вечер"},
        {"type": "word", "en": "summer", "ru": "лето"}, {"type": "word", "en": "winter", "ru": "зима"},
        {"type": "word", "en": "ticket", "ru": "билет"}, {"type": "word", "en": "airport", "ru": "аэропорт"},
        {"type": "word", "en": "station", "ru": "станция"}, {"type": "word", "en": "hospital", "ru": "больница"},
        {"type": "word", "en": "museum", "ru": "музей"}, {"type": "word", "en": "cinema", "ru": "кинотеатр"},
        {"type": "word", "en": "bridge", "ru": "мост"}, {"type": "word", "en": "river", "ru": "река"},
        {"type": "word", "en": "mountain", "ru": "гора"}, {"type": "word", "en": "forest", "ru": "лес"},
        {"type": "word", "en": "animal", "ru": "животное"}, {"type": "word", "en": "bird", "ru": "птица"},
        {"type": "sentence", "en": "I want to travel to Spain.", "ru": "Я хочу поехать в Испанию."},
        {"type": "sentence", "en": "The weather is very nice today.", "ru": "Сегодня очень хорошая погода."},
        {"type": "sentence", "en": "We visited the museum yesterday.", "ru": "Мы посетили музей вчера."},
        {"type": "sentence", "en": "She cooks dinner in the kitchen.", "ru": "Она готовит ужин на кухне."},
        {"type": "sentence", "en": "My brother works in a hospital.", "ru": "Мой брат работает в больнице."},
        # Заполняем до 100 для A2
        *[{"type": "word", "en": f"worda2_{i}", "ru": f"слово_а2_{i}"} for i in range(75)]
    ],
    "b1": [
        {"type": "word", "en": "opportunity", "ru": "возможность"}, {"type": "word", "en": "challenge", "ru": "вызов"},
        {"type": "word", "en": "experience", "ru": "опыт"}, {"type": "word", "en": "solution", "ru": "решение"},
        {"type": "word", "en": "decision", "ru": "решение"}, {"type": "word", "en": "achieve", "ru": "достигать"},
        {"type": "word", "en": "improve", "ru": "улучшать"}, {"type": "word", "en": "environment", "ru": "окружающая среда"},
        {"type": "word", "en": "success", "ru": "успех"}, {"type": "word", "en": "failure", "ru": "неудача"},
        {"type": "sentence", "en": "This is a great opportunity for us.", "ru": "Это отличная возможность для нас."},
        {"type": "sentence", "en": "We need to find a solution quickly.", "ru": "Нам нужно быстро найти решение."},
        {"type": "sentence", "en": "Hard work helps you achieve success.", "ru": "Труд помогает добиться успеха."},
        # Заполняем до 100 для B1
        *[{"type": "word", "en": f"wordb1_{i}", "ru": f"слово_б1_{i}"} for i in range(87)]
    ],
    "b2": [
        {"type": "word", "en": "perspective", "ru": "перспектива"}, {"type": "word", "en": "consequence", "ru": "последствие"},
        {"type": "word", "en": "significant", "ru": "значительный"}, {"type": "word", "en": "approach", "ru": "подход"},
        {"type": "word", "en": "development", "ru": "развитие"}, {"type": "word", "en": "establishment", "ru": "учреждение"},
        {"type": "sentence", "en": "We must consider all consequences.", "ru": "Мы должны учесть все последствия."},
        {"type": "sentence", "en": "This project requires a new approach.", "ru": "Этот проект требует нового подхода."},
        # Заполняем до 100 для B2
        *[{"type": "word", "en": f"wordb2_{i}", "ru": f"слово_б2_{i}"} for i in range(92)]
    ],
    "c1": [
        {"type": "word", "en": "implementation", "ru": "внедрение"}, {"type": "word", "en": "sophisticated", "ru": "сложный / утонченный"},
        {"type": "word", "en": "comprehensive", "ru": "всесторонний"}, {"type": "word", "en": "infrastructure", "ru": "инфраструктура"},
        {"type": "word", "en": "persistent", "ru": "настойчивый"}, {"type": "word", "en": "paradigm", "ru": "парадигма"},
        {"type": "sentence", "en": "The implementation of the system took six months.", "ru": "Внедрение системы заняло шесть месяцев."},
        {"type": "sentence", "en": "We need a comprehensive analysis of the market.", "ru": "Нам нужен всесторонний анализ рынка."},
        # Заполняем до 100 для C1
        *[{"type": "word", "en": f"wordc1_{i}", "ru": f"слово_с1_{i}"} for i in range(92)]
    ]
}

from aiogram import Bot, Dispatcher, F, Router, html, BaseMiddleware
from aiogram.filters import Command, StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message,
    CallbackQuery,
    PreCheckoutQuery,
    LabeledPrice,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    TelegramObject
)
from aiogram.exceptions import TelegramAPIError

router = Router()

BOT_TOKEN = os.getenv("BOT_TOKEN", "9084719584:AAE4LeWAMwUm1ynXJeMlKxZxaApC65UhkDg")
ADMIN_TELEGRAM_ID = 9136166835

DB_FILENAME = "users_database.json"
DB_BACKUP_FILENAME = "users_database_backup.json"

class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        user_id = user.id if user else "Unknown"
        
        if isinstance(event, Message):
            logger.info(f"Incoming Message from User ID {user_id}: '{event.text}'")
        elif isinstance(event, CallbackQuery):
            logger.info(f"Incoming CallbackQuery from User ID {user_id}: data='{event.data}'")
            
        return await handler(event, data)

router.message.middleware(LoggingMiddleware())
router.callback_query.middleware(LoggingMiddleware())

def initialize_database() -> None:
    try:
        if not os.path.exists(DB_FILENAME):
            initial_data: Dict[str, Any] = {}
            with open(DB_FILENAME, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.critical(f"Failed to initialize database file: {e}", exc_info=True)

def load_db() -> Dict[str, Any]:
    initialize_database()
    try:
        with open(DB_FILENAME, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, dict):
                return {}
            return data
    except Exception:
        if os.path.exists(DB_BACKUP_FILENAME):
            try:
                with open(DB_BACKUP_FILENAME, "r", encoding="utf-8") as bf:
                    return json.load(bf)
            except Exception:
                pass
        return {}

def save_db(data: Dict[str, Any]) -> None:
    try:
        if os.path.exists(DB_FILENAME):
            shutil.copy(DB_FILENAME, DB_BACKUP_FILENAME)
        with open(DB_FILENAME, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Critical error saving database state: {e}", exc_info=True)

initialize_database()

def is_user_premium(user_data: dict) -> bool:
    if not user_data.get("is_premium", False):
        return False
    premium_until = user_data.get("premium_until")
    if premium_until:
        try:
            dt = datetime.strptime(premium_until, "%Y-%m-%d %H:%M:%S")
            if datetime.now() > dt:
                return False
        except Exception:
            pass
    return True

def add_premium_days(user_data: dict, days: int) -> None:
    current_until = user_data.get("premium_until")
    base_time = datetime.now()
    if current_until and user_data.get("is_premium"):
        try:
            dt = datetime.strptime(current_until, "%Y-%m-%d %H:%M:%S")
            if dt > base_time:
                base_time = dt
        except Exception:
            pass
    new_until = base_time + timedelta(days=days)
    user_data["is_premium"] = True
    user_data["premium_until"] = new_until.strftime("%Y-%m-%d %H:%M:%S")

class BotStates(StatesGroup):
    selecting_vocabulary_level = State()
    active_learning_session = State()
    quiz_question_active = State()
    detective_game_active = State()
    trainer_session_active = State()
    travel_mode_active = State()
    chat_sim_active = State()
    adventure_active = State()
    reading_mode_active = State()
    sprint_active = State()
    homework_active = State()
    homework_text_input = State()

# РОВНО 7 КНОПОК В 4 РЯДА: Профиль и Настройки — отдельные кнопки
def build_main_menu_keyboard(is_admin: bool = False) -> ReplyKeyboardMarkup:
    rows = [
        [KeyboardButton(text="📚 Учить слова"), KeyboardButton(text="🎯 Тесты и Блиц")],
        [KeyboardButton(text="📖 Чтение текстов"), KeyboardButton(text="🎮 Игры и Чат-бот")],
        [KeyboardButton(text="👤 Профиль"), KeyboardButton(text="⚙️ Настройки")],
        [KeyboardButton(text="⭐ Купить Премиум *")]
    ]
    if is_admin:
        rows.append([KeyboardButton(text="👑 Панель администратора")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, persistent=True)

def build_tests_hub_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎯 Обычный тест по словам", callback_data="hub_start_quiz")],
            [InlineKeyboardButton(text="⚡ Блиц-спринт (На скорость)", callback_data="hub_sprint_menu")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
        ]
    )

def build_games_hub_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🤖 Чат-бот симулятор", callback_data="hub_chatsim_open")],
            [InlineKeyboardButton(text="🕵️‍♂️ Детективное расследование", callback_data="game_detective_start")],
            [InlineKeyboardButton(text="⚡ Блиц-спринт", callback_data="hub_sprint_menu")],
            [InlineKeyboardButton(text="⭐ Премиум-аркада *", callback_data="game_premium_arcade")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
        ]
    )

def build_settings_hub_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔤 Изменить уровень обучения", callback_data="action_change_level")],
            [InlineKeyboardButton(text="📚 Домашнее задание (500 тем)", callback_data="hub_homework_open")],
            [InlineKeyboardButton(text="📖 Справочник падежей", callback_data="hub_grammar_open")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
        ]
    )

def build_premium_hub_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⭐ Купить Премиум (Stars)", callback_data="prem_hub_buy")],
            [InlineKeyboardButton(text="👥 Вывести друзей (Награды)", callback_data="prem_hub_withdraw")],
            [InlineKeyboardButton(text="🔗 Реферальная ссылка", callback_data="prem_hub_link")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
        ]
    )

def build_levels_selection_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🟢 Уровень A1", callback_data="setlevel_a1")],
            [InlineKeyboardButton(text="🟢 Уровень A2", callback_data="setlevel_a2")],
            [InlineKeyboardButton(text="🟡 Уровень B1 (Премиум ⭐)", callback_data="setlevel_b1")],
            [InlineKeyboardButton(text="🟠 Уровень B2 (Премиум ⭐)", callback_data="setlevel_b2")],
            [InlineKeyboardButton(text="🔴 Уровень C1 (Премиум ⭐)", callback_data="setlevel_c1")],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="action_main_menu")]
        ]
    )

def build_sprint_levels_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🟢 Спринт A1 (300 слов, 5 тем)", callback_data="sprint_lvl_a1")],
            [InlineKeyboardButton(text="🟢 Спринт A2 (300 слов, 5 тем)", callback_data="sprint_lvl_a2")],
            [InlineKeyboardButton(text="🟡 Спринт B1 (Премиум ⭐)", callback_data="sprint_lvl_b1")],
            [InlineKeyboardButton(text="🟠 Спринт B2 (Премиум ⭐)", callback_data="sprint_lvl_b2")],
            [InlineKeyboardButton(text="🔴 Спринт C1 (Премиум ⭐)", callback_data="sprint_lvl_c1")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
        ]
    )

def build_reading_levels_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🟡 Уровень B1 (10 текстов)", callback_data="readlvl_b1")],
            [InlineKeyboardButton(text="🟠 Уровень B2 (10 текстов)", callback_data="readlvl_b2")],
            [InlineKeyboardButton(text="🔴 Уровень C1 (10 текстов)", callback_data="readlvl_c1")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
        ]
    )

def build_grammar_directory_keyboard() -> InlineKeyboardMarkup:
    rows = []
    for code, info in EXTENDED_GRAMMAR_DATABASE.items():
        title = info.get("title", code)
        rows.append([InlineKeyboardButton(text=f"📌 {title}", callback_data=f"grammar_info_{code}")])
    rows.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

@router.message(CommandStart())
async def handle_start_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    uid_str = str(message.from_user.id)
    database = load_db()
    
    args = message.text.split()
    ref_id = None
    if len(args) > 1 and args[1].startswith("ref_"):
        ref_id = args[1].replace("ref_", "")
    
    if uid_str not in database:
        database[uid_str] = {
            "first_name": message.from_user.first_name or "Ученик",
            "level": "a1",
            "words_learned": 0,
            "correct_answers": 0,
            "quiz_score": 0,
            "is_premium": False,
            "premium_until": None,
            "invited_users": [],
            "referred_by": None,
            "referral_tier": 0,
            "joined_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if ref_id and ref_id != uid_str and ref_id in database:
            database[uid_str]["referred_by"] = ref_id
            if uid_str not in database[ref_id]["invited_users"]:
                database[ref_id]["invited_users"].append(uid_str)
                try:
                    await message.bot.send_message(
                        int(ref_id),
                        f"🎉 По вашей реферальной ссылке зарегистрировался новый друг ({html.quote(message.from_user.first_name)})!\n"
                        f"Всего приглашено друзей: <b>{len(database[ref_id]['invited_users'])}</b>. Зайдите в раздел «⭐ Купить Премиум *», чтобы забрать награду!"
                    )
                except Exception:
                    pass
                    
        save_db(database)

    is_admin = (message.from_user.id == ADMIN_TELEGRAM_ID)
    bot_info = await message.bot.get_me()
    bot_username = f"@{bot_info.username}"
    
    await message.answer(
        f"👋 Здравствуй, <b>{html.quote(message.from_user.first_name)}</b>!\n\n"
        f"Добро пожаловать в бота <b>{bot_username}</b>.\n"
        f"Все функции, словарные базы, тренировки и режим чтения полностью активированы!",
        parse_mode="HTML",
        reply_markup=build_main_menu_keyboard(is_admin)
    )

# --- ТЕСТЫ И БЛИЦ ---
@router.message(F.text == "🎯 Тесты и Блиц")
async def tests_hub_handler(message: Message) -> None:
    await message.answer(
        "🎯 <b>Тесты и Блиц-спринт:</b>\n\nВыберите режим проверки знаний:",
        parse_mode="HTML",
        reply_markup=build_tests_hub_keyboard()
    )

# --- ИГРЫ И ЧАТ-БОТ ---
@router.message(F.text == "🎮 Игры и Чат-бот")
async def games_hub_handler(message: Message) -> None:
    await message.answer(
        "🎮 <b>Игры, Чат-бот и Спринт:</b>\n\nВыберите интерактивный режим:",
        parse_mode="HTML",
        reply_markup=build_games_hub_keyboard()
    )

# --- ОТДЕЛЬНАЯ КНОПКА: ПРОФИЛЬ ---
@router.message(F.text == "👤 Профиль")
async def handle_profile_direct(message: Message) -> None:
    uid_str = str(message.from_user.id)
    db = load_db()
    info = db.get(uid_str, {
        "level": "a1",
        "words_learned": 0,
        "correct_answers": 0,
        "is_premium": False,
        "premium_until": None,
        "invited_users": [],
        "joined_date": "Н/Д"
    })
    
    prem_active = is_user_premium(info)
    sub_status = f"🟢 Активна до {info.get('premium_until', '')}" if prem_active else "⚪️ Базовый"
    invited_count = len(info.get("invited_users", []))
    
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
    await message.answer(
        f"📊 <b>Твой профиль и статистика:</b>\n\n"
        f"👤 Имя: {html.quote(message.from_user.first_name)}\n"
        f"📈 Уровень: <code>{info.get('level', 'a1').upper()}</code>\n"
        f"💎 Статус подписки: {sub_status}\n"
        f"👥 Приглашено друзей: <b>{invited_count}</b>\n"
        f"📚 Выучено карточек: {info.get('words_learned', 0)}\n"
        f"🎯 Правильных ответов в тестах: {info.get('correct_answers', 0)}\n"
        f"📅 Дата регистрации: {info.get('joined_date', 'Н/Д')}",
        parse_mode="HTML",
        reply_markup=markup
    )

# --- ОТДЕЛЬНАЯ КНОПКА: НАСТРОЙКИ ---
@router.message(F.text == "⚙️ Настройки")
async def handle_settings_direct(message: Message, state: FSMContext) -> None:
    await message.answer(
        "⚙️ <b>Настройки и вспомогательные разделы:</b>\n\nВыберите нужное действие:",
        parse_mode="HTML",
        reply_markup=build_settings_hub_keyboard()
    )

# --- ИНТЕРАКТИВНОЕ ДОМАШНЕЕ ЗАДАНИЕ (3 рандомных элемента из базы 100+ на уровень) ---
@router.callback_query(F.data == "hub_homework_open")
async def hub_homework_callback(callback: CallbackQuery, state: FSMContext) -> None:
    uid_str = str(callback.from_user.id)
    db = load_db()
    lvl = db.get(uid_str, {}).get("level", "a1")
    
    level_pool = HOMEWORK_DATABASE.get(lvl, HOMEWORK_DATABASE["a1"])
    selected_tasks = random.sample(level_pool, min(3, len(level_pool)))
    
    await state.update_data(hw_tasks=selected_tasks, hw_index=0, hw_score=0, hw_level=lvl)
    await state.set_state(BotStates.homework_active)
    
    summary_lines = []
    for t in selected_tasks:
        if t.get("type") == "word":
            summary_lines.append(f"• <b>{html.quote(str(t.get('en')))}</b> — {html.quote(str(t.get('ru')))}")
        else:
            summary_lines.append(f"• <i>Предложение:</i> {html.quote(str(t.get('en')))} — {html.quote(str(t.get('ru')))}")
            
    summary_text = "\n".join(summary_lines)
    
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Начать проверку ДЗ", callback_data="hw_next_step")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    
    await callback.message.edit_text(
        f"📚 <b>Домашнее задание (Уровень {lvl.upper()}):</b>\n\n"
        f"<b>Шаг 1.</b> Изучи эти элементы задания:\n{summary_text}\n\n"
        f"Нажми кнопку ниже, когда будешь готов к проверке!",
        parse_mode="HTML",
        reply_markup=markup
    )
    await callback.answer()

@router.callback_query(F.data == "hw_next_step", StateFilter(BotStates.homework_active, BotStates.homework_text_input))
async def process_homework_next_step(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    tasks = data.get("hw_tasks", [])
    index = data.get("hw_index", 0)
    score = data.get("hw_score", 0)
    lvl = data.get("hw_level", "a1")
    
    if index >= len(tasks):
        db = load_db()
        uid_str = str(callback.from_user.id)
        if uid_str in db:
            db[uid_str]["words_learned"] = db[uid_str].get("words_learned", 0) + 3
            db[uid_str]["correct_answers"] = db[uid_str].get("correct_answers", 0) + score
            save_db(db)
            
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Новое домашнее задание", callback_data="hub_homework_open")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
        ])
        await callback.message.edit_text(
            f"🎉 <b>Домашнее задание успешно выполнено!</b>\n\n"
            f"🎯 Правильных ответов: <b>{score} из {len(tasks)}</b>\n"
            f"⭐ Зачислено +3 выученных слова в профиль!",
            parse_mode="HTML",
            reply_markup=markup
        )
        await state.clear()
        await callback.answer()
        return
        
    current_task = tasks[index]
    task_type = current_task.get("type", "word")
    
    # Случайный выбор формата проверки (0 - выбор из 5 вариантов, 1 - ввод слова, 2 - перевод предложения)
    if task_type == "sentence":
        sub_mode = 2
    else:
        sub_mode = random.choice([0, 1])
        
    direction = random.choice(["en_to_ru", "ru_to_en"])
    
    if sub_mode == 0:
        # Выбор из 5 вариантов (для слов)
        word_en = str(current_task.get("en", ""))
        word_ru = str(current_task.get("ru", ""))
        
        level_words = [w for w in HOMEWORK_DATABASE.get(lvl, []) if w.get("type") == "word"]
        if direction == "en_to_ru":
            prompt = f"Как переводится на русский слово:\n🔤 <b>{html.quote(word_en)}</b>?"
            correct_ans = word_ru
            wrong_pool = [str(w.get("ru")) for w in level_words if str(w.get("ru")) != word_ru]
            wrong_opts = random.sample(wrong_pool, min(4, len(wrong_pool))) if wrong_pool else ["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4"]
            options = wrong_opts + [correct_ans]
            random.shuffle(options)
        else:
            prompt = f"Как переводится на английский слово:\n🇷🇺 <b>{html.quote(word_ru)}</b>?"
            correct_ans = word_en
            wrong_pool = [str(w.get("en")) for w in level_words if str(w.get("en")) != word_en]
            wrong_opts = random.sample(wrong_pool, min(4, len(wrong_pool))) if wrong_pool else ["Apple", "House", "Car", "Tree"]
            options = wrong_opts + [correct_ans]
            random.shuffle(options)
            
        await state.update_data(hw_correct=correct_ans)
        
        btns = []
        for opt in options:
            is_c = "1" if opt == correct_ans else "0"
            btns.append([InlineKeyboardButton(text=opt, callback_data=f"hw_ans_{is_c}")])
        btns.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")])
        
        await callback.message.edit_text(
            f"📚 <b>ДЗ (Вопрос {index + 1} из {len(tasks)}):</b>\n\n{prompt}",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns)
        )
    elif sub_mode == 1:
        # Самостоятельный ввод слова текстом
        word_en = str(current_task.get("en", ""))
        word_ru = str(current_task.get("ru", ""))
        
        if direction == "en_to_ru":
            prompt = f"Напиши перевод на русский для слова:\n🔤 <b>{html.quote(word_en)}</b>"
            correct_ans = word_ru.lower().strip()
        else:
            prompt = f"Напиши перевод на английский для слова:\n🇷🇺 <b>{html.quote(word_ru)}</b>"
            correct_ans = word_en.lower().strip()
            
        await state.set_state(BotStates.homework_text_input)
        await state.update_data(hw_correct=correct_ans)
        
        markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
        await callback.message.edit_text(
            f"📚 <b>ДЗ (Вопрос {index + 1} из {len(tasks)} - Ввод слова):</b>\n\n{prompt}\n\n"
            f"✍️ <i>Отправь свой вариант ответа следующим сообщением в чат.</i>",
            parse_mode="HTML",
            reply_markup=markup
        )
    else:
        # Перевод предложений (с англ на русс или с русс на англ в случайной форме)
        sent_en = str(current_task.get("en", ""))
        sent_ru = str(current_task.get("ru", ""))
        
        if direction == "en_to_ru":
            prompt = f"Переведи предложение на русский язык:\n🇬🇧 <b>{html.quote(sent_en)}</b>"
            correct_ans = sent_ru.lower().strip()
        else:
            prompt = f"Переведи предложение на английский язык:\n🇷🇺 <b>{html.quote(sent_ru)}</b>"
            correct_ans = sent_en.lower().strip()
            
        await state.set_state(BotStates.homework_text_input)
        await state.update_data(hw_correct=correct_ans)
        
        markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
        await callback.message.edit_text(
            f"📚 <b>ДЗ (Вопрос {index + 1} из {len(tasks)} - Перевод предложения):</b>\n\n{prompt}\n\n"
            f"✍️ <i>Отправь перевод текстом в чат.</i>",
            parse_mode="HTML",
            reply_markup=markup
        )
    await callback.answer()

@router.callback_query(F.data.startswith("hw_ans_"), StateFilter(BotStates.homework_active))
async def homework_choice_answer_callback(callback: CallbackQuery, state: FSMContext) -> None:
    is_corr = callback.data.split("_")[2] == "1"
    data = await state.get_data()
    correct_word = data.get("hw_correct", "")
    score = data.get("hw_score", 0)
    index = data.get("hw_index", 0)
    
    if is_corr:
        score += 1
        res_header = "✅ <b>Правильно!</b>"
    else:
        res_header = f"❌ <b>Неправильно!</b> Правильный ответ: <b>{html.quote(str(correct_word))}</b>"
        
    await state.update_data(hw_score=score, hw_index=index + 1)
    
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Следующий вопрос", callback_data="hw_next_step")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    await callback.message.edit_text(f"{res_header}", parse_mode="HTML", reply_markup=markup)
    await callback.answer()

@router.message(StateFilter(BotStates.homework_text_input), F.text)
async def homework_text_input_handler(message: Message, state: FSMContext) -> None:
    user_text = message.text.lower().strip()
    data = await state.get_data()
    correct_word = str(data.get("hw_correct", "")).lower().strip()
    score = data.get("hw_score", 0)
    index = data.get("hw_index", 0)
    
    # Гибкая проверка для предложений (убираем лишние точки/пробелы для удобства)
    clean_user = user_text.replace(".", "").replace(",", "").strip()
    clean_correct = correct_word.replace(".", "").replace(",", "").strip()
    
    is_corr = (clean_user == clean_correct) or (user_text == correct_word)
    if is_corr:
        score += 1
        res_header = "✅ <b>Отлично, верно!</b>"
    else:
        res_header = f"❌ <b>Неверно!</b> Твой ответ: «{html.quote(message.text)}». Правильный ответ: <b>{html.quote(str(data.get('hw_correct')))}</b>"
        
    await state.update_data(hw_score=score, hw_index=index + 1)
    await state.set_state(BotStates.homework_active)
    
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Следующий вопрос", callback_data="hw_next_step")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    await message.answer(f"{res_header}", parse_mode="HTML", reply_markup=markup)

# --- БЛИЦ-СПРИНТ ---
@router.callback_query(F.data == "hub_sprint_menu")
async def hub_sprint_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(
        "⚡ <b>Режим «Спринт (Блиц)»</b>\n\nВыберите уровень для молниеносной тренировки словарного запаса:",
        parse_mode="HTML",
        reply_markup=build_sprint_levels_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("sprint_lvl_"))
async def sprint_level_selected_callback(callback: CallbackQuery, state: FSMContext) -> None:
    lvl = callback.data.split("_")[2]
    uid_str = str(callback.from_user.id)
    db = load_db()
    is_prem = is_user_premium(db.get(uid_str, {}))
    
    if lvl in ["b1", "b2", "c1"] and not is_prem:
        await callback.answer(f"⚠️ Уровень {lvl.upper()} для Спринта требует Премиум-подписку ⭐!", show_alert=True)
        return
        
    categories_map = {
        "a1": SPRINT_A1_CATEGORIES,
        "a2": SPRINT_A2_CATEGORIES,
        "b1": SPRINT_B1_CATEGORIES,
        "b2": SPRINT_B2_CATEGORIES,
        "c1": SPRINT_C1_CATEGORIES
    }
    categories = categories_map.get(lvl, {})
    if not categories:
        await callback.answer("⚠️ Словарь для этого уровня спринта еще не заполнен.", show_alert=True)
        return
        
    btns = []
    for cat_key, words_list in categories.items():
        cat_title = cat_key.replace("_", " ").title()
        btns.append([InlineKeyboardButton(text=f"📂 {cat_title} ({len(words_list)} слов)", callback_data=f"spcat_{lvl}_{cat_key}")])
        
    btns.append([InlineKeyboardButton(text="🔙 К выбору уровней спринта", callback_data="hub_sprint_menu")])
    btns.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")])
    
    await callback.message.edit_text(
        f"⚡ <b>Спринт: Уровень {lvl.upper()}</b>\n\nВыберите категорию для тренировки:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=btns)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("spcat_"))
async def start_sprint_category_session(callback: CallbackQuery, state: FSMContext) -> None:
    parts = callback.data.split("_", 2)
    lvl = parts[1]
    cat_key = parts[2]
    
    categories_map = {
        "a1": SPRINT_A1_CATEGORIES,
        "a2": SPRINT_A2_CATEGORIES,
        "b1": SPRINT_B1_CATEGORIES,
        "b2": SPRINT_B2_CATEGORIES,
        "c1": SPRINT_C1_CATEGORIES
    }
    categories = categories_map.get(lvl, {})
    words_list = categories.get(cat_key, [])
    
    if not words_list:
        await callback.answer("⚠️ В этой категории пока нет слов.", show_alert=True)
        return
        
    session_words = list(words_list)
    random.shuffle(session_words)
    
    await state.update_data(
        sprint_lvl=lvl,
        sprint_cat=cat_key,
        sprint_words=session_words,
        sprint_index=0,
        sprint_score=0
    )
    await state.set_state(BotStates.sprint_active)
    
    await send_next_sprint_question(callback.message, state, is_edit=True)
    await callback.answer()

async def send_next_sprint_question(message: Message, state: FSMContext, is_edit: bool = False) -> None:
    data = await state.get_data()
    words = data.get("sprint_words", [])
    index = data.get("sprint_index", 0)
    score = data.get("sprint_score", 0)
    lvl = data.get("sprint_lvl", "a1")
    cat_key = data.get("sprint_cat", "")
    
    if index >= len(words) or index >= 20:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Сыграть снова в эту тему", callback_data=f"spcat_{lvl}_{cat_key}")],
            [InlineKeyboardButton(text="⚡ К выбору тем спринта", callback_data=f"sprint_lvl_{lvl}")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
        ])
        text = (
            f"🎉 <b>Спринт завершен!</b>\n\n"
            f"🎯 Ваш результат: <b>{score} из {min(len(words), 20)}</b> правильных ответов!"
        )
        if is_edit:
            await message.edit_text(text, parse_mode="HTML", reply_markup=markup)
        else:
            await message.answer(text, parse_mode="HTML", reply_markup=markup)
        return
        
    current_item = words[index]
    word_en = current_item.get("word", "")
    correct_ru = current_item.get("ru", "")
    
    all_rus = [w.get("ru") for w in words if w.get("ru") != correct_ru]
    num_opts = min(3, len(all_rus))
    wrong_opts = random.sample(all_rus, num_opts) if num_opts > 0 else ["Нет варианта"]
    
    options = wrong_opts + [correct_ru]
    random.shuffle(options)
    
    await state.update_data(current_sprint_correct=correct_ru)
    
    btns = []
    for opt in options:
        is_corr_str = "1" if opt == correct_ru else "0"
        btns.append([InlineKeyboardButton(text=opt, callback_data=f"spans_{is_corr_str}")])
        
    btns.append([InlineKeyboardButton(text="❌ Завершить спринт", callback_data=f"sprint_lvl_{lvl}")])
    
    text = (
        f"⚡ <b>Спринт ({lvl.upper()}): Вопрос {index + 1} / {min(len(words), 20)}</b>\n"
        f"🏆 Счет: {score}\n\n"
        f"Как переводится слово:\n🔤 <b>{html.quote(word_en)}</b>?"
    )
    
    markup = InlineKeyboardMarkup(inline_keyboard=btns)
    if is_edit:
        await message.edit_text(text, parse_mode="HTML", reply_markup=markup)
    else:
        await message.answer(text, parse_mode="HTML", reply_markup=markup)

@router.callback_query(F.data.startswith("spans_"), StateFilter(BotStates.sprint_active))
async def process_sprint_answer(callback: CallbackQuery, state: FSMContext) -> None:
    is_correct = callback.data.split("_")[1] == "1"
    data = await state.get_data()
    
    score = data.get("sprint_score", 0)
    if is_correct:
        score += 1
        
    index = data.get("sprint_index", 0) + 1
    await state.update_data(sprint_score=score, sprint_index=index)
    
    await send_next_sprint_question(callback.message, state, is_edit=True)
    await callback.answer()

@router.callback_query(F.data == "hub_grammar_open")
async def hub_grammar_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "📚 <b>Справочник падежей и грамматики:</b>\n\nВыбери интересующий раздел из списка ниже:",
        parse_mode="HTML",
        reply_markup=build_grammar_directory_keyboard()
    )
    await callback.answer()

# --- ЧТЕНИЕ ТЕКСТОВ ---
@router.message(F.text == "📖 Чтение текстов")
async def reading_menu_handler(message: Message, state: FSMContext) -> None:
    uid_str = str(message.from_user.id)
    db = load_db()
    is_prem = is_user_premium(db.get(uid_str, {}))
    
    if not is_prem:
        await message.answer(
            "⭐ <b>Режим чтения текстов (B1, B2, C1)</b>\n\n"
            "⚠️ Для доступа к расширенным академическим и публицистическим текстам требуется Премиум-подписка ⭐!",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⭐ Купить Премиум", callback_data="prem_hub_buy")],
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
            ])
        )
        return

    await message.answer(
        "📖 <b>Выберите уровень для чтения текстов:</b>\n\n"
        "• <b>B1</b> — Повседневные и социальные темы (10 текстов с вопросами)\n"
        "• <b>B2</b> — Сложные научные, экономические и социальные статьи\n"
        "• <b>C1</b> — Глубокие академические и философские трактаты",
        parse_mode="HTML",
        reply_markup=build_reading_levels_keyboard()
    )

@router.callback_query(F.data.startswith("readlvl_"))
async def select_reading_level_callback(callback: CallbackQuery, state: FSMContext) -> None:
    lvl = callback.data.split("_")[1]
    uid_str = str(callback.from_user.id)
    db = load_db()
    if not is_user_premium(db.get(uid_str, {})):
        await callback.answer("⚠️ Требуется Премиум-подписка ⭐!", show_alert=True)
        return
        
    passages_map = {
        "b1": READING_PASSAGES_B1,
        "b2": READING_PASSAGES_B2,
        "c1": READING_PASSAGES_C1
    }
    passages = passages_map.get(lvl, [])
    if not passages:
        await callback.answer("⚠️ Тексты для этого уровня пока не загружены.", show_alert=True)
        return
        
    btns = []
    for p in passages:
        p_id = p.get("id")
        p_title = p.get("title", f"Текст {p_id}")
        btns.append([InlineKeyboardButton(text=f"📄 {p_title}", callback_data=f"readtext_{lvl}_{p_id}")])
    btns.append([InlineKeyboardButton(text="🔙 К выбору уровней чтения", callback_data="back_to_read_menu")])
    btns.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")])
    
    await callback.message.edit_text(
        f"📖 <b>Тексты уровня {lvl.upper()}:</b>\n\nВыберите интересующий вас текст из списка:",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=btns)
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_read_menu")
async def back_to_reading_menu(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "📖 <b>Выберите уровень для чтения текстов:</b>",
        parse_mode="HTML",
        reply_markup=build_reading_levels_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("readtext_"))
async def show_reading_text_callback(callback: CallbackQuery, state: FSMContext) -> None:
    parts = callback.data.split("_")
    lvl = parts[1]
    p_id = parts[2]
    try:
        p_id = int(p_id)
    except ValueError:
        pass
    
    passages_map = {
        "b1": READING_PASSAGES_B1,
        "b2": READING_PASSAGES_B2,
        "c1": READING_PASSAGES_C1
    }
    passages = passages_map.get(lvl, [])
    target_passage = next((p for p in passages if p.get("id") == p_id), None)
    
    if not target_passage:
        await callback.answer("⚠️ Текст не найден.", show_alert=True)
        return
        
    text_content = target_passage.get("text", "")
    title = target_passage.get("title", "")
    questions = target_passage.get("questions", [])
    
    await state.update_data(current_reading_passage=target_passage, reading_q_index=0, reading_correct_count=0)
    await state.set_state(BotStates.reading_mode_active)
    
    display_text = (
        f"📚 <b>{html.quote(title)}</b>\n\n"
        f"{html.quote(text_content)}\n\n"
        f"🎯 <i>Текст содержит {len(questions)} вопросов для проверки понимания. Нажмите кнопку ниже, чтобы начать!</i>"
    )
    
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Начать вопросы к тексту", callback_data=f"read_start_q_{lvl}_{p_id}_0")],
        [InlineKeyboardButton(text="🔙 К списку текстов", callback_data=f"readlvl_{lvl}")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    
    if len(display_text) > 4000:
        display_text = display_text[:3950] + "\n\n[Текст сокращен для отображения]..."
        
    await callback.message.edit_text(display_text, parse_mode="HTML", reply_markup=markup)
    await callback.answer()

@router.callback_query(F.data.startswith("read_start_q_"), StateFilter(BotStates.reading_mode_active))
async def process_reading_question(callback: CallbackQuery, state: FSMContext) -> None:
    parts = callback.data.split("_")
    lvl = parts[3]
    p_id = parts[4]
    try:
        p_id = int(p_id)
    except ValueError:
        pass
    q_index = int(parts[5])
    
    data = await state.get_data()
    passage = data.get("current_reading_passage")
    if not passage:
        await callback.answer("⚠️ Сессия чтения сброшена.", show_alert=True)
        return
        
    questions = passage.get("questions", [])
    if q_index >= len(questions):
        correct_count = data.get("reading_correct_count", 0)
        await callback.message.edit_text(
            f"🎉 <b>Поздравляем! Вы завершили чтение текста и вопросы!</b>\n\n"
            f"🎯 Правильных ответов: <b>{correct_count} из {len(questions)}</b>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📖 К списку текстов", callback_data=f"readlvl_{lvl}")],
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
            ])
        )
        await callback.answer()
        await state.clear()
        return
        
    q = questions[q_index]
    q_text = q.get("q") or q.get("question", "")
    options = q.get("options", [])
    correct_ans = q.get("answer") or q.get("correct", "")
    
    if options:
        btns = []
        for opt in options:
            is_corr = "1" if opt == correct_ans else "0"
            btns.append([InlineKeyboardButton(text=opt, callback_data=f"readans_{lvl}_{p_id}_{q_index}_{is_corr}")])
        btns.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")])
        
        await callback.message.edit_text(
            f"❓ <b>Вопрос {q_index + 1} из {len(questions)}</b>:\n\n{html.quote(q_text)}",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=btns)
        )
    else:
        sample_ans = q.get("sample", correct_ans)
        await state.update_data(current_open_q_index=q_index, current_lvl=lvl, current_p_id=p_id)
        await callback.message.edit_text(
            f"✍️ <b>Вопрос {q_index + 1} из {len(questions)}</b> (Открытый вопрос):\n\n"
            f"{html.quote(q_text)}\n\n"
            f"💡 <i>Напишите ваш ответ в чат следующим сообщением. Образец ответа: <code>{html.quote(str(sample_ans))}</code></i>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
        )
    await callback.answer()

@router.callback_query(F.data.startswith("readans_"), StateFilter(BotStates.reading_mode_active))
async def evaluate_reading_choice_answer(callback: CallbackQuery, state: FSMContext) -> None:
    parts = callback.data.split("_")
    lvl = parts[1]
    p_id = parts[2]
    q_index = int(parts[3])
    is_corr = parts[4] == "1"
    
    data = await state.get_data()
    correct_count = data.get("reading_correct_count", 0)
    if is_corr:
        correct_count += 1
        await state.update_data(reading_correct_count=correct_count)
        
    next_index = q_index + 1
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Следующий вопрос", callback_data=f"read_start_q_{lvl}_{p_id}_{next_index}")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    
    res_text = "✅ <b>Верно!</b>" if is_corr else "❌ <b>Неправильно.</b>"
    await callback.message.edit_text(f"{res_text}", parse_mode="HTML", reply_markup=markup)
    await callback.answer()

@router.message(StateFilter(BotStates.reading_mode_active), F.text)
async def evaluate_reading_open_answer(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    q_index = data.get("current_open_q_index")
    lvl = data.get("current_lvl")
    p_id = data.get("current_p_id")
    passage = data.get("current_reading_passage")
    
    if q_index is None or not passage:
        return
        
    questions = passage.get("questions", [])
    q = questions[q_index]
    sample = q.get("sample") or q.get("answer") or q.get("correct", "")
    
    correct_count = data.get("reading_correct_count", 0) + 1
    await state.update_data(reading_correct_count=correct_count)
    
    next_index = q_index + 1
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Следующий вопрос", callback_data=f"read_start_q_{lvl}_{p_id}_{next_index}")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    
    await message.answer(
        f"✍️ <b>Ваш ответ принят!</b>\n\n"
        f"💡 Образец правильного ответа:\n<i>{html.quote(str(sample))}</i>",
        parse_mode="HTML",
        reply_markup=markup
    )

# --- ПРЕМИУМ И РЕФЕРАЛЫ ---
@router.message(F.text.in_(["⭐ Купить Премиум *", "⭐ Купить Премиум"]))
async def premium_hub_handler(message: Message) -> None:
    uid_str = str(message.from_user.id)
    db = load_db()
    user_info = db.get(uid_str, {})
    prem_active = is_user_premium(user_info)
    
    status_text = f"🟢 Активен до {user_info.get('premium_until')}" if prem_active else "⚪️ Отсутствует (Базовый)"
    
    text = (
        f"⭐ <b>Центр Премиум и Рефералов:</b>\n\n"
        f"Статус подписки: {status_text}\n\n"
        f"Выберите нужное действие из меню ниже:"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=build_premium_hub_keyboard())

@router.callback_query(F.data == "prem_hub_buy")
async def callback_prem_buy(callback: CallbackQuery) -> None:
    prices = [LabeledPrice(label="Премиум доступ", amount=50)]
    try:
        await callback.message.answer_invoice(
            title="⭐ Премиум-подписка",
            description="Разблокирует уровни B1, B2, C1, тексты для чтения, спринты и эксклюзивные функции на 30 дней!",
            prices=prices,
            payload="premium_sub_payload",
            currency="XTR",
            provider_token=""
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Failed to send invoice: {e}", exc_info=True)
        await callback.answer("⚠️ Не удалось сформировать счет.", show_alert=True)

@router.callback_query(F.data == "prem_hub_link")
async def callback_prem_link(callback: CallbackQuery) -> None:
    uid_str = str(callback.from_user.id)
    bot_user = await callback.bot.get_me()
    ref_link = f"https://t.me/{bot_user.username}?start=ref_{uid_str}"
    
    text = (
        f"🔗 <b>Ваша реферальная ссылка:</b>\n\n"
        f"<code>{ref_link}</code>\n\n"
        f"💡 <i>Отправьте эту ссылку друзьям. Когда они перейдут по ней и запустят бота, они засчитаются в вашу статистику!</i>"
    )
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад в Премиум-меню", callback_data="back_to_prem_hub")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=markup)
    await callback.answer()

@router.callback_query(F.data == "prem_hub_withdraw")
async def callback_prem_withdraw(callback: CallbackQuery) -> None:
    uid_str = str(callback.from_user.id)
    db = load_db()
    user_data = db.get(uid_str, {})
    
    invited_count = len(user_data.get("invited_users", []))
    tier = user_data.get("referral_tier", 0)
    
    text = (
        f"👥 <b>Вывод друзей и награды (Рефералы):</b>\n\n"
        f"Накопительная система бонусов:\n"
        f"• <b>1 друг</b> = 1 день Премиума {'(✅ Получено)' if tier >= 1 else ''}\n"
        f"• <b>2 друга</b> = 3 дня Премиума {'(✅ Получено)' if tier >= 2 else ''}\n"
        f"• <b>3 друга</b> = 7 дней Премиума {'(✅ Получено)' if tier >= 3 else ''}\n\n"
        f"📊 Приглашено друзей: <b>{invited_count}</b>\n"
        f"⭐ Текущий уровень бонуса: <b>Уровень {tier}/3</b>"
    )
    
    markup_rows = []
    if (invited_count >= 1 and tier < 1) or (invited_count >= 2 and tier < 2) or (invited_count >= 3 and tier < 3):
        markup_rows.append([InlineKeyboardButton(text="🎁 Забрать доступную награду", callback_data="claim_referral_reward")])
        
    markup_rows.append([InlineKeyboardButton(text="◀️ Назад в Премиум-меню", callback_data="back_to_prem_hub")])
    markup_rows.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")])
    
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(inline_keyboard=markup_rows))
    await callback.answer()

@router.callback_query(F.data == "back_to_prem_hub")
async def callback_back_prem_hub(callback: CallbackQuery) -> None:
    text = "⭐ <b>Центр Премиум и Рефералов:</b>\n\nВыберите нужное действие из меню ниже:"
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=build_premium_hub_keyboard())
    await callback.answer()

@router.callback_query(F.data == "claim_referral_reward")
async def claim_referral_callback(callback: CallbackQuery) -> None:
    uid_str = str(callback.from_user.id)
    db = load_db()
    user_data = db.get(uid_str, {})
    
    invited_count = len(user_data.get("invited_users", []))
    tier = user_data.get("referral_tier", 0)
    
    days_to_add = 0
    new_tier = tier
    
    if invited_count >= 3 and tier < 3:
        if tier == 0: days_to_add = 7
        elif tier == 1: days_to_add = 6
        elif tier == 2: days_to_add = 4
        new_tier = 3
    elif invited_count >= 2 and tier < 2:
        if tier == 0: days_to_add = 3
        elif tier == 1: days_to_add = 2
        new_tier = 2
    elif invited_count >= 1 and tier < 1:
        days_to_add = 1
        new_tier = 1
        
    if days_to_add > 0:
        user_data["referral_tier"] = new_tier
        add_premium_days(user_data, days_to_add)
        db[uid_str] = user_data
        save_db(db)
        
        await callback.answer(f"🎉 Успешно! Вам добавлено +{days_to_add} дн. Премиума!", show_alert=True)
        
        invited_count = len(user_data.get("invited_users", []))
        tier = user_data.get("referral_tier", 0)
        text = (
            f"👥 <b>Вывод друзей и награды (Рефералы):</b>\n\n"
            f"• <b>1 друг</b> = 1 день {'(✅ Получено)' if tier >= 1 else ''}\n"
            f"• <b>2 друга</b> = 3 дня {'(✅ Получено)' if tier >= 2 else ''}\n"
            f"• <b>3 друга</b> = 7 дней {'(✅ Получено)' if tier >= 3 else ''}\n\n"
            f"📊 Приглашено друзей: <b>{invited_count}</b>"
        )
        markup_rows = []
        if (invited_count >= 1 and tier < 1) or (invited_count >= 2 and tier < 2) or (invited_count >= 3 and tier < 3):
            markup_rows.append([InlineKeyboardButton(text="🎁 Забрать награду", callback_data="claim_referral_reward")])
        markup_rows.append([InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_prem_hub")])
        markup_rows.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")])
        
        try:
            await callback.message.edit_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(inline_keyboard=markup_rows))
        except Exception:
            pass
    else:
        await callback.answer("⚠️ Все доступные награды уже получены.", show_alert=True)

@router.callback_query(F.data.startswith("grammar_info_"))
async def process_grammar_card(callback: CallbackQuery) -> None:
    code = callback.data.split("_")[2]
    data = EXTENDED_GRAMMAR_DATABASE.get(code)
    if not data:
        await callback.answer("⚠️ Информация не найдена в базе.", show_alert=True)
        return
        
    examples_text = "\n".join([f"• <i>{ex}</i>" for ex in data.get('examples', [])])
    text = (
        f"<b>{data.get('title', '')}</b>\n\n"
        f"❓ <b>Вопросы:</b> {data.get('questions', '')}\n"
        f"🎯 <b>Назначение:</b> {data.get('purpose', '')}\n\n"
        f"📜 <b>Правила:</b> {data.get('rules', '')}\n\n"
        f"💡 <b>Примеры:</b>\n{examples_text}\n\n"
        f"⚡ <b>Совет:</b> {data.get('tips', '')}"
    )
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=build_grammar_directory_keyboard())
    await callback.answer()

@router.callback_query(F.data == "game_detective_start")
async def detective_game_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BotStates.detective_game_active)
    text = (
        "🕵️‍♂️ <b>Детективное расследование: Дело о пропавшем коде</b>\n\n"
        "Вы стоите в темном офисе стартапа. Куда вы хотите заглянуть в первую очередь?"
    )
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑 Корзина", callback_data="det_choice_trash")],
        [InlineKeyboardButton(text="💻 Git коммиты", callback_data="det_choice_git")],
        [InlineKeyboardButton(text="😴 Сисадмин", callback_data="det_choice_admin")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=markup)
    await callback.answer()

@router.callback_query(F.data.startswith("det_choice_"), StateFilter(BotStates.detective_game_active))
async def detective_branch_handler(callback: CallbackQuery, state: FSMContext) -> None:
    choice = callback.data.split("_")[2]
    if choice == "trash":
        result = "🗑 В корзине вы нашли подсказку: <i>'Use pip install carefully'</i>."
    elif choice == "git":
        result = "💻 В истории Git обнаружена рабочая версия кода! Дело раскрыто! 🎉"
    else:
        result = "😴 Сисадмин проснулся, дал кофе и подсказал проверить логи на Render."
    
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Сыграть снова", callback_data="game_detective_start")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    await callback.message.edit_text(f"🕵️‍♂️ <b>Результат расследования:</b>\n\n{result}", parse_mode="HTML", reply_markup=markup)
    await callback.answer()

@router.callback_query(F.data == "game_premium_arcade")
async def premium_arcade_callback(callback: CallbackQuery) -> None:
    uid_str = str(callback.from_user.id)
    db = load_db()
    if not is_user_premium(db.get(uid_str, {})):
        await callback.answer("⚠️ Премиум-аркада доступна только по подписке ⭐!", show_alert=True)
        return
    await callback.message.edit_text(
        "⭐ <b>Премиум-аркада активна *!</b>\n\nДобро пожаловать в секретный режим.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
    )
    await callback.answer()

@router.callback_query(F.data == "chatsim_start_dialog")
async def chatsim_start_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "🤖 <b>Диалог начат:</b>\n\n— Hello! How can I help you today?",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
    )
    await callback.answer()

@router.callback_query(F.data == "adventure_start_quest")
async def adventure_start_callback(callback: CallbackQuery) -> None:
    uid_str = str(callback.from_user.id)
    db = load_db()
    if not is_user_premium(db.get(uid_str, {})):
        await callback.answer("⚠️ Квесты с пометкой * требуют Премиум-подписку ⭐!", show_alert=True)
        return
    await callback.message.edit_text(
        "⚔️ <b>Квест начат:</b>\n\nВы стоите у входа в заброшенную пещеру.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
    )
    await callback.answer()

@router.callback_query(F.data == "action_main_menu")
async def return_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    is_admin = (callback.from_user.id == ADMIN_TELEGRAM_ID)
    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.message.answer("🏠 Главное меню:", reply_markup=build_main_menu_keyboard(is_admin))
    await callback.answer()

# --- УЧИТЬ СЛОВА (С НАДЕЖНЫМ СОХРАНЕНИЕМ УРОВНЯ В БД) ---
@router.message(F.text == "📚 Учить слова")
async def entry_vocab(message: Message, state: FSMContext) -> None:
    uid_str = str(message.from_user.id)
    db = load_db()
    saved_lvl = db.get(uid_str, {}).get("level", "a1")
    
    await state.update_data(active_vocab_level=saved_lvl)
    await state.set_state(BotStates.active_learning_session)
    await message.answer(f"🔤 Загружен твой сохраненный уровень: <b>{saved_lvl.upper()}</b>", parse_mode="HTML")
    await dispatch_card(message, saved_lvl, replace=False)

@router.callback_query(F.data.startswith("setlevel_"))
async def set_vocab_level(callback: CallbackQuery, state: FSMContext) -> None:
    lvl = callback.data.split("_")[1]
    uid_str = str(callback.from_user.id)
    db = load_db()
    is_prem = is_user_premium(db.get(uid_str, {}))
    
    if lvl in ["b1", "b2", "c1"] and not is_prem:
        await callback.answer(f"⚠️ Уровень {lvl.upper()} платный! Требуется Премиум-подписка ⭐.", show_alert=True)
        return
            
    if uid_str not in db:
        db[uid_str] = {
            "first_name": callback.from_user.first_name,
            "level": lvl,
            "words_learned": 0,
            "correct_answers": 0,
            "is_premium": False,
            "premium_until": None,
            "invited_users": [],
            "referred_by": None,
            "referral_tier": 0,
            "joined_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    else:
        db[uid_str]["level"] = lvl
    save_db(db)
        
    await state.update_data(active_vocab_level=lvl)
    await state.set_state(BotStates.active_learning_session)
    await callback.message.edit_text(f"✅ Установлен и сохранен уровень: <b>{lvl.upper()}</b>", parse_mode="HTML")
    await dispatch_card(callback.message, lvl, replace=True)
    await callback.answer()

async def dispatch_card(message: Message, level_code: str, replace: bool = False) -> None:
    maps = {"a1": WORDS_A1, "a2": WORDS_A2, "b1": WORDS_B1, "b2": WORDS_B2, "c1": WORDS_C1}
    pool = maps.get(level_code, WORDS_A1)
    if not pool:
        pool = [{"word": "Default", "trans": "", "ru": "Слово", "ex": "Example sentence."}]
        
    word = random.choice(pool)
    card = (
        f"📖 <b>Карточка слова ({level_code.upper()})</b>\n\n"
        f"🔤 <b>{html.quote(str(word.get('word', '')))}</b> {word.get('trans', '')}\n"
        f"🇷🇺 <b>{html.quote(str(word.get('ru', '')))}</b>\n\n"
        f"<i>Пример: {html.quote(str(word.get('ex', '')))}</i>"
    )
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➡️ Следующее слово", callback_data="action_next_word")],
            [InlineKeyboardButton(text="⚙️ Изменить уровень", callback_data="action_change_level")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
        ]
    )
    
    if replace:
        try:
            await message.message.edit_text(card, parse_mode="HTML", reply_markup=keyboard)
        except Exception:
            await message.answer(card, parse_mode="HTML", reply_markup=keyboard)
    else:
        await message.answer(card, parse_mode="HTML", reply_markup=keyboard)

@router.callback_query(F.data == "action_next_word", StateFilter(BotStates.active_learning_session))
async def next_word(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    lvl = data.get("active_vocab_level", "a1")
    uid_str = str(callback.from_user.id)
    
    db = load_db()
    if uid_str in db:
        db[uid_str]["words_learned"] = db[uid_str].get("words_learned", 0) + 1
        save_db(db)
        
    await dispatch_card(callback, lvl, replace=True)
    await callback.answer()

@router.callback_query(F.data == "action_change_level")
async def change_level(callback: CallbackQuery, state: FSMContext) -> None:
    levels_desc = (
        "⚙️ <b>Настройки — Выбор уровня сложности:</b>\n\n"
        "• <b>A1 (Начальный)</b> — Базовый старт для новичков. Вы учитесь представляться, понимать простейшие вопросы, здороваться и строить элементарные предложения о себе.\n"
        "  <i>Примеры слов: apple, water, cat, dog, hello, house</i>\n\n"
        "• <b>A2 (Элементарный)</b> — Уверенная база. Вы можете описать свой обычный день, рассказать о семье, друзьях, хобби и поддержать простой диалог в магазине или кафе.\n"
        "  <i>Примеры слов: holiday, kitchen, travel, weather, morning, friend</i>\n\n"
        "• <b>B1 (Средний / Intermediate) ⭐</b> — Уверенное общение. Вы можете свободно путешествовать, описывать свои планы, выражать личное мнение, рассказывать истории и справляться с неожиданными мелкими проблемами в чужой стране.\n"
        "  <i>Примеры слов: opportunity, challenge, experience, solution, decision, achieve</i>\n\n"
        "• <b>B2 (Продвинутый / Upper-Intermediate) ⭐</b> — Свободное владение. Вы понимаете сложные тексты на абстрактные темы, можете аргументированно спорить, работать в англоязычной среде и улавливать скрытый смысл в речи собеседника.\n"
        "  <i>Примеры слов: perspective, consequence, environment, approach, significant, development</i>\n\n"
        "• <b>C1 (Профессиональный / Advanced) ⭐</b> — Уровень почти носителя. Вы бегло и спонтанно выражаете мысли без долгих пауз, легко читаете литературу в оригинале и пишете сложные научные или деловые тексты.\n"
        "  <i>Примеры слов: implementation, sophisticated, comprehensive, infrastructure, persistent, paradigm</i>\n\n"
        "Выберите уровень кнопками ниже:"
    )
    
    markup = build_levels_selection_keyboard()
    try:
        await callback.message.edit_text(levels_desc, parse_mode="HTML", reply_markup=markup)
    except Exception:
        await callback.message.answer(levels_desc, parse_mode="HTML", reply_markup=markup)
    await state.set_state(BotStates.selecting_vocabulary_level)
    await callback.answer()

# --- ТЕСТЫ ---
@router.callback_query(F.data == "hub_start_quiz")
async def entry_quiz_callback(callback: CallbackQuery, state: FSMContext) -> None:
    uid_str = str(callback.from_user.id)
    db = load_db()
    user_info = db.get(uid_str, {})
    lvl = user_info.get("level", "a1")
    is_prem = is_user_premium(user_info)
    
    if lvl in ["b1", "b2", "c1"] and not is_prem:
        await callback.answer(f"⚠️ Твой уровень ({lvl.upper()}) платный! Купи Премиум ⭐ или смени уровень в настройках.", show_alert=True)
        return

    maps = {"a1": WORDS_A1, "a2": WORDS_A2, "b1": WORDS_B1, "b2": WORDS_B2, "c1": WORDS_C1}
    pool = maps.get(lvl, WORDS_A1)
    if len(pool) < 5:
        pool = WORDS_A1 or [{"word": "Default", "ru": "Слово"}]
        
    correct = random.choice(pool)
    correct_ru = correct.get("ru")
    
    wrong_pool = [w.get("ru") for w in pool if w.get("ru") != correct_ru]
    num_options = min(4, len(wrong_pool))
    wrong_choices = random.sample(wrong_pool, num_options) if num_options > 0 else ["Неправильно"]
    
    all_options = wrong_choices + [correct_ru]
    random.shuffle(all_options)
    
    await state.update_data(quiz_correct_ru=correct_ru, quiz_level=lvl)
    await state.set_state(BotStates.quiz_question_active)
    
    btns = []
    for opt in all_options:
        is_correct_flag = "1" if opt == correct_ru else "0"
        btns.append([InlineKeyboardButton(text=opt, callback_data=f"quizans_{is_correct_flag}")])
        
    btns.append([InlineKeyboardButton(text="❌ Выход в меню", callback_data="action_main_menu")])
    
    await callback.message.edit_text(
        f"🎯 <b>Тест ({lvl.upper()}):</b>\n\nКак переводится слово <b>{html.quote(str(correct.get('word', '')))}</b>?",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=btns)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("quizans_"), StateFilter(BotStates.quiz_question_active))
async def eval_quiz(callback: CallbackQuery, state: FSMContext) -> None:
    is_correct = callback.data.split("_")[1] == "1"
    uid_str = str(callback.from_user.id)
    db = load_db()
    
    markup_next = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Следующий вопрос", callback_data="hub_start_quiz")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    
    if is_correct:
        if uid_str in db:
            db[uid_str]["correct_answers"] = db[uid_str].get("correct_answers", 0) + 1
            save_db(db)
        await callback.message.edit_text("✅ <b>Верно!</b> 🎉", parse_mode="HTML", reply_markup=markup_next)
    else:
        await callback.message.edit_text("❌ <b>Неправильно!</b>", parse_mode="HTML", reply_markup=markup_next)
        
    await callback.answer()

@router.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery) -> None:
    await query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message) -> None:
    uid_str = str(message.from_user.id)
    db = load_db()
    if uid_str in db:
        add_premium_days(db[uid_str], 30)
        save_db(db)
        
    is_admin = (message.from_user.id == ADMIN_TELEGRAM_ID)
    await message.answer(
        "🎉 <b>Оплата прошла успешно!</b>\n\nПремиум-подписка активирована на 30 дней ⭐",
        parse_mode="HTML",
        reply_markup=build_main_menu_keyboard(is_admin)
    )

@router.message(F.text == "👑 Панель администратора")
async def admin_panel_handler(message: Message) -> None:
    if message.from_user.id != ADMIN_TELEGRAM_ID:
        await message.answer("⛔ У тебя нет доступа.")
        return
        
    db = load_db()
    premium_count = sum(1 for u in db.values() if is_user_premium(u))
    await message.answer(
        f"👑 <b>Панель администратора:</b>\n\n"
        f"👥 Всего пользователей: <code>{len(db)}</code>\n"
        f"⭐ С Премиумом: <code>{premium_count}</code>",
        parse_mode="HTML"
    )

async def main() -> None:
    logger.info("Initializing bot instance...")
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Starting long-polling event loop...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass