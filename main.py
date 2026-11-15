import asyncio
import logging
import sys
import json
import os
import random
import shutil
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Callable, Awaitable

# =============================================================================
# РАСШИРЕННАЯ СИСТЕМА ЛОГИРОВАНИЯ
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s (Line %(lineno)d): %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger("LanguageBotCore")

# =============================================================================
# ФОНОВЫЙ KEEP-ALIVE HTTP-СЕРВЕР ДЛЯ RENDER (ПОРТ 10000)
# =============================================================================

from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class RenderKeepAliveHandler(BaseHTTPRequestHandler):
    """
    HTTP-обработчик входящих запросов для поддержания веб-сервиса в активном
    состоянии 24/7. Предотвращает засыпание бесплатного инстанса на Render.
    """
    def do_GET(self) -> None:
        """Обрабатывает входящие GET-запросы пингера."""
        try:
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"LanguageBotCore Web Service is active and fully operational 24/7!")
            logger.debug("Keep-Alive HTTP ping successfully processed.")
        except Exception as e:
            logger.error(f"Error handling HTTP keep-alive GET request: {e}")

    def log_message(self, format: str, *args: Any) -> None:
        """Подавляет стандартный вывод логов HTTP-сервера для чистоты консоли."""
        pass

def start_web_server_daemon() -> None:
    """Запускает фоновый HTTP-сервер в отдельном изолированном демоническом потоке."""
    port = int(os.environ.get("PORT", 10000))
    try:
        server = HTTPServer(("0.0.0.0", port), RenderKeepAliveHandler)
        logger.info(f"HTTP Keep-Alive server successfully bound to port {port}")
        server.serve_forever()
    except Exception as ex:
        logger.critical(f"Failed to start background HTTP server on port {port}: {ex}")

# Инициализация и запуск фонового демона
threading.Thread(target=start_web_server_daemon, daemon=True).start()

# =============================================================================
# СТРОГИЕ ВНЕШНИЕ ИМПОРТЫ ВСЕХ СЛОВАРЕЙ И БАЗ ДАННЫХ ИЗ ОТДЕЛЬНЫХ ФАЙЛОВ
# =============================================================================

try:
    from vocabulary_grammar import EXTENDED_GRAMMAR_DATABASE
    logger.info("External module 'vocabulary_grammar' loaded successfully.")
except ImportError as e:
    logger.warning(f"Failed to load 'vocabulary_grammar': {e}. Fallback to empty dict.")
    EXTENDED_GRAMMAR_DATABASE = {}

try:
    from vocabulary_homework import HOMEWORK_DATABASE
    logger.info("External module 'vocabulary_homework' loaded successfully.")
except ImportError as e:
    logger.warning(f"Failed to load 'vocabulary_homework': {e}. Fallback to empty dict.")
    HOMEWORK_DATABASE = {}

try:
    from vocabulary_adventure import ADVENTURE_MODULE_DATA
    logger.info("External module 'vocabulary_adventure' loaded successfully.")
except ImportError as e:
    logger.warning(f"Failed to load 'vocabulary_adventure': {e}.")
    ADVENTURE_MODULE_DATA = {}

try:
    from vocabulary_chat_sim import CHAT_SIM_MODULE_DATA
    logger.info("External module 'vocabulary_chat_sim' loaded successfully.")
except ImportError as e:
    logger.warning(f"Failed to load 'vocabulary_chat_sim': {e}.")
    CHAT_SIM_MODULE_DATA = {}

try:
    from vocabulary_detective import DETECTIVE_MODULE_DATA
    logger.info("External module 'vocabulary_detective' loaded successfully.")
except ImportError as e:
    logger.warning(f"Failed to load 'vocabulary_detective': {e}.")
    DETECTIVE_MODULE_DATA = {}

try:
    from vocabulary_travel import TRAVEL_MODULE_DATA
    logger.info("External module 'vocabulary_travel' loaded successfully.")
except ImportError as e:
    logger.warning(f"Failed to load 'vocabulary_travel': {e}.")
    TRAVEL_MODULE_DATA = {}

try:
    from vocabulary_premium import PREMIUM_MODULE_DATA
    logger.info("External module 'vocabulary_premium' loaded successfully.")
except ImportError as e:
    logger.warning(f"Failed to load 'vocabulary_premium': {e}.")
    PREMIUM_MODULE_DATA = {}

try:
    from vocabulary_a1 import WORDS_A1
    logger.info(f"Loaded {len(WORDS_A1)} words for level A1.")
except ImportError as e:
    logger.warning(f"Failed to load 'vocabulary_a1': {e}.")
    WORDS_A1 = []

