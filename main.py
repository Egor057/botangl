import asyncio
import logging
import sys
import json
import os
import random
import shutil
from datetime import datetime, timedelta
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
    do_GET = lambda self: (
        self.send_response(200),
        self.send_header("Content-type", "text/plain; charset=utf-8"),
        self.end_headers(),
        self.wfile.write(b"LanguageBotCore Web Service is active and fully operational 24/7!")
    )

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

# =============================================================================
# ВНЕШНИЕ ИМПОРТЫ СЛОВАРЕЙ И БАЗ ДАННЫХ
# =============================================================================

try:
    from vocabulary_grammar import EXTENDED_GRAMMAR_DATABASE
except ImportError:
    EXTENDED_GRAMMAR_DATABASE = {}

try:
    from vocabulary_homework import HOMEWORK_DATABASE
except ImportError:
    HOMEWORK_DATABASE = {}

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

# =============================================================================
# ИМПОРТЫ AIOGRAM 3.X И МИДЛВАРЕЙ
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

router = Router()

BOT_TOKEN = "9084719584:AAE4LeWAMwUm1ynXJeMlKxZxaApC65UhkDg"
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

# =============================================================================
# МЕНЕДЖЕР БАЗЫ ДАННЫХ И ПРЕМИУМ-УТИЛИТЫ
# =============================================================================

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

# =============================================================================
# МАШИНА СОСТОЯНИЙ (FSM STATES)
# =============================================================================

class BotStates(StatesGroup):
    selecting_vocabulary_level = State()
    active_learning_session = State()
    quiz_question_active = State()
    detective_game_active = State()
    trainer_session_active = State()
    travel_mode_active = State()
    chat_sim_active = State()
    adventure_active = State()

# =============================================================================
# КЛАВИАТУРЫ
# =============================================================================

def build_main_menu_keyboard(is_admin: bool = False) -> ReplyKeyboardMarkup:
    # Убрали отдельную кнопку рефералки, оставили в премиум-разделе
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

def build_premium_hub_keyboard() -> InlineKeyboardMarkup:
    """Меню внутри Премиума с тремя подблоками по запросу пользователя."""
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

def build_learning_actions_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➡️ Следующее слово", callback_data="action_next_word")],
            [InlineKeyboardButton(text="🔤 Изменить уровень", callback_data="action_change_level")],
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

def build_games_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🕵️‍♂️ Детективное расследование", callback_data="game_detective_start")],
            [InlineKeyboardButton(text="🧩 Мини-квиз слов", callback_data="game_miniquiz_start")],
            [InlineKeyboardButton(text="⭐ Премиум-аркада *", callback_data="game_premium_arcade")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
        ]
    )

# =============================================================================
# ОБРАБОТЧИКИ КОМАНД И СООБЩЕНИЙ
# =============================================================================

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
                        f"Всего приглашено друзей: <b>{len(database[ref_id]['invited_users'])}</b>. Зайдите в раздел «⭐ Купить Премиум» -> «Вывести друзей», чтобы забрать награду!"
                    )
                except Exception:
                    pass
                    
        save_db(database)

    is_admin = (message.from_user.id == ADMIN_TELEGRAM_ID)
    await message.answer(
        f"👋 Здравствуй, <b>{html.quote(message.from_user.first_name)}</b>!\n\n"
        f"Добро пожаловать в бота <b>lang-bot2</b>.\n"
        f"Все функции и реферальная система теперь доступны прямо через меню Премиума!",
        parse_mode="HTML",
        reply_markup=build_main_menu_keyboard(is_admin)
    )

# =============================================================================
# ПРЕМИУМ ХАБ (ВКЛЮЧАЕТ ПОКУПКУ, ВЫВОД ДРУЗЕЙ И РЕФЕРАЛЬНУЮ ССЫЛКУ)
# =============================================================================

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
            description="Разблокирует уровни B1, B2, C1, премиум-тренажеры и эксклюзивные функции на 30 дней!",
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
        
        # Обновляем экран вывода
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

# =============================================================================
# ПРОФИЛЬ И СТАТИСТИКА
# =============================================================================

@router.message(F.text == "👤 Профиль и Статистика")
async def handle_profile_request(message: Message) -> None:
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
    
    await message.answer(
        f"📊 <b>Твой профиль и статистика:</b>\n\n"
        f"👤 Имя: {html.quote(message.from_user.first_name)}\n"
        f"📈 Уровень: <code>{info.get('level', 'a1').upper()}</code>\n"
        f"💎 Статус подписки: {sub_status}\n"
        f"👥 Приглашено друзей: <b>{invited_count}</b>\n"
        f"📚 Выучено карточек: {info.get('words_learned', 0)}\n"
        f"🎯 Правильных ответов в тестах: {info.get('correct_answers', 0)}\n"
        f"📅 Дата регистрации: {info.get('joined_date', 'Н/Д')}",
        parse_mode="HTML"
    )

