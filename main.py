import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), BaseHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

import asyncio
import datetime
import json
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
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

def get_user(user_id: int, first_name: str = "Ученик"):
    str_id = str(user_id)
    if str_id not in USERS_DB:
        USERS_DB[str_id] = {
            "name": first_name,
            "is_premium": False,
            "level": "a1",
            "points": 0,
            "words": 0,
            "tests": 0,
            "refs": 0,
            "ref_days_claimed": 0,
            "streak": 1,
            "last_word_time": 0,
            "reg_date": datetime.date.today().strftime("%d.%m.%Y"),
            "block_progress": {}
        }
        save_database()
    else:
        USERS_DB[str_id]["name"] = first_name
        if "block_progress" not in USERS_DB[str_id]:
            USERS_DB[str_id]["block_progress"] = {}
        if "ref_days_claimed" not in USERS_DB[str_id]:
            USERS_DB[str_id]["ref_days_claimed"] = 0
    return USERS_DB[str_id]

try:
    import vocabulary_a1
    import vocabulary_a2
    import vocabulary_adventure
    import vocabulary_b1
    import vocabulary_b2
    import vocabulary_c1
    import vocabulary_chat_sim
    import vocabulary_detective
    import vocabulary_grammar
    import vocabulary_homework
    import vocabulary_premium
    import vocabulary_premium_travel
    import vocabulary_reading
    import vocabulary_sprint_a1
    import vocabulary_sprint_a2
    import vocabulary_sprint_b1_categorized
    import vocabulary_sprint_b2_categorized
    import vocabulary_sprint_c1_categorized
    import vocabulary_travel
except ImportError as e:
    logger.warning(f"Предупреждение при импорте модуля: {e}")

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📚 Учить слова"),
                KeyboardButton(text="🎯 Тесты и блиц"),
            ],
            [
                KeyboardButton(text="📖 Чтение текстов"),
                KeyboardButton(text="🎮 Игры и чат"),
            ],
            [
                KeyboardButton(text="🏆 Лидерборд (500⭐)"),
                KeyboardButton(text="👤 Профиль"),
            ],
            [
                KeyboardButton(text="⭐ Купить Премиум ✨"),
            ],
        ],
        resize_keyboard=True,
    )

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    get_user(user_id, message.from_user.first_name)

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
                    "🎉 Новый ученик присоединился по вашей реферальной ссылке!\n🎁 Вам начислено +100 очков рейтинга 🚀",
                )
        except ValueError:
            pass

    welcome_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🟢 Уровень A1 (Beginner)", callback_data="start_set_a1")],
            [InlineKeyboardButton(text="🟢 Уровень A2 (Elementary)", callback_data="start_set_a2")],
            [InlineKeyboardButton(text="⭐ Уровень B1 (Intermediate - Премиум)", callback_data="start_set_b1")],
            [InlineKeyboardButton(text="⭐ Уровень B2 (Upper-Intermediate - Премиум)", callback_data="start_set_b2")],
            [InlineKeyboardButton(text="⭐ Уровень C1 (Advanced - Премиум)", callback_data="start_set_c1")],
        ]
    )

    welcome_text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "🚀 Профессиональный образовательный бот для эффективного изучения английского языка со всеми базами и модулями.\n\n"
        "🎯 **Выберите ваш текущий уровень владения английским языком**, чтобы бот адаптировал программы обучения и словари под вас:"
    )
    await message.answer(
        welcome_text, reply_markup=welcome_keyboard, parse_mode="Markdown"
    )

@dp.callback_query(F.data.startswith("start_set_"))
async def callback_start_set_level(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user(user_id, callback.from_user.first_name)
    chosen_lvl = callback.data.replace("start_set_", "")

    if chosen_lvl in ["b1", "b2", "c1"] and not user_data["is_premium"]:
        user_data["level"] = chosen_lvl
        save_database()
        await callback.message.edit_text(
            f"⭐ Вы выбрали уровень **{chosen_lvl.upper()}**.\n"
            "Обратите внимание: уровни от B1 до C1 требуют Премиум-подписки. Вы можете активировать её прямо сейчас или временно выбрать базовый уровень A1/A2.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="⭐ Купить Премиум ✨", callback_data="prem_buy_cb")],
                    [InlineKeyboardButton(text="🔄 Выбрать другой уровень", callback_data="restart_choose_lvl")]
                ]
            ),
            parse_mode="Markdown"
        )
        await callback.answer()
        return

    user_data["level"] = chosen_lvl
    save_database()

    await callback.message.delete()
    await callback.message.answer(
        f"✅ Уровень **{chosen_lvl.upper()}** успешно установлен и сохранен в вашем профиле!\n\n"
        "🔥 **Участвуйте в битве за призы!** Приглашайте друзей, учите слова из баз и забирайте главные награды:\n"
        "🥇 **1 место:** Уникальный NFT за 500 звезд!\n"
        "🥈 **2 и 🥉 3 места:** Премиум-доступ на 1 месяц бесплатно!\n\n"
        "Используйте панель управления внизу для навигации 👇",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "restart_choose_lvl")
