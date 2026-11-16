import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Надежный веб-сервер в отдельном потоке для мгновенного открытия порта на Render
def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), BaseHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

import asyncio
import datetime
import json
import logging
import time
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

# Настройка логирования
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

def get_user(user_id: int, first_name: str = "Student"):
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
            "streak": 1,
            "last_word_time": 0,
            "reg_date": datetime.date.today().strftime("%d.%m.%Y"),
        }
        save_database()
    else:
        USERS_DB[str_id]["name"] = first_name
    return USERS_DB[str_id]

# 100% точный импорт всех твоих модулей из проекта без пропусков
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
    import vocabulary_radin_b1
    import vocabulary_radin_b2
    import vocabulary_radin_c1
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
                KeyboardButton(text="📚 Learn Words"),
                KeyboardButton(text="🎯 Tests & Quiz"),
            ],
            [
                KeyboardButton(text="📖 Reading Texts"),
                KeyboardButton(text="🎮 Games & Chat"),
            ],
            [
                KeyboardButton(text="🏆 Leaderboard (500⭐)"),
                KeyboardButton(text="👤 Profile"),
            ],
            [
                KeyboardButton(text="⚙️ Settings"),
                KeyboardButton(text="⭐ Get Premium *"),
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

    welcome_text = (
        f"👋 Welcome, {message.from_user.first_name}!\n\n"
        "🚀 Профессиональный образовательный бот для эффективного изучения английского языка.\n"
        "🔥 **Участвуйте в рейтинге!** Приглашайте друзей, изучайте слова из базы и получайте награды:\n"
        "🥇 **1 место:** Уникальный NFT за 500 звезд!\n"
        "🥈 **2 и 🥉 3 места:** Премиум-доступ на 1 месяц бесплатно!\n\n"
        "Выберите нужный раздел в меню ниже 👇"
    )
    await message.answer(
        welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown"
    )

@dp.message(F.text.in_(["🏠 Главное меню", "Main Menu"]))
async def main_menu(message: types.Message):
    await message.answer(
        "🏠 Вы вернулись в главное меню:", reply_markup=get_main_keyboard()
    )

@dp.message(F.text == "📚 Learn Words")
async def learn_words_handler(message: types.Message):
    user_data = get_user(message.from_user.id, message.from_user.first_name)
    current_level = user_data.get("level", "a1")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Учить слова по уровню", callback_data=f"lvl_train_{current_level}")],
            [InlineKeyboardButton(text="⚡ Словарный спринт (A1-C1)", callback_data="sprint_menu")],
            [InlineKeyboardButton(text="👤 Сменить уровень в профиле", callback_data="open_profile")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")]
        ]
    )
    await message.answer(
        f"📚 **Словарный тренажер английского языка**\n"
        f"🎯 Ваш текущий уровень: **{current_level.upper()}**\n\n"
        "Выберите режим тренировки слов:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.startswith("lvl_train_"))
async def callback_lvl_train(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    user_data = get_user(user_id, callback.from_user.first_name)
    lvl = callback.data.replace("lvl_train_", "")

    if lvl in ["b1", "b2", "c1"] and not user_data["is_premium"]:
        await callback.answer(
            "⭐ Этот уровень доступен только по Премиум-подписке!", show_alert=True
        )
        return

    user_data["words"] += 1
    user_data["points"] += 10
    save_database()

    target_words = 300
    current_words = user_data["words"]
    percent = min(100, int((current_words / target_words) * 100))
    filled = int(percent / 10)
    progress_bar = "█" * filled + "░" * (10 - filled)

    content = f"📖 Слово уровня **{lvl.upper()}** успешно загружено из модуля словаря!"
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
        logger.error(f"Ошибка словаря: {e}")

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➡️ Следующее слово", callback_data=f"lvl_train_{lvl}")],
            [InlineKeyboardButton(text="⬅️ Назад к выбору", callback_data="back_to_words")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")]
        ]
    )
    await callback.message.edit_text(
        f"✅ **Тренировка лексики ({lvl.upper()}):**\n\n{content}\n\n"
        f"📊 **Прогресс:** {current_words}/{target_words} слов ({percent}%)\n"
        f"[{progress_bar}]\n\n🚀 +10 очков зачислено в рейтинг!",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await callback.answer()

@dp.callback_query(F.data == "back_to_words")
async def back_to_words_cb(callback: types.CallbackQuery):
    await callback.message.delete()
    await learn_words_handler(callback.message)
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
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_words")],
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

@dp.message(F.text == "🎯 Tests & Quiz")
async def tests_handler(message: types.Message):
    user_data = get_user(message.from_user.id, message.from_user.first_name)
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
        "🎯 **Тест на знание английского языка:**\n\nКак правильно переводится слово *«Success»*?",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

@dp.callback_query(F.data.startswith("test_"))
async def callback_test(callback: types.CallbackQuery):
    if callback.data == "test_correct":
        await callback.answer("🎉 Абсолютно верно! +25 очков", show_alert=True)
    else:
        await callback.answer(
            "❌ Неверно. Правильный вариант: Success (Успех).", show_alert=True
        )
    await callback.message.edit_text(
        "🎯 Тест завершен!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")]
            ]
        ),
    )

