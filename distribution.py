# Подключаем встроенные модули и библиотеки:
from random import randint

# Подключаем свои модули:
import logic
import printer

# Нужные функции:
def game_dist(game_session) -> list:
    """Отвечает за основную игру и распределяет информацию по другим функциям.

    Args:
        game_session: Класс с параметрами игры.
        themes: Словарь тем со словами

    """
    lst_players = game_session.lst_players
    user_theme = game_session.user_theme
    game_mode = game_session.game_mode
    num_shpions = game_session.num_shpions
    chat_id = game_session.chat_id
    themes = logic.db_all_themes(chat_id)
    if game_mode == 'classic':
        return classic(lst_players, user_theme, themes, chat_id, num_shpions)
    else:
        return chaos(lst_players, user_theme, themes, chat_id)


def classic(lst_players: list, user_theme: str, themes: dict, chat_id: str, num_shpions: int = 1) -> list:
    """Создает классическую игру и распределяет данные по другим функциям.

     Args:
         lst_players: Список игроков.
         user_theme: Тема, которая выбрана пользователем в начале игры.
         themes: Словарь тем со словами.
         chat_id: ID чата пользователя.
         num_shpions: Максимальное кол-во Шпионов.
     """
    shpions = logic.create_shpion(num_shpions, lst_players)
    secret_word = logic.sec_word(user_theme, themes, chat_id)
    return create_roles(lst_players, user_theme, secret_word, shpions)


def chaos(lst_players: list, user_theme: str, themes: dict, chat_id: str) -> list:
    """Случайно выбирает и запускает 1 из 4 режимов Хаоса с шансом 25%.

    Args:
        lst_players: Список игроков.
        user_theme: Тема, которая выбрана пользователем в начале игры.
        themes: Словарь тем со словами.
        chat_id: ID чата пользователя.
    """
    mode_chaos = randint(1, 100)

    if mode_chaos <= 25:
        shpions = lst_players
        secret_word = logic.sec_word(user_theme, themes, chat_id)
        return create_roles(lst_players, user_theme, secret_word, shpions)

    elif mode_chaos <= 50:
        shpions = []
        secret_word = logic.sec_word(user_theme, themes, chat_id)
        return create_roles(lst_players, user_theme, secret_word, shpions)

    elif mode_chaos <= 75:
        return random_secret_word(lst_players, user_theme, themes, chat_id)

    else:
        return classic(lst_players, user_theme, themes, chat_id)


def random_secret_word(lst_players: list, user_theme: str, themes: dict, chat_id: str) -> list:
    """Раздаёт каждому игроку индивидуальное случайное слово из выбранной темы.

    Args:
        lst_players: Список игроков.
        user_theme: Тема, которая выбрана пользователем в начале игры.
        themes: Словарь тем со словами.
        chat_id: ID чата пользователя.
    """
    all_roles = []
    subsidiary = []
    for _ in enumerate(lst_players):
        secret_word = logic.sec_word(user_theme, themes, chat_id)
        all_roles.append(printer.text_roles("live", user_theme, secret_word))
        subsidiary.append(f"random_live_{secret_word}")
    subsidiary.append(user_theme)
    return all_roles, subsidiary


def create_roles(lst_players: list, user_theme: str, secret_word: str, shpions: list) -> list:
    """Определяет роль (Шпион или Мирный) для каждого игрока.

    Args:
        lst_players: Список игроков.
        user_theme: Тема, которая выбрана пользователем в начале игры.
        secret_word: Секретное слово, которое должны отгадать Шпион(-ы).
        shpions: Список Шпионов.
    """
    all_roles = []
    subsidiary = []
    for idx in lst_players:
        if idx in shpions:
           all_roles.append(printer.text_roles("shpion", user_theme, secret_word))
           subsidiary.append("shpion")
        else:
            all_roles.append(printer.text_roles("live", user_theme, secret_word))
            subsidiary.append("live")
    subsidiary.append(user_theme), subsidiary.append(secret_word)
    return all_roles, subsidiary
