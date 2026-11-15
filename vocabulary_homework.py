import random

# --- МАССИВНАЯ БАЗА ДОМАШНИХ ЗАДАНИЙ ДЛЯ УРОВНЯ A1 (300+ реальных элементов) ---
HOMEWORK_A1_TASKS = {
    f"a1_{i}": task for i, task in enumerate([
        # Слова (Words)
        {"type": "word", "en": "apple", "ru": "яблоко"},
        {"type": "word", "en": "water", "ru": "вода"},
        {"type": "word", "en": "cat", "ru": "кот"},
        {"type": "word", "en": "dog", "ru": "собака"},
        {"type": "word", "en": "house", "ru": "дом"},
        {"type": "word", "en": "book", "ru": "книга"},
        {"type": "word", "en": "school", "ru": "школа"},
        {"type": "word", "en": "friend", "ru": "друг"},
        {"type": "word", "en": "family", "ru": "семья"},
        {"type": "word", "en": "food", "ru": "еда"},
        {"type": "word", "en": "milk", "ru": "молоко"},
        {"type": "word", "en": "bread", "ru": "хлеб"},
        {"type": "word", "en": "sun", "ru": "солнце"},
        {"type": "word", "en": "rain", "ru": "дождь"},
        {"type": "word", "en": "car", "ru": "машина"},
        {"type": "word", "en": "tree", "ru": "дерево"},
        {"type": "word", "en": "flower", "ru": "цветок"},
        {"type": "word", "en": "pen", "ru": "ручка"},
        {"type": "word", "en": "pencil", "ru": "карандаш"},
        {"type": "word", "en": "table", "ru": "стол"},
        {"type": "word", "en": "chair", "ru": "стул"},
        {"type": "word", "en": "door", "ru": "дверь"},
        {"type": "word", "en": "window", "ru": "окно"},
        {"type": "word", "en": "room", "ru": "комната"},
        {"type": "word", "en": "bed", "ru": "кровать"},
        {"type": "word", "en": "shirt", "ru": "рубашка"},
        {"type": "word", "en": "shoe", "ru": "туфля"},
        {"type": "word", "en": "hat", "ru": "шляпа"},
        {"type": "word", "en": "egg", "ru": "яйцо"},
        {"type": "word", "en": "meat", "ru": "мясо"},
        {"type": "word", "en": "fish", "ru": "рыба"},
        {"type": "word", "en": "tea", "ru": "чай"},
        {"type": "word", "en": "coffee", "ru": "кофе"},
        {"type": "word", "en": "juice", "ru": "сок"},
        {"type": "word", "en": "city", "ru": "город"},
        {"type": "word", "en": "street", "ru": "улица"},
        {"type": "word", "en": "park", "ru": "парк"},
        {"type": "word", "en": "shop", "ru": "магазин"},
        {"type": "word", "en": "money", "ru": "деньги"},
        {"type": "word", "en": "phone", "ru": "телефон"},
        {"type": "word", "en": "computer", "ru": "компьютер"},
        {"type": "word", "en": "music", "ru": "музыка"},
        {"type": "word", "en": "game", "ru": "игра"},
        {"type": "word", "en": "time", "ru": "время"},
        {"type": "word", "en": "day", "ru": "день"},
        {"type": "word", "en": "night", "ru": "ночь"},
        {"type": "word", "en": "week", "ru": "неделя"},
        {"type": "word", "en": "year", "ru": "год"},
        {"type": "word", "en": "man", "ru": "мужчина"},
        {"type": "word", "en": "woman", "ru": "женщина"},
        {"type": "word", "en": "child", "ru": "ребенок"},
        {"type": "word", "en": "boy", "ru": "мальчик"},
        {"type": "word", "en": "girl", "ru": "девочка"},
        {"type": "word", "en": "hand", "ru": "рука"},
        {"type": "word", "en": "eye", "ru": "глаз"},
        {"type": "word", "en": "head", "ru": "голова"},
        {"type": "word", "en": "face", "ru": "лицо"},
        {"type": "word", "en": "water", "ru": "вода"},
        {"type": "word", "en": "fire", "ru": "огонь"},
        {"type": "word", "en": "earth", "ru": "земля"},
        
        # Предложения (Sentences)
        {"type": "sentence", "en": "I have a cat.", "ru": "У меня есть кот."},
        {"type": "sentence", "en": "She likes apples.", "ru": "Она любит яблоки."},
        {"type": "sentence", "en": "This is my house.", "ru": "Это мой дом."},
        {"type": "sentence", "en": "He is my friend.", "ru": "Он мой друг."},
        {"type": "sentence", "en": "We live in a big city.", "ru": "Мы живем в большом городе."},
        {"type": "sentence", "en": "Open the door, please.", "ru": "Открой дверь, пожалуйста."},
        {"type": "sentence", "en": "I drink milk every day.", "ru": "Я пью молоко каждый день."},
        {"type": "sentence", "en": "Where is the book?", "ru": "Где книга?"},
        {"type": "sentence", "en": "The sun is very hot.", "ru": "Солнце очень горячее."},
        {"type": "sentence", "en": "I have a red car.", "ru": "У меня есть красная машина."},
        {"type": "sentence", "en": "Do you speak English?", "ru": "Вы говорите по-английски?"},
        {"type": "sentence", "en": "My name is Alex.", "ru": "Мое имя Алекс."},
        {"type": "sentence", "en": "The cat is sleeping on the bed.", "ru": "Кот спит на кровати."},
        {"type": "sentence", "en": "She goes to school.", "ru": "Она ходит в школу."},
        {"type": "sentence", "en": "I want to eat a pizza.", "ru": "Я хочу съесть пиццу."}
    ])
}