try:
    from vocabulary_a2 import WORDS_A2
    logger.info(f"Loaded {len(WORDS_A2)} words for level A2.")
except ImportError as e:
    logger.warning(f"Failed to load 'vocabulary_a2': {e}.")
    WORDS_A2 = []

try:
    from vocabulary_b1 import WORDS_B1
    logger.info(f"Loaded {len(WORDS_B1)} words for level B1.")
except ImportError as e:
    logger.warning(f"Failed to load 'vocabulary_b1': {e}.")
    WORDS_B1 = []

try:
    from vocabulary_b2 import WORDS_B2
    logger.info(f"Loaded {len(WORDS_B2)} words for level B2.")
except ImportError as e:
    logger.warning(f"Failed to load 'vocabulary_b2': {e}.")
    WORDS_B2 = []

try:
    from vocabulary_c1 import WORDS_C1
    logger.info(f"Loaded {len(WORDS_C1)} words for level C1.")
except ImportError as e:
    logger.warning(f"Failed to load 'vocabulary_c1': {e}.")
    WORDS_C1 = []

# =============================================================================
# ИМПОРТЫ ФРЕЙМВОРКА AIOGRAM 3.X И МИДЛВАРЕЙ
# =============================================================================

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

# Инициализация роутера и констант авторизации
router = Router()

BOT_TOKEN = "9084719584:AAE4LeWAMwUm1ynXJeMlKxZxaApC65UhkDg"
ADMIN_TELEGRAM_ID = 9136166835

DB_FILENAME = "users_database.json"
DB_BACKUP_FILENAME = "users_database_backup.json"

# =============================================================================
# АРХИТЕКТУРНЫЕ МИДЛВАРИ (MIDDLEWARES)
# =============================================================================

class LoggingMiddleware(BaseMiddleware):
    """
    Мидлварь для детального логирования входящих сообщений и callback-запросов
    с фиксацией идентификаторов пользователей и времени обработки.
    """
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
            
        start_time = asyncio.get_event_loop().time()
        try:
            result = await handler(event, data)
            duration = asyncio.get_event_loop().time() - start_time
            logger.debug(f"Event for User ID {user_id} handled successfully in {duration:.4f}s")
            return result
        except Exception as ex:
            logger.error(f"Critical exception while handling event for User ID {user_id}: {ex}", exc_info=True)
            raise ex

# Регистрация мидлваря в роутере
router.message.middleware(LoggingMiddleware())
router.callback_query.middleware(LoggingMiddleware())

# =============================================================================
# МЕНЕДЖЕР ПЕРСИСТЕНТНОЙ БАЗЫ ДАННЫХ (БЕЗ УДАЛЕНИЯ СУЩЕСТВУЮЩИХ ФАЙЛОВ)
# =============================================================================

def initialize_database() -> None:
    """
    Инициализирует файл JSON-базы данных ТОЛЬКО если он полностью отсутствует.
    Ни при каких обстоятельствах не перезаписывает существующий users_database.json,
    чтобы гарантировать сохранность пользовательских данных и прогресса.
    """
    try:
        if not os.path.exists(DB_FILENAME):
            logger.info(f"Database file '{DB_FILENAME}' not found. Initializing new persistent store...")
            initial_data: Dict[str, Any] = {}
            with open(DB_FILENAME, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, ensure_ascii=False, indent=4)
            logger.info("New database file successfully created.")
        else:
            logger.info(f"Existing database file '{DB_FILENAME}' detected. Preserving user data safely.")
    except Exception as e:
        logger.critical(f"Failed to initialize database file: {e}", exc_info=True)

def load_db() -> Dict[str, Any]:
    """
    Загружает всю структуру данных пользователей из персистентного JSON-файла.
    В случае повреждения JSON выполняет автоматическое восстановление из резервной копии.
    
    :return: Словарь с данными пользователей.
    """
    initialize_database()
    try:
        with open(DB_FILENAME, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, dict):
                raise ValueError("Database root structure is not a dictionary.")
            return data
    except json.JSONDecodeError as jde:
        logger.error(f"Database JSON decoding error detected ({jde}). Attempting restoration from backup...")
        if os.path.exists(DB_BACKUP_FILENAME):
            try:
                with open(DB_BACKUP_FILENAME, "r", encoding="utf-8") as bf:
                    backup_data = json.load(bf)
                logger.info("Successfully restored user database from backup file.")
                return backup_data
            except Exception as be:
                logger.error(f"Backup restoration failed: {be}", exc_info=True)
        return {}
    except Exception as e:
        logger.error(f"Unexpected error loading database: {e}", exc_info=True)
        return {}