async def restart_choose_lvl_cb(callback: types.CallbackQuery):
    welcome_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🟢 Уровень A1 (Beginner)", callback_data="start_set_a1")],
            [InlineKeyboardButton(text="🟢 Уровень A2 (Elementary)", callback_data="start_set_a2")],
            [InlineKeyboardButton(text="⭐ Уровень B1 (Intermediate - Премиум)", callback_data="start_set_b1")],
            [InlineKeyboardButton(text="⭐ Уровень B2 (Upper-Intermediate - Премиум)", callback_data="start_set_b2")],
            [InlineKeyboardButton(text="⭐ Уровень C1 (Advanced - Премиум)", callback_data="start_set_c1")],
        ]
    )
    await callback.message.edit_text(
        "🎯 **Выберите ваш текущий уровень владения английским языком:**",
        reply_markup=welcome_keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.message(F.text == "🏠 Главное меню")
async def main_menu(message: types.Message):
    await message.answer(
        "🏠 Вы вернулись в главное меню:", reply_markup=get_main_keyboard()
    )

@dp.message(F.text == "📚 Учить слова")
async def learn_words_handler(message: types.Message):
    user_data = get_user(message.from_user.id, message.from_user.first_name)
    current_level = user_data.get("level", "a1")

    if current_level in ["b1", "b2", "c1"] and not user_data["is_premium"]:
        await message.answer(
            f"⭐ Уровень **{current_level.upper()}** доступен только по Премиум-подписке!\n"
            "Вы можете изменить уровень на A1/A2 в профиле или приобрести Премиум.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="👤 В профиль (сменить уровень)", callback_data="open_profile")],
                    [InlineKeyboardButton(text="⭐ Купить Премиум ✨", callback_data="prem_buy_cb")],
                    [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")]
                ]
            ),
            parse_mode="Markdown"
        )
        return

    bp = user_data.setdefault("block_progress", {})
    block_target = 100

    p1 = min(100, int((bp.get(f"{current_level}_1", 0) / block_target) * 100))
    p2 = min(100, int((bp.get(f"{current_level}_2", 0) / block_target) * 100))
    p3 = min(100, int((bp.get(f"{current_level}_3", 0) / block_target) * 100))

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"📦 Блок 1 (Часть 1) — завершено {p1}%", callback_data=f"block_{current_level}_1")],
            [InlineKeyboardButton(text=f"📦 Блок 2 (Часть 2) — завершено {p2}%", callback_data=f"block_{current_level}_2")],
            [InlineKeyboardButton(text=f"📦 Блок 3 (Часть 3) — завершено {p3}%", callback_data=f"block_{current_level}_3")],
            [InlineKeyboardButton(text="⚡ Словарный спринт", callback_data="sprint_menu")],
            [InlineKeyboardButton(text="👤 Сменить уровень в профиле", callback_data="open_profile")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")]
        ]
    )

    await message.answer(
        f"📚 **Профессиональный словарный тренажер**\n"
        f"🎯 Текущий уровень: **{current_level.upper()}**\n\n"
        "Выберите один из трех блоков лексики для глубокого изучения и отслеживания прогресса:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.startswith("block_"))
async def callback_block_train(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user(user_id, callback.from_user.first_name)
    
    parts = callback.data.split("_")
    lvl = parts[1]
    block_num = parts[2]

    if lvl in ["b1", "b2", "c1"] and not user_data["is_premium"]:
        await callback.answer("⭐ Этот уровень доступен только по Премиум-подписке!", show_alert=True)
        return

    bp = user_data.setdefault("block_progress", {})
    key = f"{lvl}_{block_num}"
    bp[key] = bp.get(key, 0) + 5
    user_data["words"] += 5
    user_data["points"] += 25
    save_database()

    block_target = 100
    current_block_words = bp[key]
    percent = min(100, int((current_block_words / block_target) * 100))
    filled = int(percent / 10)
    progress_bar = "█" * filled + "░" * (10 - filled)

    content = f"📖 Детальный урок словаря уровня **{lvl.upper()}** (Блок {block_num}) успешно загружен из базы данных!"
    try:
        if lvl == "a1" and "vocabulary_a1" in globals():
            content = vocabulary_a1.get_lesson()
        elif lvl == "a2" and "vocabulary_a2" in globals():
            content = vocabulary_a2.get_lesson()
        elif lvl == "b1" and "vocabulary_b1" in globals():
            content = vocabulary_b1.get_lesson()
        elif lvl == "b2" and "vocabulary_b2" in globals():
            content = vocabulary_b2.get_lesson()
        elif lvl == "c1" and "vocabulary_c1" in globals():
            content = vocabulary_c1.get_lesson()
    except Exception as e:
        logger.error(f"Ошибка вызова модуля словаря: {e}")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➡️ Следующая порция слов", callback_data=f"block_{lvl}_{block_num}")],
            [InlineKeyboardButton(text="⬅️ К выбору блоков", callback_data="back_to_blocks")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")]
        ]
    )

    await callback.message.edit_text(
        f"✅ **Тренировка лексики ({lvl.upper()} — Блок {block_num}):**\n\n{content}\n\n"
        f"📊 **Прогресс блока {block_num}:** {current_block_words}/{block_target} слов ({percent}%)\n"
        f"[{progress_bar}]\n\n🚀 +25 очков зачислено в рейтинг!",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "back_to_blocks")
async def back_to_blocks_cb(callback: types.CallbackQuery):
    await callback.message.delete()
    fake_msg = callback.message
    fake_msg.from_user = callback.from_user
    await learn_words_handler(fake_msg)
    await callback.answer()

@dp.callback_query(F.data == "sprint_menu")
async def sprint_menu_cb(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚡ Спринт A1", callback_data="sprint_a1")],
            [InlineKeyboardButton(text="⚡ Спринт A2", callback_data="sprint_a2")],
            [InlineKeyboardButton(text="⭐ Спринт B1 (Премиум)", callback_data="sprint_b1")],
            [InlineKeyboardButton(text="⭐ Спринт B2 (Премиум)", callback_data="sprint_b2")],
            [InlineKeyboardButton(text="⭐ Спринт C1 (Премиум)", callback_data="sprint_c1")],
            [InlineKeyboardButton(text="⬅️ Назад к блокам", callback_data="back_to_blocks")],
        ]
    )
    await callback.message.edit_text(
        "⚡ **Выберите категорию словарного спринта:**",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("sprint_"))