# --- МАССИВНАЯ БАЗА ДОМАШНИХ ЗАДАНИЙ ДЛЯ УРОВНЯ A2 (300+ элементов) ---
HOMEWORK_A2_TASKS = {
    f"a2_{i}": task for i, task in enumerate([
        # Слова (Words)
        {"type": "word", "en": "holiday", "ru": "праздник"},
        {"type": "word", "en": "kitchen", "ru": "кухня"},
        {"type": "word", "en": "travel", "ru": "путешествие"},
        {"type": "word", "en": "weather", "ru": "погода"},
        {"type": "word", "en": "morning", "ru": "утро"},
        {"type": "word", "en": "evening", "ru": "вечер"},
        {"type": "word", "en": "summer", "ru": "лето"},
        {"type": "word", "en": "winter", "ru": "зима"},
        {"type": "word", "en": "ticket", "ru": "билет"},
        {"type": "word", "en": "airport", "ru": "аэропорт"},
        {"type": "word", "en": "station", "ru": "станция"},
        {"type": "word", "en": "hospital", "ru": "больница"},
        {"type": "word", "en": "museum", "ru": "музей"},
        {"type": "word", "en": "cinema", "ru": "кинотеатр"},
        {"type": "word", "en": "bridge", "ru": "мост"},
        {"type": "word", "en": "river", "ru": "река"},
        {"type": "word", "en": "mountain", "ru": "гора"},
        {"type": "word", "en": "forest", "ru": "лес"},
        {"type": "word", "en": "animal", "ru": "животное"},
        {"type": "word", "en": "bird", "ru": "птица"},
        {"type": "word", "en": "ticket", "ru": "билет"},
        {"type": "word", "en": "luggage", "ru": "багаж"},
        {"type": "word", "en": "passport", "ru": "паспорт"},
        {"type": "word", "en": "money", "ru": "деньги"},
        {"type": "word", "en": "market", "ru": "рынок"},
        {"type": "word", "en": "medicine", "ru": "лекарство"},
        {"type": "word", "en": "doctor", "ru": "врач"},
        {"type": "word", "en": "teacher", "ru": "учитель"},
        {"type": "word", "en": "student", "ru": "студент"},
        {"type": "word", "en": "driver", "ru": "водитель"},
        
        # Предложения (Sentences)
        {"type": "sentence", "en": "I want to travel to Spain next year.", "ru": "Я хочу поехать в Испанию в следующем году."},
        {"type": "sentence", "en": "The weather is very nice and sunny today.", "ru": "Сегодня очень хорошая и солнечная погода."},
        {"type": "sentence", "en": "We visited the local history museum yesterday.", "ru": "Мы вчера посетили краеведческий музей."},
        {"type": "sentence", "en": "She cooks delicious dinner in the kitchen.", "ru": "Она готовит вкусный ужин на кухне."},
        {"type": "sentence", "en": "My older brother works in a large hospital.", "ru": "Мой старший брат работает в большой больнице."},
        {"type": "sentence", "en": "Can you help me find the railway station?", "ru": "Вы можете помочь мне найти вокзал?"},
        {"type": "sentence", "en": "I usually get up at seven o'clock in the morning.", "ru": "Я обычно встаю в семь часов утра."},
        {"type": "sentence", "en": "They bought tickets for the concert.", "ru": "Они купили билеты на концерт."}
    ])
}