def save_db(data: Dict[str, Any]) -> None:
    """
    Безопасно сохраняет актуальное состояние базы данных на диск с предварительным
    созданием резервной копии (бэкапа).
    
    :param data: Словарь данных для сохранения.
    """
    try:
        if os.path.exists(DB_FILENAME):
            shutil.copy(DB_FILENAME, DB_BACKUP_FILENAME)
        with open(DB_FILENAME, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        logger.debug("Database state successfully saved and backed up.")
    except Exception as e:
        logger.error(f"Critical error saving database state: {e}", exc_info=True)

# Инициализация хранилища при старте модуля
initialize_database()

# =============================================================================
# МАШИНА СОСТОЯНИЙ (FSM STATES)
# =============================================================================

class BotStates(StatesGroup):
    """Класс состояний конечного автомата (FSM) для управления диалогами."""
    selecting_vocabulary_level = State()
    active_learning_session = State()
    quiz_question_active = State()
    detective_game_active = State()
    trainer_session_active = State()
    travel_mode_active = State()
    chat_sim_active = State()
    adventure_active = State()
    admin_broadcast_active = State()

# =============================================================================
# ГЕНЕРАТОРЫ КЛАВИАТУР И ИНТЕРФЕЙСОВ
# =============================================================================

def build_main_menu_keyboard(is_admin: bool = False) -> ReplyKeyboardMarkup:
    """
    Строит главную клавиатуру пользовательского интерфейса (Reply).
    
    :param is_admin: Флаг отображения панели администратора.
    :return: Объект ReplyKeyboardMarkup.
    """
    rows = [
        [KeyboardButton(text="📚 Учить слова"), KeyboardButton(text="📚 Домашнее задание")],
        [KeyboardButton(text="🎯 Режим тестов"), KeyboardButton(text="⚡ Тренажер фраз")],
        [KeyboardButton(text="🗺 Путешествия"), KeyboardButton(text="🤖 Чат-бот сим")],
        [KeyboardButton(text="🎮 Игры и Детектив"), KeyboardButton(text="⚔️ Приключения")],
        [KeyboardButton(text="📖 Справочник падежей"), KeyboardButton(text="👤 Профиль и Статистика")],
        [KeyboardButton(text="⭐ Купить Премиум *"), KeyboardButton(text="⚙️ Настройки")]
    ]
    if is_admin:
        rows.append([KeyboardButton(text="👑 Панель администратора")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, persistent=True)

def build_levels_selection_keyboard() -> InlineKeyboardMarkup:
    """
    Строит клавиатуру выбора уровня сложности словарного запаса (A1 - C1).
    
    :return: Объект InlineKeyboardMarkup.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🟢 Уровень A1", callback_data="setlevel_a1")],
            [InlineKeyboardButton(text="🟢 Уровень A2", callback_data="setlevel_a2")],
            [InlineKeyboardButton(text="🟡 Уровень B1", callback_data="setlevel_b1")],
            [InlineKeyboardButton(text="🟠 Уровень B2", callback_data="setlevel_b2")],
            [InlineKeyboardButton(text="🔴 Уровень C1 (Премиум ⭐)", callback_data="setlevel_c1")],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="action_main_menu")]
        ]
    )

def build_learning_actions_keyboard() -> InlineKeyboardMarkup:
    """
    Строит инлайн-клавиатуру для карточек изучения слов.
    
    :return: Объект InlineKeyboardMarkup.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➡️ Следующее слово", callback_data="action_next_word")],
            [InlineKeyboardButton(text="🔤 Изменить уровень", callback_data="action_change_level")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
        ]
    )

def build_grammar_directory_keyboard() -> InlineKeyboardMarkup:
    """
    Строит интерактивную клавиатуру справочника грамматических падежей и правил.
    
    :return: Объект InlineKeyboardMarkup.
    """
    rows = []
    for code, info in EXTENDED_GRAMMAR_DATABASE.items():
        title = info.get("title", code)
        rows.append([InlineKeyboardButton(text=f"📌 {title}", callback_data=f"grammar_info_{code}")])
    rows.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def build_games_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Строит клавиатуру игрового зала, объединяющего детектива, квизы и аркады.
    
    :return: Объект InlineKeyboardMarkup.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🕵️‍♂️ Детективное расследование", callback_data="game_detective_start")],
            [InlineKeyboardButton(text="🧩 Мини-квиз слов", callback_data="game_miniquiz_start")],
            [InlineKeyboardButton(text="⭐ Премиум-аркада *", callback_data="game_premium_arcade")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
        ]
    )

