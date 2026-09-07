# Подключаем встроенные модули и библиотеки:
import json
import random
from telebot import types
import os

# Подключаем свои модули:
import button
import printer
import loader 
from loader import bot

# Нужные функции:
def lst_players(num):
    lst_players = []
    for i in range(num):
        lst_players.append(i + 1)
    return lst_players


def sec_word(user_theme: str, themes: dict, chat_id: str) -> str:
    """Выбирает случайное секретное слово, которое должны угадать Шпионы.

    Args:
        user_theme: Тема, выбранная пользователем.
        themes: Словарь тем со словами.
        chat_id: ID чата пользователя.

    Returns:
          Возвращает секретное слово.
    """
    if user_theme in themes["Main_themes"]:
        lst_words = themes["Main_themes"][user_theme]
    else:
        lst_words = themes[chat_id][user_theme]
    choice_word = random.choice(lst_words)
    return choice_word


def create_shpion(num_shpions: int, lst_players: list) -> list:
    """Создаёт список шпионов для игры.

    Args:
        num_shpions: Кол-во Шпионов.
        lst_players: Список игроков.

    Returns:
        Возвращает список Шпионов.
    """
    shpion1 = random.choice(lst_players)
    shpions = [shpion1]
    if num_shpions == 2:
        lst_without_shpion1 = [i for i in range(lst_players) if i != shpion1]
        shpion2 = random.choice(lst_without_shpion1)
        shpions.append(shpion2)
    return shpions


def current_games(current_games, chat_id):
    count_players = len(current_games[chat_id]["lst_players"])
    num_shpions = current_games[chat_id]["num_shpions"]
    user_theme = current_games[chat_id]["user_theme"]
    game_mode = current_games[chat_id]["game_mode"]

    if game_mode == 'classic':
        mode_display = "📜 Классика"
        shpions_text = f"*{num_shpions}* 🕵️‍♂️"
        peace_text = f"*{count_players - num_shpions}* 🧑‍🌾"
    else:
        mode_display = "🎲 Хаос"
        shpions_text = "_Случайно_ 🔮"
        peace_text = "_Случайно_ 🔮"
    return [count_players, peace_text, shpions_text, user_theme, mode_display]


def create_theme(themes: dict, theme_name: str, words: tuple, chat_id: str):
    """Создаёт тему со словами от пользователя.

    Args:
        themes: Словарь тем со словами.
        theme_name: Тема, введённая от пользователя.
        words: Слова, введённая от пользователя
        chat_id: ID чата пользователя.
    """
    if chat_id not in themes:
        themes[chat_id] = {}
    themes[chat_id][theme_name] = words
    json_dump(themes)


def rename_theme(choice_theme, new_theme, chat_id, themes):
    themes[str(chat_id)][new_theme] = themes[str(chat_id)].pop(choice_theme)
    json_dump(themes)


def get_theme_name(message: types.Message, themes: dict, flag: str = "need", choice_theme=None):
    """Принимает имя новой темы от пользователя и отправляет его в другую функцию.

    Args:
        message: Объект, содержащий данные о сообщении и пользователе.
        themes: Словарь тем со словами.
        words:
        choice_theme:

    Returns:
        Выходит из функции в случае ошибки.
    """
    chat_id = message.chat.id
    new_theme = message.text.strip()
    if not new_theme:
        bot.send_message(chat_id, printer.TEXT_ERROR_CREATE_THEME, reply_markup=button.markup_start(),
                         parse_mode='Markdown')
        return
    elif themes.get(str(chat_id), False):
        for old_theme in themes[str(chat_id)]:
            if new_theme.lower() == old_theme.lower():
                bot.send_message(chat_id, printer.TEXT_ERROR_SUCH_THEME, reply_markup=button.markup_start(),
                                 parse_mode='Markdown')
                return
    if flag == "need":
        sent = bot.send_message(message.chat.id, printer.TEXT_CREATE_WORDS,
                                reply_markup=button.markup_back(["themes", "create"], "🔙 Назад в МЕНЮ СОЗДАНИЯ ТЕМЫ"), parse_mode='Markdown')
        bot.clear_step_handler_by_chat_id(chat_id)
        bot.register_next_step_handler(sent, get_theme_words, new_theme, themes)

    else:
        if themes.get(str(chat_id), False):
            for old_theme in themes[str(chat_id)]:
                if new_theme.lower() == old_theme.lower():
                    bot.send_message(chat_id, printer.TEXT_ERROR_SUCH_THEME,
                                     reply_markup=button.markup_start(),
                                     parse_mode='Markdown')
                    return
        rename_theme(choice_theme, new_theme, chat_id, themes)
        bot.send_message(chat_id, printer.TEXT_CREATE_FINISH, reply_markup=button.markup_back(["themes", "start"],"🔙 Назад в 📂 ТЕМЫ"), parse_mode='Markdown')