# =============================================================================
# ОСТАЛЬНОЙ ФУНКЦИОНАЛ (Слова, Тесты, Грамматика, Игры, ДЗ)
# =============================================================================

@router.message(F.text == "📖 Справочник падежей")
async def handle_grammar_menu(message: Message) -> None:
    await message.answer(
        "📚 <b>Справочник падежей и грамматики:</b>\n\nВыбери интересующий раздел из списка ниже:",
        parse_mode="HTML",
        reply_markup=build_grammar_directory_keyboard()
    )

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

@router.message(F.text == "📚 Домашнее задание")
async def homework_handler(message: Message) -> None:
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
    await callback.message.edit_text(
        "🎉 <b>Отличная работа!</b>\n\nДомашнее задание отмечено как выполненное.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
    )
    await callback.answer("Задание успешно сдано!")

@router.message(F.text == "🎮 Игры и Детектив")
async def games_menu_handler(message: Message) -> None:
    await message.answer(
        "🎮 <b>Игровой зал и детективный модуль:</b>\n\nВыбери интерактивное развлечение:",
        parse_mode="HTML",
        reply_markup=build_games_menu_keyboard()
    )

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

@router.message(F.text == "🗺 Путешествия")
async def travel_menu_handler(message: Message) -> None:
    phrases = TRAVEL_MODULE_DATA.get("phrases", [
        {"en": "Where is the nearest subway station?", "ru": "Где ближайшая станция метро?"},
        {"en": "How much does this ticket cost?", "ru": "Сколько стоит этот билет?"}
    ])
    phrases_text = "\n".join([f"• <b>{p.get('en', '')}</b> — {p.get('ru', '')}" for p in phrases])
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗺 Следующие фразы", callback_data="travel_next_set")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    await message.answer(f"🗺 <b>Путешествия:</b>\n\n{phrases_text}", parse_mode="HTML", reply_markup=markup)

@router.callback_query(F.data == "travel_next_set")
async def travel_next_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "🗺 <b>Путешествия: Набор обновлен!</b>\n\n• <b>Can I get the bill, please?</b> — Можно мне счет?\n• <b>Where is the airport?</b> — Где аэропорт?",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
    )
    await callback.answer()

@router.message(F.text == "🤖 Чат-бот сим")
async def chatsim_menu_handler(message: Message) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Начать диалог", callback_data="chatsim_start_dialog")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    await message.answer("🤖 <b>Симулятор диалогов:</b>", parse_mode="HTML", reply_markup=markup)

@router.callback_query(F.data == "chatsim_start_dialog")
async def chatsim_start_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "🤖 <b>Диалог начат:</b>\n\n— Hello! How can I help you today?",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
    )
    await callback.answer()

@router.message(F.text == "⚔️ Приключения")
async def adventure_menu_handler(message: Message) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚔️ Начать квест *", callback_data="adventure_start_quest")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    await message.answer("⚔️ <b>Текстовые приключения:</b>", parse_mode="HTML", reply_markup=markup)

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

@router.message(F.text == "⚡ Тренажер фраз")
async def trainer_menu_message(message: Message) -> None:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 Обычный тренажер", callback_data="trainer_free_block")],
        [InlineKeyboardButton(text="⭐ Премиум-тренажер *", callback_data="trainer_premium_block")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
    ])
    await message.answer("⚡ <b>Тренажер предложений:</b>", parse_mode="HTML", reply_markup=keyboard)

@router.callback_query(F.data.in_({"trainer_free_block", "trainer_premium_block"}))
async def trainer_content_handler(callback: CallbackQuery) -> None:
    is_prem = (callback.data == "trainer_premium_block")
    if is_prem:
        uid_str = str(callback.from_user.id)
        db = load_db()
        if not is_user_premium(db.get(uid_str, {})):
            await callback.answer("⚠️ Требуется Премиум-подписка ⭐!", show_alert=True)
            return
            
    text = "⭐ Премиум-тренажер активен *." if is_prem else "📖 Обычный тренажер активен."
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)
    await callback.answer()

@router.message(F.text == "📚 Учить слова")
async def entry_vocab(message: Message, state: FSMContext) -> None:
    uid_str = str(message.from_user.id)
    db = load_db()
    saved_lvl = db.get(uid_str, {}).get("level", "a1")
    
    await state.update_data(active_vocab_level=saved_lvl)
    await state.set_state(BotStates.active_learning_session)
    await message.answer(f"🔤 Загружен твой сохраненный уровень: <b>{saved_lvl.upper()}</b>", parse_mode="HTML")
    await dispatch_card(message, saved_lvl, replace=False)