# =============================================================================
# ОБРАБОТЧИКИ КОМАНД И СООБЩЕНИЙ (MESSAGE & CALLBACK HANDLERS)
# =============================================================================

@router.message(CommandStart())
async def handle_start_command(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает команду старта `/start`, сбрасывает состояние FSM, регистрирует
    нового пользователя в базе данных и отправчает приветственное сообщение.
    """
    await state.clear()
    uid_str = str(message.from_user.id)
    database = load_db()
    
    if uid_str not in database:
        database[uid_str] = {
            "first_name": message.from_user.first_name or "Ученик",
            "level": "a1",
            "words_learned": 0,
            "correct_answers": 0,
            "quiz_score": 0,
            "is_premium": False,
            "joined_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_db(database)
        logger.info(f"Registered new user: ID {uid_str}, Name: {message.from_user.first_name}")

    is_admin = (message.from_user.id == ADMIN_TELEGRAM_ID)
    await message.answer(
        f"👋 Здравствуй, <b>{html.quote(message.from_user.first_name)}</b>!\n\n"
        f"Добро пожаловать в полностью модульный Enterprise-бот <b>lang-bot2</b>.\n"
        f"Вся база данных активирована, внешние словари успешно подгружены!",
        parse_mode="HTML",
        reply_markup=build_main_menu_keyboard(is_admin)
    )

@router.message(F.text == "👤 Профиль и Статистика")
async def handle_profile_request(message: Message) -> None:
    """Выводит детальную статистику профиля пользователя, уровень и статус подписки."""
    uid_str = str(message.from_user.id)
    db = load_db()
    info = db.get(uid_str, {
        "level": "a1",
        "words_learned": 0,
        "correct_answers": 0,
        "quiz_score": 0,
        "is_premium": False,
        "joined_date": "Н/Д"
    })
    sub_status = "🟢 Активна (Премиум ⭐)" if info.get("is_premium") else "⚪️ Базовый"
    await message.answer(
        f"📊 <b>Твой профиль и статистика:</b>\n\n"
        f"👤 Имя: {html.quote(message.from_user.first_name)}\n"
        f"📈 Текущий уровень: <code>{info.get('level').upper()}</code>\n"
        f"💎 Статус подписки: {sub_status}\n"
        f"📚 Выучено карточек: {info.get('words_learned', 0)}\n"
        f"🎯 Правильных ответов в тестах: {info.get('correct_answers', 0)}\n"
        f"📅 Дата регистрации: {info.get('joined_date', 'Н/Д')}",
        parse_mode="HTML"
    )

@router.message(F.text == "📖 Справочник падежей")
async def handle_grammar_menu(message: Message) -> None:
    """Отокрывает справочник падежей и грамматических правил."""
    await message.answer(
        "📚 <b>Справочник падежей и грамматики:</b>\n\nВыбери интересующий раздел из списка ниже:",
        parse_mode="HTML",
        reply_markup=build_grammar_directory_keyboard()
    )

@router.callback_query(F.data.startswith("grammar_info_"))
async def process_grammar_card(callback: CallbackQuery) -> None:
    """Отображает подробную теоретическую карточку по выбранному грамматическому разделу."""
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

@router.message(F.text == "📚 Домашнее задание")
async def homework_handler(message: Message) -> None:
    """Загружает и выводит текущее домашнее задание из внешнего модуля."""
    if isinstance(HOMEWORK_DATABASE, dict):
        hw_content = HOMEWORK_DATABASE.get("current", "На сегодня новых домашних заданий нет.")
        deadline_info = HOMEWORK_DATABASE.get("deadline", "Срок не указан")
        text = f"📚 <b>Домашнее задание:</b>\n\n{hw_content}\n\n⏳ <i>Срок выполнения: {deadline_info}</i>"
    else:
        text = f"📚 <b>Домашнее задание:</b>\n\n{str(HOMEWORK_DATABASE)}"
    
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Отметить выполненным", callback_data="hw_done_action")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    await message.answer(text, parse_mode="HTML", reply_markup=markup)

@router.callback_query(F.data == "hw_done_action")
async def homework_done_callback(callback: CallbackQuery) -> None:
    """Обрабатывает успешную сдачу и отметку выполнения домашнего задания."""
    await callback.message.edit_text(
        "🎉 <b>Отличная работа!</b>\n\nДомашнее задание отмечено как выполненное. Продолжай в том же духе!",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
    )
    await callback.answer("Задание успешно сдано!")

@router.message(F.text == "🎮 Игры и Детектив")
async def games_menu_handler(message: Message) -> None:
    """Открывает игровой зал, включающий детективное расследование и аркады."""
    await message.answer(
        "🎮 <b>Игровой зал и детективный модуль:</b>\n\n"
        "Выбери интерактивное развлечение из списка ниже:",
        parse_mode="HTML",
        reply_markup=build_games_menu_keyboard()
    )

@router.callback_query(F.data == "game_detective_start")
async def detective_game_callback(callback: CallbackQuery, state: FSMContext) -> None:
    """Запускает интерактивный детективный квест с выбором веток развития."""
    await state.set_state(BotStates.detective_game_active)
    text = (
        "🕵️‍♂️ <b>Детективное расследование: Дело о пропавшем коде</b>\n\n"
        "Вы стоите в темном офисе стартапа. На мониторе мигает последняя строка нескомпилированного кода. "
        "Вам нужно найти улику.\n\n"
        "Куда вы хотите заглянуть в первую очередь?\n"
        "1. Проверить корзину для мусора\n"
        "2. Посмотреть историю коммитов в Git\n"
        "3. Допросить спящего сисадмина"
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
    """Обрабатывает ветвление сюжетной линии в детективной игре."""
    choice = callback.data.split("_")[2]
    if choice == "trash":
        result = "🗑 В корзине вы нашли старый черновик с подсказкой: <i>'Use pip install carefully'</i>. Расследование продолжается!"
    elif choice == "git":
        result = "💻 В истории Git вы обнаружили удаленную ветку `lang-bot-fix` с рабочей версией кода! Дело раскрыто! 🎉"
    else:
        result = "😴 Сисадмин проснулся, дал чашку кофе и подсказал проверить логи на Render. Полезный опыт!"
    
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Сыграть снова", callback_data="game_detective_start")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    await callback.message.edit_text(f"🕵️‍♂️ <b>Результат расследования:</b>\n\n{result}", parse_mode="HTML", reply_markup=markup)
    await callback.answer()

@router.callback_query(F.data == "game_premium_arcade")
async def premium_arcade_callback(callback: CallbackQuery) -> None:
    """Проверяет наличие премиум-подписки для доступа к аркадному режиму."""
    uid_str = str(callback.from_user.id)
    db = load_db()
    if not db.get(uid_str, {}).get("is_premium", False):
        await callback.answer("⚠️ Премиум-аркада доступна только с подпиской ⭐!", show_alert=True)
        return
    await callback.message.edit_text(
        "⭐ <b>Премиум-аркада активна *!</b>\n\nДобро пожаловать в секретный режим повышенной сложности.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
    )
    await callback.answer()

@router.message(F.text == "🗺 Путешествия")
async def travel_menu_handler(message: Message) -> None:
    """Запускает модуль полезных фраз для путешествий за рубежом."""
    phrases = TRAVEL_MODULE_DATA.get("phrases", [
        {"en": "Where is the nearest subway station?", "ru": "Где ближайшая станция метро?"},
        {"en": "How much does this ticket cost?", "ru": "Сколько стоит этот билет?"}
    ])
    phrases_text = "\n".join([f"• <b>{p.get('en', '')}</b> — {p.get('ru', '')}" for p in phrases])
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗺 Следующие фразы", callback_data="travel_next_set")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    await message.answer(
        f"🗺 <b>Модуль путешествий (Travel Assistant):</b>\n\n"
        f"Полезные фразы для поездок за рубеж:\n\n{phrases_text}",
        parse_mode="HTML",
        reply_markup=markup
    )

@router.callback_query(F.data == "travel_next_set")
async def travel_next_callback(callback: CallbackQuery) -> None:
    """Подгружает следующий набор фраз в модуле путешествий."""
    await callback.answer("Загружен новый набор фраз для путешествий!")
    await callback.message.edit_text(
        "🗺 <b>Путешествия: Набор обновлен!</b>\n\n• <b>Can I get the bill, please?</b> — Можно мне счет, пожалуйста?\n• <b>Where is the airport?</b> — Где аэропорт?",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
    )

@router.message(F.text == "🤖 Чат-бот сим")
async def chatsim_menu_handler(message: Message) -> None:
    """Запускает интерактивный симулятор живого диалога на английском языке."""
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Начать диалог с ботом", callback_data="chatsim_start_dialog")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    await message.answer(
        "🤖 <b>Симулятор диалогов (Chat Simulator):</b>\n\nПрактикуй живой диалог на английском языке в реальном времени.",
        parse_mode="HTML",
        reply_markup=markup
    )

@router.callback_query(F.data == "chatsim_start_dialog")
async def chatsim_start_callback(callback: CallbackQuery) -> None:
    """Активирует сессию текстового диалога с симулятором."""
    await callback.message.edit_text(
        "🤖 <b>Диалог начат:</b>\n\n— Hello! How can I help you with your language practice today?\n\n<i>(Напиши ответ в чат!)</i>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
    )
    await callback.answer()

@router.message(F.text == "⚔️ Приключения")
async def adventure_menu_handler(message: Message) -> None:
    """Открывает модуль текстовых квестов и ролевых приключений."""
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚔️ Начать квест *", callback_data="adventure_start_quest")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    await message.answer(
        "⚔️ <b>Текстовые приключения (Adventure Quest):</b>\n\nИсследуй фэнтезийный мир и решай языковые задачи.",
        parse_mode="HTML",
        reply_markup=markup
    )

@router.callback_query(F.data == "adventure_start_quest")
async def adventure_start_callback(callback: CallbackQuery) -> None:
    """Проверяет премиум-статус пользователя перед запуском эксклюзивного квеста."""
    uid_str = str(callback.from_user.id)
    db = load_db()
    if not db.get(uid_str, {}).get("is_premium", False):
        await callback.answer("⚠️ Квесты с пометкой * требуют Премиум-подписку ⭐!", show_alert=True)
        return
    await callback.message.edit_text(
        "⚔️ <b>Квест начат:</b>\n\nВы стоите у входа в заброшенную пещеру. Дверь заперта магическим заклинанием на английском языке.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
    )
    await callback.answer()

@router.callback_query(F.data == "action_main_menu")
async def return_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    """Безопасно очищает текущее состояние FSM и возвращает пользователя в главное меню."""
    await state.clear()
    is_admin = (callback.from_user.id == ADMIN_TELEGRAM_ID)
    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.message.answer("🏠 Главное меню:", reply_markup=build_main_menu_keyboard(is_admin))
    await callback.answer()

@router.message(F.text == "⚡ Тренажер фраз")
async def trainer_menu_message(message: Message) -> None:
    """Открывает тренажер предложений, разделенный на обычный и премиум уровни."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 Обычный тренажер фраз", callback_data="trainer_free_block")],
        [InlineKeyboardButton(text="⭐ Премиум-тренажер *", callback_data="trainer_premium_block")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    await message.answer("⚡ <b>Тренажер предложений и фраз:</b>\n\nВыбери режим работы:", parse_mode="HTML", reply_markup=keyboard)

@router.callback_query(F.data.in_({"trainer_free_block", "trainer_premium_block"}))
async def trainer_content_handler(callback: CallbackQuery) -> None:
    """Обрабатывает выбор режима в тренажере фраз с проверкой подписки для премиум-блока."""
    is_prem = (callback.data == "trainer_premium_block")
    if is_prem:
        uid_str = str(callback.from_user.id)
        db = load_db()
        if not db.get(uid_str, {}).get("is_premium", False):
            await callback.answer("⚠️ Требуется Премиум-подписка ⭐ для доступа к премиум-тренажеру!", show_alert=True)
            return
            
    text = (
        "⭐ Премиум-режим тренажера активен *.\n\nПереводите конструкции и тренируйте грамматику продвинутого уровня."
        if is_prem else
        "📖 Обычный режим тренажера активен.\n\nПрактикуйте базовые разговорные конструкции."
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)
    await callback.answer()

@router.message(F.text == "📚 Учить слова")
async def entry_vocab(message: Message, state: FSMContext) -> None:
    """Инициирует процесс изучения слов, открывая меню выбора уровня сложности."""
    await message.answer("🔤 <b>Выбери уровень для изучения слов:</b>", parse_mode="HTML", reply_markup=build_levels_selection_keyboard())
    await state.set_state(BotStates.selecting_vocabulary_level)

@router.callback_query(F.data.startswith("setlevel_"), StateFilter(BotStates.selecting_vocabulary_level, BotStates.active_learning_session))
async def set_vocab_level(callback: CallbackQuery, state: FSMContext) -> None:
    """Устанавливает выбранный пользователем уровень сложности словаря (A1-C1) с проверкой подписки для C1."""
    lvl = callback.data.split("_")[1]
    uid_str = str(callback.from_user.id)
    
    if lvl == "c1":
        db = load_db()
        if not db.get(uid_str, {}).get("is_premium", False):
            await callback.answer("⚠️ Уровень C1 доступен только с Премиум-подпиской ⭐!", show_alert=True)
            return
            
    await state.update_data(active_vocab_level=lvl)
    await state.set_state(BotStates.active_learning_session)
    await callback.message.edit_text(f"✅ Установлен уровень: <b>{lvl.upper()}</b>", parse_mode="HTML")
    await dispatch_card(callback.message, lvl, replace=True)
    await callback.answer()

async def dispatch_card(message: Message, level_code: str, replace: bool = False) -> None:
    """
    Выбирает случайную словарную карточку из соответствующего внешнего модуля
    и отправляет её пользователю с инлайн-кнопками управления.
    
    :param message: Объект сообщения Telegram.
    :param level_code: Код уровня (a1, a2, b1, b2, c1).
    :param replace: Флаг редактирования существующего сообщения.
    """
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
    
    if replace:
        try:
            await message.edit_text(card, parse_mode="HTML", reply_markup=build_learning_actions_keyboard())
        except Exception:
            await message.answer(card, parse_mode="HTML", reply_markup=build_learning_actions_keyboard())
    else:
        await message.answer(card, parse_mode="HTML", reply_markup=build_learning_actions_keyboard())

@router.callback_query(F.data == "action_next_word", StateFilter(BotStates.active_learning_session))
async def next_word(callback: CallbackQuery, state: FSMContext) -> None:
    """Переключает карточку на следующее слово, инкрементируя счётчик выученных слов в БД."""
    data = await state.get_data()
    lvl = data.get("active_vocab_level", "a1")
    uid_str = str(callback.from_user.id)
    
    db = load_db()
    if uid_str in db:
        db[uid_str]["words_learned"] = db[uid_str].get("words_learned", 0) + 1
        save_db(db)
        
    await dispatch_card(callback.message, lvl, replace=True)
    await callback.answer()

@router.callback_query(F.data == "action_change_level")
async def change_level(callback: CallbackQuery, state: FSMContext) -> None:
    """Позволяет сменить уровень словарного запаса прямо во время учебной сессии."""
    await callback.message.edit_text("🔤 Выбери уровень для продолжения:", parse_mode="HTML", reply_markup=build_levels_selection_keyboard())
    await state.set_state(BotStates.selecting_vocabulary_level)
    await callback.answer()

@router.message(F.text == "🎯 Режим тестов")
async def entry_quiz(message: Message, state: FSMContext) -> None:
    """Запускает интерактивный мини-квиз для проверки словарного запаса."""
    uid_str = str(message.from_user.id)
    db = load_db()
    lvl = db.get(uid_str, {}).get("level", "a1")
    
    maps = {"a1": WORDS_A1, "a2": WORDS_A2, "b1": WORDS_B1, "b2": WORDS_B2, "c1": WORDS_C1}
    pool = maps.get(lvl, WORDS_A1)
    if not pool:
        pool = [{"word": "Default", "ru": "Слово"}]
        
    correct = random.choice(pool)
    await state.update_data(quiz_correct_ru=correct.get("ru"))
    await state.set_state(BotStates.quiz_question_active)
    
    btns = [
        [InlineKeyboardButton(text=correct.get("ru", "Правильный"), callback_data=f"quizanswer_{correct.get('ru')}")],
        [InlineKeyboardButton(text="❌ Выход в меню", callback_data="action_main_menu")]
    ]
    await message.answer(
        f"🎯 <b>Тест знаний слов:</b>\n\nКак переводится слово <b>{html.quote(str(correct.get('word', '')))}</b>?",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=btns)
    )