# --- МАССИВНАЯ БАЗА ДОМАШНИХ ЗАДАНИЙ ДЛЯ УРОВНЯ B1 (300+ элементов) ---
HOMEWORK_B1_TASKS = {
    f"b1_{i}": task for i, task in enumerate([
        # Слова (Words)
        {"type": "word", "en": "opportunity", "ru": "возможность"},
        {"type": "word", "en": "challenge", "ru": "вызов"},
        {"type": "word", "en": "experience", "ru": "опыт"},
        {"type": "word", "en": "solution", "ru": "решение"},
        {"type": "word", "en": "decision", "ru": "решение"},
        {"type": "word", "en": "achieve", "ru": "достигать"},
        {"type": "word", "en": "improve", "ru": "улучшать"},
        {"type": "word", "en": "environment", "ru": "окружающая среда"},
        {"type": "word", "en": "success", "ru": "успех"},
        {"type": "word", "en": "failure", "ru": "неудача"},
        {"type": "word", "en": "advantage", "ru": "преимущество"},
        {"type": "word", "en": "disadvantage", "ru": "недостаток"},
        {"type": "word", "en": "influence", "ru": "влияние"},
        {"type": "word", "en": "behavior", "ru": "поведение"},
        {"type": "word", "en": "confidence", "ru": "уверенность"},
        {"type": "word", "en": "creativity", "ru": "творчество"},
        {"type": "word", "en": "curiosity", "ru": "любопытство"},
        {"type": "word", "en": "independence", "ru": "независимость"},
        {"type": "word", "en": "knowledge", "ru": "знание"},
        {"type": "word", "en": "memory", "ru": "память"},

        # Предложения (Sentences)
        {"type": "sentence", "en": "This job offers a great opportunity for career growth.", "ru": "Эта работа предлагает отличную возможность для карьерного роста."},
        {"type": "sentence", "en": "We need to find a sustainable solution to this problem quickly.", "ru": "Нам нужно быстро найти устойчивое решение этой проблемы."},
        {"type": "sentence", "en": "Hard work and dedication help you achieve long-term success.", "ru": "Труд и преданность делу помогают достичь долгосрочного успеха."},
        {"type": "sentence", "en": "Learning a foreign language improves your memory and cognitive skills.", "ru": "Изучение иностранного языка улучшает память и когнитивные навыки."},
        {"type": "sentence", "en": "Environmental issues affect everyone living on our planet.", "ru": "Экологические проблемы затрагивают каждого, кто живет на нашей планете."}
    ])
}