async def sprint_exec_cb(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user(user_id, callback.from_user.first_name)
    sprint_type = callback.data.replace("sprint_", "")

    if sprint_type in ["b1", "b2", "c1"] and not user_data["is_premium"]:
        await callback.answer("⭐ Этот спринт доступен по Премиум-подписке!", show_alert=True)
        return

    content = "⚡ Спринт загружен!"
    try:
        if sprint_type == "a1" and "vocabulary_sprint_a1" in globals():
            content = vocabulary_sprint_a1.get_sprint()
        elif sprint_type == "a2" and "vocabulary_sprint_a2" in globals():
            content = vocabulary_sprint_a2.get_sprint()
        elif sprint_type == "b1" and "vocabulary_sprint_b1_categorized" in globals():
            content = vocabulary_sprint_b1_categorized.get_sprint()
        elif sprint_type == "b2" and "vocabulary_sprint_b2_categorized" in globals():
            content = vocabulary_sprint_b2_categorized.get_sprint()
        elif sprint_type == "c1" and "vocabulary_sprint_c1_categorized" in globals():
            content = vocabulary_sprint_c1_categorized.get_sprint()
    except Exception as e:
        logger.error(f"Ошибка спринта: {e}")

    user_data["points"] += 20
    save_database()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Еще спринт", callback_data=f"sprint_{sprint_type}")],
            [InlineKeyboardButton(text="⬅️ К списку спринтов", callback_data="sprint_menu")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")]
        ]
    )
    await callback.message.edit_text(
        f"⚡ **Словарный спринт ({sprint_type.upper()}):**\n\n{content}\n\n🚀 +20 очков зачислено!",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

QUESTIONS_POOL = [
    {"q": "Как переводится слово «Success»?", "options": [("Яблоко", False), ("Успех", True), ("Окно", False), ("Бег", False)]},
    {"q": "Как переводится слово «Travel»?", "options": [("Путешествие", True), ("Стол", False), ("Книга", False), ("Ручка", False)]},
    {"q": "Выберите правильный перевод слова «Opportunity»:", "options": [("Препятствие", False), ("Возможность", True), ("Опасность", False), ("Привычка", False)]},
    {"q": "Что означает слово «Reliable»?", "options": [("Надёжный", True), ("Скрытный", False), ("Случайный", False), ("Сложный", False)]},
    {"q": "Как переводится фраза «To make up one's mind»?", "options": [("Передумать", False), ("Принять решение", True), ("Забыть о деле", False), ("Потерять время", False)]}
]

@dp.message(F.text == "🎯 Тесты и блиц")
async def tests_handler(message: types.Message):
    await send_quiz_question(message, question_index=0, score=0)

async def send_quiz_question(event, question_index, score):
    if question_index >= len(QUESTIONS_POOL):
        user_id = event.from_user.id
        user_data = get_user(user_id, event.from_user.first_name)
        user_data["tests"] += 1
        bonus = score * 15
        user_data["points"] += bonus
        save_database()

        text = (
            f"🎯 **Тест завершен!**\n\n"
            f"🏆 Ваш результат: **{score} из {len(QUESTIONS_POOL)}** правильных ответов!\n"
            f"🚀 Начислено бонусных очков: **+{bonus}**"
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Пройти еще раз", callback_data="restart_test")],
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")]
            ]
        )
        if isinstance(event, types.Message):
            await event.answer(text, reply_markup=keyboard, parse_mode="Markdown")
        else:
            await event.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
        return

    q_data = QUESTIONS_POOL[question_index]
    buttons = []
    for opt_text, is_correct in q_data["options"]:
        cb_data = f"quiz_{question_index}_{1 if is_correct else 0}_{score}"
        buttons.append([InlineKeyboardButton(text=opt_text, callback_data=cb_data)])
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")])

    text = f"🎯 **Вопрос {question_index + 1} из {len(QUESTIONS_POOL)}:**\n\n{q_data['q']}"
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    if isinstance(event, types.Message):
        await event.answer(text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await event.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(F.data.startswith("quiz_"))
async def quiz_answer_cb(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    q_idx = int(parts[1])
    is_correct = int(parts[2])
    score = int(parts[3])

    if is_correct:
        score += 1
        await callback.answer("🎉 Верно!", show_alert=False)
    else:
        await callback.answer("❌ Неверно!", show_alert=False)

    await send_quiz_question(callback, question_index=q_idx + 1, score=score)

@dp.callback_query(F.data == "restart_test")
async def restart_test_cb(callback: types.CallbackQuery):
    await send_quiz_question(callback, question_index=0, score=0)
    await callback.answer()

@dp.message(F.text == "📖 Чтение текстов")
async def reading_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Истории и статьи", callback_data="read_stories")],
            [InlineKeyboardButton(text="✈️ Путешествия (200 слов + 25 историй)", callback_data="read_travel")],
            [InlineKeyboardButton(text="⭐ VIP-путешествия (Премиум)", callback_data="read_prem_travel")],
            [InlineKeyboardButton(text="⭐ Сленг и идиомы (Премиум)", callback_data="read_slang")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")],
        ]
    )
    await message.answer(
        "📖 **Библиотека текстов для чтения на английском:**",
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
    user_data = get_user(callback.from_user.id, callback.from_user.first_name)
    user_data["points"] += 30
    save_database()
    await callback.message.edit_text(
        f"{text}\n\n✅ Текст успешно прочитан! +30 очков.",
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
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📚 200+ слов для путешествий с примерами", callback_data="travel_vocab_1")],
            [InlineKeyboardButton(text="💬 25 историй и диалогов (Аэропорты/Отели)", callback_data="travel_stories_menu")],
            [InlineKeyboardButton(text="⬅️ Назад к чтению", callback_data="back_to_reading")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")]
        ]
    )
    await callback.message.edit_text(
        "✈️ **Интерактивный модуль путешествий**\n\n"
        "Выберите, что вы хотите изучить:\n"
        "• **200+ слов** с примерами и переводами для любых ситуаций в поезде, аэропорту и городе.\n"
        "• **25 увлекательных историй и диалогов** (в отелях, ресторанах, на вокзалах).",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("travel_vocab_"))
async def travel_vocab_page_cb(callback: types.CallbackQuery):
    page = int(callback.data.replace("travel_vocab_", ""))
    words = []
    try:
        if "vocabulary_travel" in globals() and hasattr(vocabulary_travel, "get_travel_vocabulary"):
            words = vocabulary_travel.get_travel_vocabulary()
    except Exception:
        pass

    if not words:
        words = [("Passport", "Please show your passport.", "Пожалуйста, покажите паспорт.")]

    per_page = 10
    total_pages = (len(words) + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, len(words))

    text = f"📚 **Словарь путешественника (Страница {page}/{total_pages}):**\n\n"
    for i in range(start_idx, end_idx):
        w, ex, tr = words[i]
        text += f"*{i+1}. {w}*\n   💬 {ex}\n   🇷🇺 _{tr}_\n\n"

    buttons = []
    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"travel_vocab_{page-1}"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"travel_vocab_{page+1}"))
    if nav_row:
        buttons.append(nav_row)

    buttons.append([InlineKeyboardButton(text="✈️ К меню путешествий", callback_data="read_travel")])
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")])

    user_data = get_user(callback.from_user.id, callback.from_user.first_name)
    user_data["points"] += 15
    save_database()

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "travel_stories_menu")
async def travel_stories_menu_cb(callback: types.CallbackQuery):
    stories = []
    try:
        if "vocabulary_travel" in globals() and hasattr(vocabulary_travel, "get_travel_stories"):
            stories = vocabulary_travel.get_travel_stories()
    except Exception:
        pass

    keyboard_buttons = []
    for s in stories:
        keyboard_buttons.append([InlineKeyboardButton(text=s["title"], callback_data=f"travel_story_{s['id']}")])
    
    keyboard_buttons.append([InlineKeyboardButton(text="✈️ К меню путешествий", callback_data="read_travel")])
    keyboard_buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")])

    await callback.message.edit_text(
        "💬 **25 историй и диалогов в путешествиях**\n\nВыберите историю для чтения:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_buttons),
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("travel_story_"))
async def travel_story_view_cb(callback: types.CallbackQuery):
    story_id = int(callback.data.replace("travel_story_", ""))
    stories = []
    try:
        if "vocabulary_travel" in globals() and hasattr(vocabulary_travel, "get_travel_stories"):
            stories = vocabulary_travel.get_travel_stories()
    except Exception:
        pass

    selected = next((s for s in stories if s["id"] == story_id), None)
    if not selected:
        selected = {"title": "История", "content": "Содержимое загружается..."}

    user_data = get_user(callback.from_user.id, callback.from_user.first_name)
    user_data["points"] += 20
    save_database()

    text = f"📖 **{selected['title']}**\n\n{selected['content']}\n\n✅ Прочитано! +20 очков."
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ К списку историй", callback_data="travel_stories_menu")],
            [InlineKeyboardButton(text="✈️ Меню путешествий", callback_data="read_travel")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")]
        ]
    )
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "back_to_reading")
async def back_to_reading_cb(callback: types.CallbackQuery):
    fake_msg = callback.message
    fake_msg.from_user = callback.from_user
    await reading_handler(fake_msg)
    await callback.answer()