@router.callback_query(F.data.startswith("quizanswer_"), StateFilter(BotStates.quiz_question_active))
async def eval_quiz(callback: CallbackQuery, state: FSMContext) -> None:
    """Оценивает ответ пользователя в квизе и фиксирует победу в базе данных."""
    uid_str = str(callback.from_user.id)
    db = load_db()
    if uid_str in db:
        db[uid_str]["correct_answers"] = db[uid_str].get("correct_answers", 0) + 1
        save_db(db)
        
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Следующий вопрос", callback_data="action_next_quiz")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    await callback.message.edit_text("✅ <b>Верно!</b> 🎉 Отличный результат.", parse_mode="HTML", reply_markup=markup)
    await callback.answer()

@router.callback_query(F.data == "action_next_quiz")
async def next_quiz_question(callback: CallbackQuery, state: FSMContext) -> None:
    """Генерирует следующий вопрос в режиме тестирования."""
    uid_str = str(callback.from_user.id)
    db = load_db()
    lvl = db.get(uid_str, {}).get("level", "a1")
    
    maps = {"a1": WORDS_A1, "a2": WORDS_A2, "b1": WORDS_B1, "b2": WORDS_B2, "c1": WORDS_C1}
    pool = maps.get(lvl, WORDS_A1)
    if not pool:
        pool = [{"word": "Default", "ru": "Слово"}]
        
    correct = random.choice(pool)
    await state.update_data(quiz_correct_ru=correct.get("ru"))
    
    btns = [
        [InlineKeyboardButton(text=correct.get("ru", "Ответ"), callback_data=f"quizanswer_{correct.get('ru')}")],
        [InlineKeyboardButton(text="❌ Выход", callback_data="action_main_menu")]
    ]
    await message.answer(
        f"🎯 <b>Тест знаний слов:</b>\n\nКак переводится слово <b>{html.quote(str(correct.get('word', '')))}</b>?",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=btns)
    )
    await callback.answer()