@router.callback_query(F.data.startswith("setlevel_"), StateFilter(BotStates.selecting_vocabulary_level, BotStates.active_learning_session))
async def set_vocab_level(callback: CallbackQuery, state: FSMContext) -> None:
    lvl = callback.data.split("_")[1]
    uid_str = str(callback.from_user.id)
    db = load_db()
    is_prem = is_user_premium(db.get(uid_str, {}))
    
    if lvl in ["b1", "b2", "c1"] and not is_prem:
        await callback.answer(f"⚠️ Уровень {lvl.upper()} платный! Требуется Премиум-подписка ⭐.", show_alert=True)
        return
            
    if uid_str in db:
        db[uid_str]["level"] = lvl
        save_db(db)
        
    await state.update_data(active_vocab_level=lvl)
    await state.set_state(BotStates.active_learning_session)
    await callback.message.edit_text(f"✅ Установлен уровень: <b>{lvl.upper()}</b>", parse_mode="HTML")
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
            [InlineKeyboardButton(text="🔤 Изменить уровень", callback_data="action_change_level")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]
        ]
    )
    
    if replace:
        try:
            await message.edit_text(card, parse_mode="HTML", reply_markup=keyboard)
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
        
    await dispatch_card(callback.message, lvl, replace=True)
    await callback.answer()

@router.callback_query(F.data == "action_change_level")
async def change_level(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text("🔤 Выбери уровень:", parse_mode="HTML", reply_markup=build_levels_selection_keyboard())
    await state.set_state(BotStates.selecting_vocabulary_level)
    await callback.answer()

# =============================================================================
# РЕЖИМ ТЕСТОВ (4-5 ВАРИАНТОВ)
# =============================================================================

@router.message(F.text == "🎯 Режим тестов")
async def entry_quiz(message: Message, state: FSMContext) -> None:
    uid_str = str(message.from_user.id)
    db = load_db()
    user_info = db.get(uid_str, {})
    lvl = user_info.get("level", "a1")
    is_prem = is_user_premium(user_info)
    
    if lvl in ["b1", "b2", "c1"] and not is_prem:
        await message.answer(f"⚠️ Твой сохраненный уровень ({lvl.upper()}) является платным! Купи Премиум ⭐ или смени уровень в разделе «Учить слова».")
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
    
    await message.answer(
        f"🎯 <b>Тест ({lvl.upper()}):</b>\n\nКак переводится слово <b>{html.quote(str(correct.get('word', '')))}</b>?",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=btns)
    )

@router.callback_query(F.data.startswith("quizans_"), StateFilter(BotStates.quiz_question_active))
async def eval_quiz(callback: CallbackQuery, state: FSMContext) -> None:
    is_correct = callback.data.split("_")[1] == "1"
    uid_str = str(callback.from_user.id)
    db = load_db()
    
    markup_next = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Следующий вопрос", callback_data="action_next_quiz")],
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

@router.callback_query(F.data == "action_next_quiz")
async def next_quiz_question(callback: CallbackQuery, state: FSMContext) -> None:
    uid_str = str(callback.from_user.id)
    db = load_db()
    lvl = db.get(uid_str, {}).get("level", "a1")
    
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
    
    btns = []
    for opt in all_options:
        is_correct_flag = "1" if opt == correct_ru else "0"
        btns.append([InlineKeyboardButton(text=opt, callback_data=f"quizans_{is_correct_flag}")])
        
    btns.append([InlineKeyboardButton(text="❌ Выход", callback_data="action_main_menu")])
    
    await callback.message.edit_text(
        f"🎯 <b>Тест ({lvl.upper()}):</b>\n\nКак переводится слово <b>{html.quote(str(correct.get('word', '')))}</b>?",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=btns)
    )
    await callback.answer()

# =============================================================================
# НАСТРОЙКИ, ОПЛАТА И АДМИНКА
# =============================================================================

@router.message(F.text == "⚙️ Настройки")
async def settings_menu(message: Message) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Главное меню", callback_data="action_main_menu")]])
    await message.answer("⚙️ <b>Настройки бота:</b>", parse_mode="HTML", reply_markup=markup)

@router.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery) -> None:
    await query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message) -> None:
    uid_str = str(message.from_user.id)
    db = load_db()
    if uid_str in db:
        add_premium_days(db[uid_str], 30) # Покупка дает 30 дней
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

# =============================================================================
# ТОЧКА ВХОДА
# =============================================================================

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