@dp.callback_query(F.data == "read_prem_travel")
async def read_prem_travel_cb(callback: types.CallbackQuery):
    user_data = get_user(callback.from_user.id, callback.from_user.first_name)
    if not user_data["is_premium"]:
        await callback.answer(
            "⭐ VIP-путешествия доступны только по Премиум-подписке!",
            show_alert=True,
        )
        return

    prem_text = "⭐ **First Class Journeys & VIP Travel:** Загрузка..."
    try:
        if "vocabulary_premium_travel" in globals() and hasattr(vocabulary_premium_travel, "get_vip_travel"):
            prem_text = vocabulary_premium_travel.get_vip_travel()
    except Exception:
        pass

    user_data["points"] += 75
    save_database()
    await callback.message.edit_text(
        f"{prem_text}\n\n✅ Элитный материал проработан! +75 очков зачислено 🚀",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")
            ]]
        ),
        parse_mode="Markdown",
    )
    await callback.answer()

@dp.callback_query(F.data == "read_slang")
async def read_slang_cb(callback: types.CallbackQuery):
    user_data = get_user(callback.from_user.id, callback.from_user.first_name)
    if not user_data["is_premium"]:
        await callback.answer(
            "⭐ Сленг и идиомы доступны только по Премиум-подписке!",
            show_alert=True,
        )
        return

    slang_text = "⭐ **Сленг и идиомы:** Загрузка..."
    try:
        if "vocabulary_premium" in globals() and hasattr(vocabulary_premium, "get_vip_travel"):
            slang_text = vocabulary_premium.get_vip_travel()
    except Exception:
        pass

    user_data["points"] += 50
    save_database()
    await callback.message.edit_text(
        f"{slang_text}\n\n✅ Сленг успешно изучен! +50 очков зачислено 🚀",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")
            ]]
        ),
        parse_mode="Markdown",
    )
    await callback.answer()