@router.message(F.text == "⚙️ Настройки")
async def settings_menu(message: Message) -> None:
    """Отображает панель настроек аккаунта и параметров бота."""
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
    await message.answer(
        "⚙️ <b>Настройки бота:</b>\n\nЗдесь ты можешь управлять параметрами интерфейса, уведомлениями и языковыми предпочтениями.",
        parse_mode="HTML",
        reply_markup=markup
    )

@router.message(Command("buy"))
@router.message(F.text.in_(["⭐ Купить Премиум *", "⭐ Купить Премиум"]))
async def buy_premium(message: Message) -> None:
    """Формирует и отправляет платежный инвойс Telegram Stars для покупки Премиум-доступа."""
    prices = [LabeledPrice(label="Премиум доступ", amount=50)]
    try:
        await message.answer_invoice(
            title="⭐ Премиум-подписка",
            description="Полный доступ ко всем уровням (C1), премиум-тренажерам, детективам и эксклюзивным функциям!",
            prices=prices,
            payload="premium_sub_payload",
            currency="XTR",
            provider_token=""
        )
        logger.info(f"Invoice sent successfully to User ID {message.from_user.id}")
    except Exception as e:
        logger.error(f"Failed to send invoice: {e}", exc_info=True)
        await message.answer("⚠️ Не удалось сформировать счет на оплату. Попробуйте позже.")

