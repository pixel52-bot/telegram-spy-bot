# Подключаем встроенные модули и библиотеки:
import random

from logic import utils
from telebot import types
from loader import bot
from logic import database as db
import printer
import button


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


def current_games(game_session):
    count_players = len(game_session.lst_players)
    num_shpions = game_session.num_shpions
    user_theme = game_session.user_theme
    game_mode = game_session.game_mode

    if game_mode == 'classic':
        mode_display = "📜 Классика"
        shpions_text = f"*{num_shpions}* 🕵️‍♂️"
        peace_text = f"*{count_players - num_shpions}* 🧑‍🌾"
    else:
        mode_display = "🎲 Хаос"
        shpions_text = "_Случайно_ 🔮"
        peace_text = "_Случайно_ 🔮"
    return [count_players, peace_text, shpions_text, user_theme, mode_display]


def send_role_message(subsidiary, idx, call, player_idx, player_role):
    """Отправляет сообщение с ролью игрока и соответствующим изображением."""
    main_themes = db.db_only_themes(call.message.chat.id, "main")
    result = utils.send_foto(subsidiary, main_themes, idx)
    if result == None:
        utils.edit_message(printer.printer.text_chek_role(player_idx, player_role), call, reply_markup=button.markup_hide_role())
    else:
        file = game.send_role_message(subsidiary, main_themes, idx)
        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=types.InputMediaPhoto(file,
                caption=printer.text_chek_role(player_idx, player_role), parse_mode="Markdown"), reply_markup=button.markup_hide_role())
        