@dp.message(F.text == "🎮 Игры и чат")
async def games_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔍 Детективное расследование ⭐", callback_data="game_detective")],
            [InlineKeyboardButton(text="🗺️ Приключение (Adventure)", callback_data="game_adventure")],
            [InlineKeyboardButton(text="💬 Симулятор чата на английском", callback_data="game_chat")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")],
        ]
    )
    await message.answer(
        "🎮 **Игровой зал для практики английского языка:**",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

@dp.callback_query(F.data == "game_detective")
async def detective_game(callback: types.CallbackQuery):
    user_data = get_user(callback.from_user.id, callback.from_user.first_name)
    if not user_data["is_premium"]:
        await callback.answer(
            "⭐ Детективный режим доступен по Премиум-подписке!",
            show_alert=True,
        )
        return
    det_text = "🔍 **Детективное расследование:** Загрузка дела..."
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
    adv_text = "🗺️ **Приключение:** Загрузка истории..."
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
    chat_text = "💬 **Симулятор чата:** Загрузка диалога..."
    try:
        if "vocabulary_chat_sim" in globals() and hasattr(vocabulary_chat_sim, "get_prompt"):
            chat_text = vocabulary_chat_sim.get_prompt()
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
    get_user(user_id, message.from_user.first_name)
    ref_link = f"https://t.me/English_StudyyBot?start=ref_{user_id}"

    sorted_users = sorted(
        USERS_DB.items(),
        key=lambda item: item[1].get("points", 0),
        reverse=True
    )

    top_text = "🏆 **Топ-10 участников рейтинга:**\n\n"
    medals = ["🥇", "🥈", "🥉"]
    
    user_rank = "Ниже 10"
    for index, (uid, udata) in enumerate(sorted_users[:10], start=1):
        medal = medals[index - 1] if index <= 3 else f"{index}."
        name = udata.get("name", "Student")
        pts = udata.get("points", 0)
        marker = " (Вы)" if int(uid) == user_id else ""
        top_text += f"{medal} {name}{marker} — {pts} очков\n"

    for index, (uid, udata) in enumerate(sorted_users, start=1):
        if int(uid) == user_id:
            user_rank = f"#{index}"
            break

    text = (
        f"{top_text}\n"
        f"📍 **Ваше место:** {user_rank}\n\n"
        "🎁 **Призовой фонд:**\n"
        "🥇 **1 место:** Уникальный NFT за 500 звезд!\n"
        "🥈 **2 место:** Премиум на 1 месяц бесплатно!\n"
        "🥉 **3 место:** Премиум на 1 месяц бесплатно!\n\n"
        "🚀 Приглашайте друзей по вашей реферальной ссылке (+100 очков)!\n\n"
        f"🔗 **Ваша реферальная ссылка:**\n`{ref_link}`"
    )
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📤 Поделиться ссылкой",
                    url=(
                        "https://t.me/share/url?url="
                        + ref_link
                        + "&text=Залетай%20в%20бота,%20учим%20английский,%20боремся%20за%20NFT!%20🚀"
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
    user_data = get_user(user.id, user.first_name)
    ref_link = f"https://t.me/English_StudyyBot?start=ref_{user.id}"
    status = "⭐ Премиум (Активен)" if user_data["is_premium"] else "⚪ Базовый"
    current_lvl = user_data.get("level", "a1").upper()

    target_words = 300
    current_words = user_data["words"]
    percent = min(100, int((current_words / target_words) * 100))
    filled = int(percent / 10)
    progress_bar = "█" * filled + "░" * (10 - filled)

    text = (
        f"📊 **Ваш профиль и статистика:**\n\n"
        f"👤 Имя: {user.first_name}\n"
        f"💎 Статус подписки: {status}\n"
        f"🎯 Уровень английского: **{current_lvl}**\n"
        f"🏆 Очки рейтинга: {user_data['points']}\n"
        f"👥 Приглашено друзей: {user_data['refs']}\n"
        f"📚 Изучено слов: {current_words}/{target_words} ({percent}%)\n"
        f"[{progress_bar}]\n"
        f"🎯 Пройдено тестов: {user_data['tests']}\n"
        f"🔥 Дней подряд: {user_data['streak']}\n"
        f"📅 Регистрация: {user_data['reg_date']}\n\n"
        f"🔗 Ваша рефералка:\n`{ref_link}`"
    )
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Сменить уровень (A1-C1)", callback_data="change_level")],
            [InlineKeyboardButton(text="🏆 Открыть лидерборд", callback_data="open_lb")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")],
        ]
    )
    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(F.data == "open_profile")
async def callback_open_profile(callback: types.CallbackQuery):
    await callback.message.delete()
    fake_msg = callback.message
    fake_msg.from_user = callback.from_user
    await profile_handler(fake_msg)
    await callback.answer()

@dp.callback_query(F.data == "change_level")
async def callback_change_level(callback: types.CallbackQuery):
    level_descriptions = (
        "⚙️ **Выбор уровня владения английским языком:**\n\n"
        "🟢 **A1 (Beginner):** Начальный уровень. Подходит для изучения базовых слов, алфавита и простейших фраз для повседневного общения.\n\n"
        "🟢 **A2 (Elementary):** Элементарный уровень. Понимание простых предложений, умение поддержать базовый диалог и рассказать о себе.\n\n"
        "⭐ **B1 (Intermediate):** Средний уровень. Уверенное общение в большинстве ситуаций, понимание основных идей текстов.\n\n"
        "⭐ **B2 (Upper-Intermediate):** Продвинутый уровень. Свободное выражение мыслей, понимание сложных текстов и участие в дискуссиях.\n\n"
        "⭐ **C1 (Advanced):** Профессиональный уровень. Свободное владение языком, спонтанная речь без поиска слов и понимание скрытых смыслов.\n\n"
        "Выберите подходящий уровень ниже:"
    )
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🟢 Уровень A1", callback_data="set_lvl_a1")],
            [InlineKeyboardButton(text="🟢 Уровень A2", callback_data="set_lvl_a2")],
            [InlineKeyboardButton(text="⭐ Уровень B1 (Премиум)", callback_data="set_lvl_b1")],
            [InlineKeyboardButton(text="⭐ Уровень B2 (Премиум)", callback_data="set_lvl_b2")],
            [InlineKeyboardButton(text="⭐ Уровень C1 (Премиум)", callback_data="set_lvl_c1")],
            [InlineKeyboardButton(text="⬅️ Назад в профиль", callback_data="open_profile")],
        ]
    )
    await callback.message.edit_text(
        level_descriptions,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("set_lvl_"))