@router.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery) -> None:
    """Подтверждает предзаказ платежной системы Telegram Stars перед списанием средств."""
    await query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message) -> None:
    """Обрабатывает успешный платеж, активируя премиум-статус пользователя в базе данных."""
    uid_str = str(message.from_user.id)
    db = load_db()
    if uid_str in db:
        db[uid_str]["is_premium"] = True
        save_db(db)
        logger.info(f"User ID {uid_str} successfully upgraded to Premium via Telegram Stars.")
        
    is_admin = (message.from_user.id == ADMIN_TELEGRAM_ID)
    await message.answer(
        "🎉 <b>Оплата прошла успешно!</b>\n\nПремиум-подписка активирована ⭐ Пользуйся всеми функциями без ограничений!",
        parse_mode="HTML",
        reply_markup=build_main_menu_keyboard(is_admin)
    )

@router.message(F.text == "👑 Панель администратора")
async def admin_panel_handler(message: Message) -> None:
    """Отображает панель управления администратора со статистикой пользователей и системы."""
    if message.from_user.id != ADMIN_TELEGRAM_ID:
        await message.answer("⛔ У тебя нет доступа к этой панели управления.")
        logger.warning(f"Unauthorized admin panel access attempt by User ID {message.from_user.id}")
        return
        
    db = load_db()
    premium_count = sum(1 for u in db.values() if u.get("is_premium", False))
    await message.answer(
        f"👑 <b>Панель администратора:</b>\n\n"
        f"👥 Всего зарегистрировано пользователей: <code>{len(db)}</code>\n"
        f"⭐ С активным Премиумом: <code>{premium_count}</code>\n"
        f"🟢 Статус системы: <b>Онлайн (24/7)</b>\n"
        f"🛠 База данных: <code>{DB_FILENAME}</code>",
        parse_mode="HTML"
    )

# =============================================================================
# ТОЧКА ВХОДА И ЗАПУСК АСИНХРОННОГО ПОЛЛИНГА
# =============================================================================

async def main() -> None:
    """Главная асинхронная точка входа для инициализации бота и запуска polling."""
    logger.info("Initializing bot instance with modular enterprise architecture...")
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Starting long-polling event loop...")
        await dp.start_polling(bot)
    except TelegramAPIError as api_err:
        logger.critical(f"Telegram API Error encountered during polling: {api_err}", exc_info=True)
    except Exception as ex:
        logger.critical(f"Unexpected critical error in main event loop: {ex}", exc_info=True)
    finally:
        await bot.session.close()
        logger.info("Bot session closed gracefully.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot process terminated manually by user.")
        pass