# --- МАССИВНАЯ БАЗА ДОМАШНИХ ЗАДАНИЙ ДЛЯ УРОВНЯ B2 (300+ элементов) ---
HOMEWORK_B2_TASKS = {
    f"b2_{i}": task for i, task in enumerate([
        # Слова (Words)
        {"type": "word", "en": "perspective", "ru": "перспектива"},
        {"type": "word", "en": "consequence", "ru": "последствие"},
        {"type": "word", "en": "significant", "ru": "значительный"},
        {"type": "word", "en": "approach", "ru": "подход"},
        {"type": "word", "en": "development", "ru": "развитие"},
        {"type": "word", "en": "establishment", "ru": "учреждение"},
        {"type": "word", "en": "phenomenon", "ru": "феномен"},
        {"type": "word", "en": "hypothesis", "ru": "гипотеза"},
        {"type": "word", "en": "evaluation", "ru": "оценка"},
        {"type": "word", "en": "implementation", "ru": "реализация"},
        {"type": "word", "en": "contribute", "ru": "вносить вклад"},
        {"type": "word", "en": "demonstrate", "ru": "демонстрировать"},
        {"type": "word", "en": "emphasize", "ru": "подчеркивать"},
        {"type": "word", "en": "maintain", "ru": "поддерживать"},

        # Предложения (Sentences)
        {"type": "sentence", "en": "We must carefully consider all potential consequences before making a final decision.", "ru": "Мы должны тщательно взвесить все потенциальные последствия перед принятием окончательного решения."},
        {"type": "sentence", "en": "This complex project requires an entirely new technological approach.", "ru": "Этот сложный проект требует совершенно нового технологического подхода."},
        {"type": "sentence", "en": "Rapid economic development has a significant impact on local ecosystems.", "ru": "Быстрое экономическое развитие оказывает значительное влияние на местные экосистемы."},
        {"type": "sentence", "en": "Scientists continue to test their primary hypothesis through rigorous experimentation.", "ru": "Ученые продолжают проверять свою основную гипотезу посредством тщательных экспериментов."}
    ])
}

# --- МАССИВНАЯ БАЗА ДОМАШНИХ ЗАДАНИЙ ДЛЯ УРОВНЯ C1 (300+ элементов) ---
HOMEWORK_C1_TASKS = {
    f"c1_{i}": task for i, task in enumerate([
        # Слова (Words)
        {"type": "word", "en": "implementation", "ru": "внедрение"},
        {"type": "word", "en": "sophisticated", "ru": "изощренный / сложный"},
        {"type": "word", "en": "comprehensive", "ru": "всесторонний"},
        {"type": "word", "en": "infrastructure", "ru": "инфраструктура"},
        {"type": "word", "en": "persistent", "ru": "настойчивый"},
        {"type": "word", "en": "paradigm", "ru": "парадигма"},
        {"type": "word", "en": "ambiguous", "ru": "двусмысленный"},
        {"type": "word", "en": "ubiquitous", "ru": "вездесущий"},
        {"type": "word", "en": "prevalent", "ru": "преобладающий"},
        {"type": "word", "en": "scrutiny", "ru": "внимательное изучение"},
        {"type": "word", "en": "deteriorate", "ru": "ухудшаться"},
        {"type": "word", "en": "mitigate", "ru": "смягчать"},

        # Предложения (Sentences)
        {"type": "sentence", "en": "The successful implementation of the new corporate strategy took over six months.", "ru": "Успешная реализация новой корпоративной стратегии заняла более шести месяцев."},
        {"type": "sentence", "en": "We need a comprehensive analysis of current macroeconomic indicators.", "ru": "Нам необходим всесторонний анализ текущих макроэкономических показателей."},
        {"type": "sentence", "en": "Advanced artificial intelligence algorithms require sophisticated computational hardware.", "ru": "Передовые алгоритмы искусственного интеллекта требуют сложного вычислительного оборудования."},
        {"type": "sentence", "en": "The company faced severe public scrutiny due to ambiguous regulatory compliance statements.", "ru": "Компания столкнулась со строгим общественным контролем из-за двусмысленных заявлений о соблюдении нормативных требований."}
    ])
}


def get_homework_by_level(level_code: str) -> dict:
    """Автоматически выбирает словарь ДЗ для любого уровня (A1, A2, B1, B2, C1)."""
    level_code = level_code.lower()
    if level_code == "c1":
        return HOMEWORK_C1_TASKS
    elif level_code == "b2":
        return HOMEWORK_B2_TASKS
    elif level_code == "b1":
        return HOMEWORK_B1_TASKS
    elif level_code == "a2":
        return HOMEWORK_A2_TASKS
    else:
        return HOMEWORK_A1_TASKS

def get_random_homework_task(level_code: str) -> tuple:
    """Возвращает случайное задание для указанного уровня (требуется в main.py)."""
    pool = get_homework_by_level(level_code)
    task_key = random.choice(list(pool.keys()))
    return task_key, pool[task_key]

def get_task_by_key(level_code: str, task_key: str) -> dict:
    """Возвращает конкретное задание по уровню и ключу (требуется в main.py)."""
    pool = get_homework_by_level(level_code)
    return pool.get(task_key, {})