def get_theme_words(message: types.Message, new_theme: str, themes: dict, flag: str = "need", add_words=""):
    """Получает слова для новой темы, сохраняет тему и подтверждает пользователю.

    Args:
        message: Объект, содержащий данные о сообщении и пользователе.
        new_theme: Тема, которую ввёл пользователь.
        themes: Словарь тем со словами.
        word:
        add_words:

    Returns:
        Выходит из функции в случае ошибки.
    """
    need_words = None
    if flag == "need":
        need_words = list(word.strip() for word in message.text.split(',') if word.strip())

    if not need_words:
        bot.send_message(message.chat.id, printer.TEXT_ERROR_CREATE_WORDS, parse_mode='Markdown')
        return

    if add_words == "add":
        old_words = themes[str(message.chat.id)][new_theme]
        need_words = old_words + need_words
    chat_id = message.chat.id
    create_theme(themes, new_theme, need_words, str(chat_id))
    bot.send_message(chat_id, printer.TEXT_CREATE_FINISH, reply_markup=button.markup_back(["themes", "start"],"🔙 Назад в 📂 ТЕМЫ"), parse_mode='Markdown')


def delete_theme(themes: dict, delete_theme: str, chat_id: str):
    """Удаляет тему, выбранную пользователем, кроме 4 основных тем.

    Args:
        themes: Словарь тем со словами.
        delete_theme: Тема, которую нужно удалить
        chat_id: ID чата пользователя.
    """
    themes[chat_id].pop(delete_theme)
    if themes[chat_id] == {}:
        themes.pop(chat_id)
    json_dump(themes)


def view_words(MAIN_THEMES, themes: dict, choice_theme: str, chat_id: int, act):
    if choice_theme in MAIN_THEMES:
        lst_words = themes["Main_themes"][choice_theme]
    else:
        lst_words = themes[str(chat_id)][choice_theme]

    if act == "view":
        if len(lst_words) > 20:
            lst_words = lst_words[:15]
            lst_words = "\n".join(lst_words)
            status = "txt"

        else:
            lst_words = "\n".join(lst_words)
            status = "message"
    else:
        status = "txt"
    return lst_words, choice_theme, status


def send_txt(chat_id, lst):
    txt_file = f"{str(chat_id)}_words.txt"
    with open(txt_file, mode="w", encoding='utf-8') as f:
        f.write("\n".join(lst))
    with open(txt_file, mode="rb") as f:
        bot.send_document(chat_id=chat_id, document=f, caption='📄 Полный список слов для темы успешно подготовлен.')
    os.remove(txt_file)


def edit_message(text: str, call: types.CallbackQuery, markup: str = None, parse: str = 'Markdown') -> str:
    """Изменяет преведущее сообщение в боте и выдаёт новую информацию (текст, кнопки) по введённым аргументам.

    Args:
        text: Текст, который будет выведен пользователю.
        call: Объект запроса, содержащий информацию о callback_data, пользователе и нажатой кнопке
        markup: Объект инлайн-клавиатуры с кнопками.
        parse: Мод, который делает жирный шрифт, волнистость, курсивный текст  и т.п.

    Returns:
        Возвращает, если нужно использовать `bot.register_next_step_handler()` с сообщением внутри.
    """

    return bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup,
                                 parse_mode=parse)


