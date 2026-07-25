# Подключаем встроенные модули и библиотеки:
import random

# Подключаем свои модули:
import logic
import printer

# Нужные функции:

def game_dist(game_list: dict, chat_id: str) -> list:
    """Отвечает за основную игру и распределяет информацию по другим функциям.

    Args:
        game_list: Cловарь с параметрами игры.
        chat_id: ID чата пользователя.

    """
    themes = game_list['themes']
    lst_players = game_list['lst_players']
    user_theme = game_list['user_theme']
    game_mode = game_list['game_mode']
    num_shpions = game_list['num_shpions']
    if game_mode == 'classic':
        return classic(lst_players, user_theme, themes, chat_id, num_shpions)
    else:
        return chaos(lst_players, user_theme, themes, chat_id)


def chaos(lst_players: list, user_theme: str, themes: dict, chat_id: str) -> list:
    """Случайно выбирает и запускает 1 из 4 режимов Хаоса с шансом 25%.

    Args:
        lst_players: Список игроков.
        user_theme: Тема, которая выбрана пользователем в начале игры.
        themes: Словарь тем со словами.
        chat_id: ID чата пользователя.
    """
    mode_chaos = random.randint(1, 100)

    if mode_chaos <= 25:
        shpions = lst_players
        secret_word = logic.sec_word(user_theme, themes, chat_id)
        return create_roles(lst_players, user_theme, secret_word, shpions)

    elif mode_chaos <= 50:
        shpions = ""
        secret_word = logic.sec_word(user_theme, themes, chat_id)
        return create_roles(lst_players, user_theme, secret_word, shpions)

    elif mode_chaos <= 75:
        return random_secret_word(lst_players, user_theme, themes, chat_id)

    else:
        return classic(lst_players, user_theme, themes, chat_id)


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


def create_roles(lst_players: list, user_theme: str, secret_word: str, shpions: list) -> list:
    """Определяет роль (Шпион или Мирный) для каждого игрока.

    Args:
        lst_players: Список игроков.
        user_theme: Тема, которая выбрана пользователем в начале игры.
        secret_word: Секретное слово, которое должны отгадать Шпион(-ы).
        shpions: Список Шпионов.
    """
    all_roles = []
    for _, name in enumerate(lst_players):
        if name in shpions:
           all_roles.append(printer.text_roles("shpion", user_theme, secret_word))
        else:
            all_roles.append(printer.text_roles("live", user_theme, secret_word))
    return all_roles


def random_secret_word(lst_players: list, user_theme: str, themes: dict, chat_id: str) -> list:
    """Раздаёт каждому игроку индивидуальное случайное слово из выбранной темы.

    Args:
        lst_players: Список игроков.
        user_theme: Тема, которая выбрана пользователем в начале игры.
        themes: Словарь тем со словами.
        chat_id: ID чата пользователя.
    """
    all_roles = []
    for _ in enumerate(lst_players):
        secret_word = logic.sec_word(user_theme, themes, chat_id)
        all_roles.append(printer.text_roles("live", user_theme, secret_word))
    return all_roles