async def callback_set_level(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user(user_id, callback.from_user.first_name)
    new_lvl = callback.data.replace("set_lvl_", "")
    
    user_data["level"] = new_lvl
    save_database()

    await callback.answer(f"✅ Уровень успешно изменен на {new_lvl.upper()}!", show_alert=True)
    fake_msg = callback.message
    fake_msg.from_user = callback.from_user
    await profile_handler(fake_msg)

@dp.callback_query(F.data == "open_lb")
async def callback_open_lb(callback: types.CallbackQuery):
    await callback.message.delete()
    fake_msg = callback.message
    fake_msg.from_user = callback.from_user
    await leaderboard_handler(fake_msg)
    await callback.answer()

@dp.callback_query(F.data == "prem_buy_cb")
async def callback_prem_buy_cb(callback: types.CallbackQuery):
    await callback.message.delete()
    fake_msg = callback.message
    fake_msg.from_user = callback.from_user
    await premium_handler(fake_msg)
    await callback.answer()

@dp.message(F.text == "⭐ Купить Премиум ✨")
async def premium_handler(message: types.Message):
    user_id = message.from_user.id
    get_user(user_id, message.from_user.first_name)

    text = (
        "⭐ **Центр Премиум-доступа и партнерской программы** ✨🚀\n\n"
        "Выберите нужный пункт в меню ниже, чтобы получить премиум бесплатно за приглашение друзей или приобрести его мгновенно:"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Реферальная ссылка", callback_data="prem_ref_link")],
            [InlineKeyboardButton(text="👥 Вывести друзей (Бонусы)", callback_data="prem_withdraw_refs")],
            [InlineKeyboardButton(text="ℹ️ О премиум-подписке", callback_data="prem_about")],
            [InlineKeyboardButton(text="⭐ Купить Премиум (Stars)", callback_data="prem_buy_stars")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")]
        ]
    )

    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(F.data == "prem_ref_link")
async def prem_ref_link_cb(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    ref_link = f"https://t.me/English_StudyyBot?start=ref_{user_id}"
    user_data = get_user(user_id, callback.from_user.first_name)

    text = (
        f"🔗 **Твоя реферальная ссылка:**\n`{ref_link}`\n\n"
        f"👥 Приглашено друзей: **{user_data['refs']}**\n\n"
        "🎁 **Условия партнерской программы (бонусные дни):**\n"
        "• 1 друг — 🎁 **1 день** Премиума\n"
        "• 2 друга — 🎁 **3 дня** Премиума\n"
        "• 3 друга — 🎁 **5 дней** Премиума\n\n"
        "Отправляй ссылку друзьям и забирай дни в разделе «Вывести друзей»!"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📤 Поделиться ссылкой",
                    url=(
                        "https://t.me/share/url?url="
                        + ref_link
                        + "&text=Залетай%20в%20бота,%20учим%20английский%20и%20получаем%20премиум!%20🚀"
                    ),
                )
            ],
            [InlineKeyboardButton(text="⬅️ Назад в Премиум-меню", callback_data="back_to_prem_menu")]
        ]
    )

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "prem_withdraw_refs")
async def prem_withdraw_refs_cb(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user(user_id, callback.from_user.first_name)
    refs = user_data.get("refs", 0)
    claimed = user_data.get("ref_days_claimed", 0)

    earned_days = 0
    if refs >= 3:
        earned_days = 5
    elif refs == 2:
        earned_days = 3
    elif refs == 1:
        earned_days = 1

    available_to_claim = max(0, earned_days - claimed)

    text = (
        f"👥 **Партнерский вывод бонусов**\n\n"
        f"👤 Приглашено друзей: **{refs}**\n"
        f"🎁 Всего заработано дней: **{earned_days}**\n"
        f"✅ Уже выведено/активировано: **{claimed}** дней\n"
        f"💎 Доступно к выводу: **{available_to_claim}** дней\n\n"
    )

    if available_to_claim > 0:
        text += "Нажми кнопку ниже, чтобы активировать бонусные дни премиума!"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"🎁 Активировать {available_to_claim} дн. Премиума", callback_data="claim_ref_bonus")],
                [InlineKeyboardButton(text="⬅️ Назад в Премиум-меню", callback_data="back_to_prem_menu")]
            ]
        )
    else:
        text += "Пригласи больше друзей по своей реферальной ссылке, чтобы разблокировать новые бонусные дни!"
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔗 Взять реферальную ссылку", callback_data="prem_ref_link")],
                [InlineKeyboardButton(text="⬅️ Назад в Премиум-меню", callback_data="back_to_prem_menu")]
            ]
        )

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "claim_ref_bonus")
async def claim_ref_bonus_cb(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user(user_id, callback.from_user.first_name)
    refs = user_data.get("refs", 0)
    claimed = user_data.get("ref_days_claimed", 0)

    earned_days = 5 if refs >= 3 else (3 if refs == 2 else (1 if refs == 1 else 0))
    available = max(0, earned_days - claimed)

    if available > 0:
        user_data["is_premium"] = True
        user_data["ref_days_claimed"] += available
        save_database()
        await callback.answer(f"🎉 Успешно! Активировано бонусных дней: {available}", show_alert=True)
    else:
        await callback.answer("❌ Нет доступных дней для вывода.", show_alert=True)

    await prem_withdraw_refs_cb(callback)

@dp.callback_query(F.data == "prem_about")
async def prem_about_cb(callback: types.CallbackQuery):
    text = (
        "ℹ️ **О премиум-подписке EnglishStudy** ⭐\n\n"
        "Премиум открывает полный функционал бота для тех, кто настроен выучить английский на максимум:\n\n"
        "• **Продвинутые уровни B1, B2, C1:** Огромные базы сложной лексики и разговорных конструкций.\n"
        "• **VIP-путешествия и Сленг:** Элитные поездки и современные разговорные выражения.\n"
        "• **Детективный режим:** Расследования на английском языке для прокачки логики.\n"
        "• **Симулятор чата:** Живое общение с ботом на любые темы.\n"
        "• **Ускоренный рейтинг:** +1000 очков в лидерборде для победы в битве за NFT!"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⭐ Купить Премиум (Stars)", callback_data="prem_buy_stars")],
            [InlineKeyboardButton(text="⬅️ Назад в Премиум-меню", callback_data="back_to_prem_menu")]
        ]
    )
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@dp.callback_query(F.data == "prem_buy_stars")
async def prem_buy_stars_cb(callback: types.CallbackQuery):
    await callback.message.delete()
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⭐ Заплатить 50 Telegram Stars ✨", pay=True)],
            [InlineKeyboardButton(text="⬅️ Назад в Премиум-меню", callback_data="back_to_prem_menu")]
        ]
    )
    
    await callback.message.answer(
        "⭐ **Оплата Премиум-доступа через Telegram Stars**\n\n"
        "Нажми кнопку ниже, чтобы совершить безопасный платеж и мгновенно активировать все возможности бота:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "back_to_prem_menu")
async def back_to_prem_menu_cb(callback: types.CallbackQuery):
    text = (
        "⭐ **Центр Премиум-доступа и партнерской программы** ✨🚀\n\n"
        "Выберите нужный пункт в меню ниже:"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Реферальная ссылка", callback_data="prem_ref_link")],
            [InlineKeyboardButton(text="👥 Вывести друзей (Бонусы)", callback_data="prem_withdraw_refs")],
            [InlineKeyboardButton(text="ℹ️ О премиум-подписке", callback_data="prem_about")],
            [InlineKeyboardButton(text="⭐ Купить Премиум (Stars)", callback_data="prem_buy_stars")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")]
        ]
    )
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

@dp.pre_checkout_query()
async def pre_checkout_query_handler(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment_handler(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user(user_id, message.from_user.first_name)
    user_data["is_premium"] = True
    user_data["points"] += 1000
    save_database()

    await message.answer(
        "🎉 **Успешная оплата! Премиум-доступ активирован!** ⭐✨\n"
        "Вам начислено +1000 очков в рейтинг.\n"
        "Все уровни, словари и VIP-материалы по английскому языку разблокированы!",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown",
    )

@dp.callback_query(F.data == "to_main")
async def callback_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Вы вернулись в главное меню. Используйте панель управления внизу 👇"
    )
    await callback.answer()

@dp.message(Command("setprem"))
async def cmd_set_prem(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("⚠️ Использование: `/setprem <user_id>`", parse_mode="Markdown")
        return
    try:
        target_id = str(args[1])
        if target_id in USERS_DB:
            USERS_DB[target_id]["is_premium"] = True
            save_database()
            await message.answer(f"✅ Пользователю `{target_id}` успешно выдан Премиум!")
            await bot.send_message(int(target_id), "🎉 Администратор выдал вам бесплатный Премиум-доступ!")
        else:
            await message.answer("❌ Пользователь не найден в базе данных бота.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

async def main():
    logger.info("🚀 Чистый бот запущен без рекламы!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())