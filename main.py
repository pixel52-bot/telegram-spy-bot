# Подключаем встроенные модули и библиотеки:
from telebot import types
import time

# Подключаем свои модули:
import loader
import logic
import distribution as dist
import button
import printer
from loader import bot

# Нужные переменные:
current_games = {}  # Параметры текущей игры.
ALL_THEMES, MAIN_THEMES = logic.json_load() # Словарь всех тем со словами и список основных тем.

# Нужные функции:
def create_current_game(chat_id: types.CallbackQuery):
    """Создаёт все нужные данные о текущей игре.

    Args:
        chat_id: ID ата пользователя.

    Returns:
        Словарь с данными о игре.
    """
    current_games[chat_id] = {
        'lst_players': None,
        'game_mode': None,
        'user_theme': None,
        'num_shpions': 1,
        'player_index': 0,
        'subsidiary': None,
        "user_roles": None,
    }


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    """Выводит текст приветствия и кнопки главного меню.

    Args:
        message: Объект сообщения от пользователя, содержащий текст команды и данные о чате и пользователе.
    """
    bot.send_message(message.chat.id, printer.TEXT_WELCOME, reply_markup=button.markup_start(), parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data.startswith('game_'))
def call_game(call: types.CallbackQuery):
    """Отвечает за обработку нажатия и распределяет данные в функции и переменные.

    Args:
        call: Объект запроса, содержащий информацию о callback_data, пользователе и нажатой кнопке
    """
    chat_id = call.message.chat.id
    call_data = call.data.split('_')
    if call_data[0] == 'nav':
        call_data.pop(0)
    action = call_data[1]

    if chat_id not in current_games and action != 'start':
        bot.answer_callback_query(call.id, printer.TEXT_ALERT_RELOAD_GAME, show_alert=True)
        logic.edit_message(printer.TEXT_OLD_SESSION, call, button.markup_start())
        return

    elif action == 'start':
        create_current_game(chat_id)
        logic.edit_message(printer.TEXT_NUM_PLAYERS, call, button.markup_main_create([button.markup_num_players], ['main-menu', "game"]))

    elif action == 'players':
        lst_players = logic.lst_players(int(call_data[2]))
        current_games[chat_id]['lst_players'] = lst_players

        if not ALL_THEMES:
            bot.answer_callback_query(call.id, printer.TEXT_ALERT_NO_THEME, show_alert=True)
            logic.edit_message(printer.TEXT_GAME_NO_THEME, call, button.markup_start())
            return

        else:
            logic.edit_message(printer.TEXT_CHOICE_THEME, call, button.markup_main_create([button.markup_all_themes, ALL_THEMES, chat_id, "game"], ['game', 'start']))

    elif action == 'theme':
        current_games[chat_id]['user_theme'] = call_data[2]
        logic.edit_message(printer.TEXT_GAME_MODE, call, button.markup_main_create([button.markup_game_mode], ['game', 'players', len(current_games[chat_id]['lst_players'])]))

    elif action == 'mode':
        data = call_data[2]
        lst_players = current_games[chat_id]['lst_players']
        current_games[chat_id]['game_mode'] = data
        if data == 'classic' and len(lst_players) > 5:
            logic.edit_message(printer.TEXT_NUM_SHPIONS, call, button.markup_main_create([button.markup_num_shpions], ['game', 'theme', current_games[chat_id]['user_theme']]))

        else:
            lst_settings = logic.current_games(current_games, chat_id)
            logic.edit_message(printer.text_current_game(lst_settings), call, button.markup_main_create([button.markup_go, "game_go"], ['game', 'theme', current_games[chat_id]['user_theme']]))

    elif action == 'shpion':
        data = call_data[2]
        current_games[chat_id]['num_shpions'] = int(data)
        lst_settings = logic.current_games(current_games, chat_id)
        logic.edit_message(printer.text_current_game(lst_settings), call, button.markup_main_create([button.markup_go_or_back, 'game_go'], ['game', 'mode', "classic"]))

    elif action == 'go':
        logic.edit_message(printer.TEXT_START_GAME, call, button.markup_chek_role())
        game_data = current_games[chat_id]
        user_roles, subsidiary = dist.game_dist(game_data, str(chat_id), ALL_THEMES)
        current_games[chat_id]["subsidiary"] = subsidiary
        current_games[chat_id]['user_roles'] = user_roles

    elif action == 'chek-role':
        idx = current_games[chat_id]['player_index']
        player_role = current_games[chat_id]['user_roles'][idx]
        player_idx = current_games[chat_id]['lst_players'][idx]
        file = logic.send_photo(current_games[chat_id]["subsidiary"], MAIN_THEMES, idx)
        bot.edit_message_media(chat_id=chat_id, message_id=call.message.message_id, media=types.InputMediaPhoto(file,
                caption=printer.text_chek_role(player_idx, player_role), parse_mode="Markdown"), reply_markup=button.markup_hide_role())

    elif action == 'hide-role':
        current_games[chat_id]['player_index'] += 1
        idx = current_games[chat_id]['player_index']
        total_players = len(current_games[chat_id]['lst_players'])
        bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        if idx < total_players:
            next_player_name = current_games[chat_id]['lst_players'][idx]
            bot.send_message(chat_id, printer.TEXT_NEXT_PLAYER, "Markdown", reply_markup=button.markup_chek_role())

        else:
            bot.send_message(chat_id, printer.TEXT_FINISH_ROLES,"Markdown", reply_markup=button.markup_back(["main-menu", "game"], "🔙 Назад в Главное меню"))