def json_load() -> dict:
    """Выгружает темы из файла JSON, если возникают ошибки, создаёт основные.

    Returns:
        Возвращает словарь из файла JSON или словарь, созданный из 4 основных тем.
    """
    try:
        with open('themes.json', 'r', encoding='utf-8') as file:
            themes = json.load(file)
            MAIN_THEMES = themes["Main_themes"]
            return themes, MAIN_THEMES
    except (FileNotFoundError, json.JSONDecodeError):
        themes = {
            "Main_themes": {
                "Локации 📍": (
                    "🏫 Школа", "🧸 Детский сад", "🎓 Университет", "🏥 Больница", "🩺 Поликлиника", "💊 Аптека",
                    "🛍️ Магазин", "🛒 Супермаркет", "🍅 Рынок", "🏢 Торговый центр", "🏦 Банк", "📦 Почта",
                    "🌳 Парк", "🦁 Зоопарк", "🎪 Цирк", "🛝 Детская площадка", "🏟️ Стадион", "🏊 Бассейн",
                    "🍿 Кинотеатр", "🎭 Театр", "🏛️ Музей", "📚 Библиотека", "🖼️ Выставка", "🎸 Концерт",
                    "🍽️ Ресторан", "☕ Кафе", "🍲 Столовая", "🍕 Пиццерия", "🍔 Макдоналдс", "🥤 Кофейня",
                    "🏖️ Пляж", "🏡 База отдыха", "🌲 Лес", "⛰️ Горы", "🏞️ Река", "🛶 Озеро", "🏘️ Деревня", "🏡 Дача",
                    "✈️ Аэропорт", "🚉 Вокзал", "🚇 Метро", "🚏 Остановка", "⛽ Заправка", "🧽 Автомойка",
                    "🏨 Отель", "🛏️ Хостел", "🚪 Подъезд", "🛗 Лифт", "🔑 Квартира", "🍳 Кухня", "🛁 Ванная",
                    "🏋️‍♂️ Тренажерный зал", "💪 Фитнес-клуб", "💅 Салон красоты", "💈 Парикмахерская",
                    "👮 Полиция", "🚒 Пожарная часть", "⚖️ Суд", "⛓️ Тюрьма", "🪖 Военная база", "🏗️ Стройка",
                    "🖥️ Офис", "📦 Склад", "🏭 Завод", "🛠️ Мастерская", "🚗 Гараж", "📦 Чердак", "🕸️ Подвал",
                    "🚢 Корабль", "⛵ Лодка", "🤿 Подводная лодка", "🛩️ Самолет", "🚁 Вертолет", "🚂 Поезд",
                    "🚌 Автобус", "🚕 Такси", "🚃 Трамвай", "🚎 Троллейбус", "🚛 Грузовик", "🌌 Космос",
                    "🚀 Станция МКС", "🌕 Луна", "🪐 Марс", "🏜️ Пустыня", "🌴 Джунгли", "🪨 Пещера",
                    "⛪ Церковь", "🏰 Замок", "🏛️ Дворец", "🎨 Музей искусств", "🪐 Планетарий", "🌊 Аквапарк",
                    "⛸️ Каток", "🎳 Боулинг", "🎱 Бильярд", "🕺 Ночной клуб", "🎤 Караоке", "🎯 Тир", "🎣 Рыбалка",
                    "🏹 Охота", "🥕 Огород", "🌿 Теплица", "🐝 Пасека", "🚜 Ферма", "🐴 Конюшня",
                ),
                "Clash Royal 👑": (
                    "⚔️ Рыцарь", "🏹 Лучницы", "🪵 Гигант", "💣 Бомбер", "🏰 Принцесса(Башня)", "💀 Скелеты", "🟢 Гоблины",
                    "🐗 Всадник на кабане", "🔫 Мушкетер", "🤖 Мини П.Е.К.К.А.", "🪓 Валькирия", "🐴 Принц",
                    "⚙️ Мини-генераторы",
                    "🐉 Дракончик", "💀 Армия скелетов", "🔮 Ведьма", "🎈 Воздушный шар", "👑 Три мушкетерки", "🛸 Летучка",
                    "🪓 Варвары", "🦇 Орда миньонов", "🪓 Гоблины-копейщики", "💀 Гигантский скелет", "🤖 П.Е.К.К.А.",
                    "🦇 Миньоны", "👑 Королевский гигант", "🔥 Огненный дух", "❄️ Ледяной дух", "⚔️ Элитные варвары",
                    "🦇 Мегаминьон", "❄️ Ледяной колдун", "⛏️ Шахтер", "👑 Принцесса", "🔥 Адская Гончая", "⚡ Спарки",
                    "🪓 Дровосек", "⚡ Громовержец", "🎭 Бандитка", "🔮 Ночная ведьма", "🏹 Магический лучник",
                    "🦇 Летучие мыши",
                    "👻 Королевский призрак", "🐏 Всадник на баране (PЭМ)", "🪓 Палач", "🌾 Крестьянин", "🎯 Охотник",
                    "⚡ Электрический дракон", "💣 Стенобои", "🛡️ Целительница-воин", "🐗 Королевские кабаны", "🌿 Лоза",
                    "🛡️ Мегарыцарь", "🎣 Рыбак", "⚡ Электрический гигант", "👵 Ведьмина бабушка", "🟡 Золотой рыцарь",
                    "🛡️ Стражи",
                    "💀 Король скелетов", "👑 Королева лучниц", "⛏️ Шустрый шахтёр", "🧘 Монах", "🔮 Императрица духов",
                    "👑 Маленький принц", "⚡ Электрический дух", "✨ Дух исцеления", "🦅 Феникс", "🛡️ Темный принц",
                    "🛞 Пушка на колёсах",
                    "🏹 Стрелы", "🔥 Огненный шар", "🚀 Ракета", "⚡ Молния", "⚡ Разряд", "🪞 Зеркало", "⚡ Ярость",
                    "🌋 Руническая гигантша",
                    "❄️ Заморозка", "🧪 Яд", "🪵 Бревно", "🌪️ Торнадо", "👥 Клон", "🪵 Землетрясение", "❄️ Снежок",
                    "🪓 Берсеркша",
                    "📦 Королевская почта", "🧪 Гоблинская бочка", "💣 Бочка со скелетами", "🪵 Варварская бочка",
                    "🟢 Гигантский гоблин",
                    "🧪 Гоблинское проклятие", "🌌 Бездна", "🏰 Канонир (башня)", "🏰 Графиня (башня)", "🏰 Повар (башня)",
                    "💣 Пушка", "⚡ Тесла", "💣 Мортира", "💣 Башня-бомбежка", "🔥 Адская башня", "🏹 Арбалет",
                    "🏹 Огненная лучница",
                    "🧪 Сборщик эликсира", "🪦 Надгробие", "🛖 Хижина гоблинов", "🛖 Хижина варваров", "🔥 Печь",
                    "🐉 Костяные драконы",
                    "🪵 Клетка с гоблином", "🔩 Гоблинский бур", "❄️ Ледяной голем", "🪨 Голем", "🟢 Банда гоблинов",
                    "🛡️ Рекруты",
                    "🪓 Разбойники", "🧪 Эликсирный голем", "🟢 Гоблин с дротиками", "🪵 Подозрительный куст", "🪵 Таран",
                    "🔥 Колдун",
                    "🐉 Пламенный дракон", "🪦 Кладбище", "🔩 Гоблинская машина", "🎭 Главная бандитка", "🧪 Гоблинштейн",
                    "💣 Гоблин-подрывник"
                ),
                "Видеоигры🎮": (
                    "🧱 Minecraft", "🔫 Counter-strike 2 (CS 2)", "⚔️ Dota 2", "🚗 GTA 5", "🏡 Sims", "🧸 Roblox",
                    "🪂 Fortnite", "🍳 PUBG",
                    "🌳 Terraria", "🎯 Valorant", "🌀 Portal 2", "🪖 Call of Duty", "🔧 Team fortress 2", "🛖 Rust",
                    "✨ Genshin Impact",
                    "🤖 Cyberpunk 2077", "✈️ War Thunder", "🚜 World of Tanks", "🤫 Hello Neighbor", "🏃 Subway Surfers",
                    "🔥 Free Fire",
                    "🛡️ Clash of clans", "🏎️ Need for Speed", "📮 Among Us", "👑 Clash Royale", "🏃 Temple Run",
                    "🍉 Fruit Ninja",
                    "🐦 Angry Birds", "⭐ Brawl Stars", "🧩 Homescapes", "🚗 Hill climb racing", "🐱 Tom", "🟩 Geometry dash",
                    "🐦 Flappy bird",
                    "🚜 Hay Day", "🥷 Shadow fight", "🦔 Sonic", "🏃 Stumble guys", "🧱 Tetris", "👑 Chess", "⚪ Checkers",
                    "🧱 Block blast", "👵 Granny",
                ),
                "Minecraft 🧱": (
                    "🪨 Бедрок", "🧱 Булыжник", "🪨 Глубинный сланец", "🪨 Туф", "🪨 Кальцит", "🪨 Диорит", "🪨 Андезит",
                    "🪨 Гранит",
                    "🟫 Земля", "🟫 Подзол", "🍄 Мицелий", "🌱 Дерн", "💩 Грязь", "🟫 Плотная грязь", "🏺 Глина",
                    "🧱 Терракота",
                    "⏳ Песок", "🟠 Красный песок", "🪨 Гравий", "🔮 Обсидиан", "😢 Плачущий обсидиан", "🔥 Магма",
                    "🧊 Лед", "🧊 Плотный лед", "🔷 Синий лед", "❄️ Снег", "🌨️ Слой снега", "⛄ Плотный снег",
                    "🪵 Дубовое бревно", "🪵 Березовое бревно", "🪵 Еловое бревно", "🪵 Тропическое бревно",
                    "🪵 Акациевое бревно", "🪵 Темное дубовое бревно", "🪵 Мангровое бревно", "🌸 Вишневое бревно",
                    "🪵 Обтесанное бревно", "🪵 Доски", "🪜 Ступеньки", "🪵 Плита", "🪵 Забор", "🪵 Калитка", "🚪 Дверь",
                    "🪵 Люк",
                    "⚫ Угольная руда", "🪙 Железная руда", "🟤 Медная руда", "🟡 Золотая руда", "🔴 Редстоуновая руда",
                    "🔵 Лазуритовая руда", "💎 Алмазная руда", "💚 Изумрудная руда", "🖤 Позолоченный чернит",
                    "🌋 Древние обломки", "🔥 Незеритовый скрап", "🪙 Незеритовый слиток", "🟤 Медный слиток",
                    "🔮 Аметистовый кластер", "✨ Осколок аметиста", "🔊 Эхо-осколок", "🔱 Осколок призмарина",
                    "🔴 Незерак", "🟡 Камень Энда", "⏳ Песок душ", "🟫 Почва душ", "🪨 Базальт", "🖤 Чернит",
                    "🔵 Искаженный грибок", "🔴 Багровый грибок", "💡 Светокамень", "🪄 Стержень Энда",
                    "🟪 Пурпурный блок", "🥚 Яйцо дракона", "🐚 Скорлупа шалкера", "🟪 Шалкеровый ящик",
                    "⚙️ Поршень", "🟢 Липкий поршень", "👁️ Наблюдатель", "🏹 Раздатчик", "📦 Выбрасыватель",
                    "⏳ Повторитель", "📐 Компаратор", "🕹️ Рычаг", "🔘 Кнопка", "🪵 Нажимная плита", "🎯 Мишень",
                    "🎵 Музыкальный блок", "📻 Проигрыватель", "💡 Лампа", "☀️ Датчик дневного света",
                    "⚡ Громоотвод", "🛠️ Автоматический верстак", "🔊 Калиброванный скалковый сенсор",
                    "🔭 Подзорная труба", "🛡️ Щит", "🔱 Трезубец", "🏹 Арбалет", "🏹 Лук", "🔥 Огнево", "🪢 Поводок",
                    "🏷️ Бирка", "🏇 Седло", "🐴 Конская броня", "🪖 Незеритовый шлем", "👕 Незеритовый нагрудник",
                    "👖 Незеритовые поножи", "🥾 Незеритовые ботинки", "🦅 Элитра", "🗿 Тотем бессмертия",
                    "🥕 Золотая морковь", "🍎 Зачарованное золотое яблоко", "🍲 Тушеное кроличье мясо",
                    "🍉 Ломтик арбуза", "🍓 Ягода светящаяся", "🍇 Хорус", "🧪 Пузырек опыта", "👁️ Глаз Эндера",
                    "💧 Слеза Гаста", "🌋 Сгусток магмы", "🐲 Дыхание дракона", "🧪 Зелье невидимости"
                ),
            }
        }

        json_dump(themes)
        MAIN_THEMES = tuple(themes["Main_themes"])
        return themes, MAIN_THEMES


def json_dump(themes: dict):
    """Сохраняет обновлённый словарь тем в файл JSON.

    Args:
        themes: Словарь тем со словами.
    """
    with open('themes.json', 'w', encoding='utf-8') as file:
        json.dump(themes, file, indent=4, ensure_ascii=False)


def send_photo(subsidiary, MAIN_THEMES, idx):
    if subsidiary[-1] in MAIN_THEMES:
        lst_parts = subsidiary[idx].split("_")
        path = f"images/{subsidiary[-1]}/{lst_parts[2]}.jpg"
    elif subsidiary[-2] not in MAIN_THEMES:
        return
    elif subsidiary[idx] == "live":
        path = f"images/{subsidiary[-2]}/{subsidiary[-1]}.jpg"
    else:
        path = f"images/shpion.jpg"
    with open(path, 'rb') as file:
        return file.read()