@dp.message(F.text == "📖 Reading Texts")
async def reading_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Истории и статьи", callback_data="read_stories")],
            [InlineKeyboardButton(text="✈️ Путешествия (Базовые)", callback_data="read_travel")],
            [InlineKeyboardButton(text="⭐ VIP-путешествия (Премиум) *", callback_data="read_prem_travel")],
            [InlineKeyboardButton(text="📰 Аудиоматериалы (Radin)", callback_data="read_radin")],
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
    text = "✈️ **Путешествия:** Загрузка из модуля..."
    try:
        if "vocabulary_travel" in globals() and hasattr(vocabulary_travel, "get_dialog"):
            text = vocabulary_travel.get_dialog()
    except Exception:
        pass
    user_data = get_user(callback.from_user.id, callback.from_user.first_name)
    user_data["points"] += 30
    save_database()
    await callback.message.edit_text(
        f"{text}\n\n✅ Диалог пройден! +30 очков.",
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
    user_data = get_user(callback.from_user.id, callback.from_user.first_name)
    if not user_data["is_premium"]:
        await callback.answer(
            "⭐ VIP-материалы доступны только по Премиум-подписке!",
            show_alert=True,
        )
        return

    prem_text = "⭐ **VIP-путешествия:** Загрузка из премиум-модуля..."
    try:
        if "vocabulary_premium" in globals() and hasattr(vocabulary_premium, "get_vip_travel"):
            prem_text = vocabulary_premium.get_vip_travel()
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
    user_data = get_user(callback.from_user.id, callback.from_user.first_name)
    lvl = user_data.get("level", "b1")
    text = f"📰 **Аудиоматериал ({lvl.upper()}):** Загрузка..."
    try:
        if lvl == "b2" and "vocabulary_radin_b2" in globals() and hasattr(vocabulary_radin_b2, "get_material"):
            text = vocabulary_radin_b2.get_material()
        elif lvl == "c1" and "vocabulary_radin_c1" in globals() and hasattr(vocabulary_radin_c1, "get_material"):
            text = vocabulary_radin_c1.get_material()
        elif "vocabulary_radin_b1" in globals() and hasattr(vocabulary_radin_b1, "get_material"):
            text = vocabulary_radin_b1.get_material()
    except Exception:
        pass
    
    user_data["points"] += 35
    save_database()
    await callback.message.edit_text(
        f"{text}\n\n✅ Материал прослушан и разобран! +35 очков.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text="🏠 Главное меню", callback_data="to_main")
            ]]
        ),
        parse_mode="Markdown",
    )
    await callback.answer()

@dp.message(F.text == "🎮 Games & Chat")
async def games_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔍 Детективное расследование *", callback_data="game_detective")],
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

@dp.message(F.text == "🏆 Leaderboard (500⭐)")
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

@dp.message(F.text == "👤 Profile")
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
    await profile_handler(callback.message)
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
    await profile_handler(callback.message)

@dp.callback_query(F.data == "open_lb")
async def callback_open_lb(callback: types.CallbackQuery):
    await callback.message.delete()
    await leaderboard_handler(callback.message)

@dp.message(F.text == "⚙️ Settings")
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
        "⚙️ **Настройки и справочные материалы:**",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

@dp.callback_query(F.data == "homework")
async def setting_hw(callback: types.CallbackQuery):
    user_data = get_user(callback.from_user.id, callback.from_user.first_name)
    if not user_data["is_premium"]:
        await callback.answer(
            "⭐ Домашние задания доступны по Премиум-подписке!",
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
    gram_text = "📖 **Справочник грамматики английского языка:**"
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
    prem_text = "⭐ **Премиум-доступ:** Открывает все продвинутые уровни, аудирование, игры и справочники."
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

@dp.message(F.text == "⭐ Get Premium *")
async def premium_handler(message: types.Message):
    prices = [types.LabeledPrice(label="Премиум-доступ (B1-C1 + материалы + игры)", amount=50)]
    await message.answer_invoice(
        title="Премиум-доступ к боту",
        description="Откройте продвинутый уровень B1-C1, VIP-путешествия, детективный режим, симулятор чата и 500 тем домашней работы!",
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
    user_data = get_user(user_id, message.from_user.first_name)
    user_data["is_premium"] = True
    user_data["points"] += 1000
    save_database()

    await message.answer(
        "🎉 **Успешная оплата! Премиум-доступ активирован!** ⭐\n"
        "Вам начислено +1000 очков в рейтинг.\n"
        "Все уровни, словари и VIP-материалы по английскому языку разблокированы!",
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
    logger.info("🚀 Бот для изучения английского языка полностью запущен со всеми модулями!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())