@bot.callback_query_handler(func=lambda call: call.data.startswith('themes_'))
def call_themes(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    call_data = call.data.split('_')
    if call_data[0] == 'nav':
        call_data.pop(0)
    action = call_data[1]

    if action == "start":
        create_current_game(chat_id)
        logic.edit_message(printer.TEXT_THEMES, call, button.markup_main_create([button.markup_themes], ["main-menu", "game"]))

    elif action == 'create':
        logic.edit_message(printer.TEXT_MENU_CREATE, call, button.markup_main_create([button.markup_go, "themes_create-theme"],["themes", "start"]))

    elif action == 'create-theme':
        sent = logic.edit_message(printer.TEXT_CREATE_THEME, call, button.markup_back(["themes", "create"], "🔙 Назад"))
        bot.clear_step_handler_by_chat_id(chat_id)
        bot.register_next_step_handler(sent, logic.get_theme_name, ALL_THEMES)

    elif action == 'delete':
        if ALL_THEMES.get(str(chat_id)) is None:
            bot.answer_callback_query(call.id, printer.TEXT_ALERT_NO_THEME, show_alert=True)
            logic.edit_message(printer.TEXT_DELETE_NO_THEME, call, button.markup_back(["themes", "start"], "🔙 Назад в 📂 ТЕМЫ"))
        else:
            logic.edit_message(printer.TEXT_MENU_DELETE, call, button.markup_main_create([button.markup_go, "themes_delete-theme"], ["themes", "start"]))

    elif action == 'delete-theme':
        logic.edit_message(printer.TEXT_THEME_DELETE, call,
                           button.markup_main_create([button.markup_delete_theme, ALL_THEMES, str(chat_id)], ["themes", "delete"]))

    elif action == 'delete-finish':
        logic.delete_theme(ALL_THEMES, call_data[2], str(chat_id))
        logic.edit_message(printer.TEXT_FINISH_DELETE, call, button.markup_back(["themes", "start"], "🔙 Назад в 📂 ТЕМЫ"))

    elif action == 'extra':
        logic.edit_message(printer.TEXT_INF_ABOUT_THEME, call,
                button.markup_main_create([button.markup_all_themes,ALL_THEMES, str(chat_id), "themes"], ["themes", "start"]))

    elif action == 'theme':
        name_theme = call_data[2]
        if name_theme in MAIN_THEMES:
            num_words = len(ALL_THEMES["Main_themes"][name_theme])
        else:
            num_words = len(ALL_THEMES[str(chat_id)][name_theme])
        logic.edit_message(printer.text_settings_theme(name_theme, num_words), call,
                button.markup_main_create([button.markup_settings_theme, name_theme], ["themes","extra"]))

    elif action == 'view-words':
        lst_words, choice_theme, status = logic.view_words(MAIN_THEMES, ALL_THEMES, call_data[2], chat_id, "view")
        logic.edit_message(printer.text_view_words(lst_words, choice_theme, status), call, button.markup_main_create([button.markup_download_txt, choice_theme], ["themes", "theme", choice_theme]))

    elif action == "download-txt":
        lst_words, choice_theme, status = logic.view_words(MAIN_THEMES, ALL_THEMES, call_data[2], chat_id, "download")
        logic.send_txt(chat_id, lst_words)

    elif action == "rename":
        choice_theme = call_data[2]
        sent = logic.edit_message(printer.TEXT_CREATE_THEME, call, button.markup_go_or_back())
        bot.clear_step_handler_by_chat_id(chat_id)
        bot.register_next_step_handler(sent, logic.get_theme_name, ALL_THEMES, "no", choice_theme)

    elif action == "add_words":
        choice_theme = call_data[2]
        sent = logic.edit_message(printer.TEXT_CREATE_WORDS, call, button.markup_go_or_back())
        bot.clear_step_handler_by_chat_id(chat_id)
        bot.register_next_step_handler(sent, logic.get_theme_words, choice_theme, ALL_THEMES, add_words="add")

    elif action == "words_rename":
        choice_theme = call_data[2]
        sent = logic.edit_message(printer.TEXT_CREATE_WORDS, call, button.markup_go_or_back())
        bot.clear_step_handler_by_chat_id(chat_id)
        bot.register_next_step_handler(sent, logic.get_theme_words, choice_theme, ALL_THEMES)


@bot.callback_query_handler(func=lambda call: call.data.startswith('inf_'))
def call_information(call: types.CallbackQuery):
    call_data = call.data.split('_')
    if call_data[0] == 'nav':
        call_data.pop(0)
    action = call_data[1]

    if action == 'start':
        logic.edit_message(printer.TEXT_ABOUT_BOT, call, button.markup_main_create([button.markup_about_bot], ["main-menu", "inf"]))

    elif action == "help":
        logic.edit_message(printer.TEXT_CONNECT_AUTHOR, call, button.markup_main_create([button.markup_contact_author], ["inf", "start"]))

    elif action == "tell-friends":
        logic.edit_message(printer.TEXT_SHARE_FRIEND, call, button.markup_back(["inf", "help"]))


@bot.callback_query_handler(func=lambda call: call.data.startswith('nav_'))
def call_nav(call: types.CallbackQuery):
    call_data = call.data.split('_')
    action = call_data[1]


    if action == 'main-menu':
        logic.edit_message(printer.TEXT_WELCOME, call, button.markup_start())

    elif action == 'game':
        call_game(call)

    elif action == 'themes':
        call_themes(call)

    elif action == 'inf':
        call_information(call)



bot.polling(none_stop=True)


















