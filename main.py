# Подключаем встроенные модули и библиотеки:
from telebot import types

# Подключаем свои модули:
import distribution as dist
import button
import printer
import server
from loader import bot
from logic import game
from logic import themes
from logic import database as db
from logic import utils
from logic import models

# Нужные переменные:
game_session = models.ManagerGames()

# Нужные функции:
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
    session = game_session.get_game(chat_id)
    call_data = call.data.split('_')
    if call_data[0] == 'nav':
        call_data.pop(0)
    action = call_data[1]

    if session == None and action != 'start':
        bot.answer_callback_query(call.id, printer.TEXT_ALERT_RELOAD_GAME, show_alert=True)
        utils.edit_message(printer.TEXT_OLD_SESSION, call, button.markup_start())
        return

    elif action == 'start':
        game_session.create_game(chat_id)
        utils.edit_message(printer.TEXT_NUM_PLAYERS, call, button.markup_main_create([button.markup_num_players], ['main-menu', "game"]))

    elif action == 'players':
        session.lst_players = game.lst_players(int(call_data[2]))
        print(session.lst_players, call_data[2])
        logic.edit_message(printer.TEXT_CHOICE_THEME, call, button.markup_main_create([button.markup_all_themes, logic.db_only_themes(chat_id), chat_id, "game"], ['game', 'start']))

    elif action == 'theme':
        session.user_theme = call_data[2]
        utils.edit_message(printer.TEXT_GAME_MODE, call, button.markup_main_create([button.markup_game_mode], ['game', 'players', len(session.lst_players)]))

    elif action == 'mode':
        data = call_data[2]
        session.game_mode = data
        if data == 'classic' and len(session.lst_players) > 5:
            utils.edit_message(printer.TEXT_NUM_SHPIONS, call, button.markup_main_create([button.markup_num_shpions], ['game', 'theme', session.user_theme]))

        else:
            session.num_shpions = 1
            lst_settings = game.current_games(session)
            utils.edit_message(printer.text_current_game(lst_settings), call, button.markup_main_create([button.markup_go, "game_go"], ['game', 'theme', session.user_theme]))

    elif action == 'shpion':
        data = call_data[2]
        session.num_shpions = int(data)
        lst_settings = game.current_games(session)
        utils.edit_message(printer.text_current_game(lst_settings), call, button.markup_main_create([button.markup_go, "game_go"], ['game', 'theme', session.user_theme]))

    elif action == 'go':
        utils.edit_message(printer.TEXT_START_GAME, call, button.markup_chek_role())
        user_roles, subsidiary = dist.game_dist(session)
        session.subsidiary = subsidiary
        session.user_roles = user_roles
        session.player_index = 0

    elif action == 'chek-role':
        idx = session.player_index
        print("session:", session)
        print("user_roles:", session.user_roles if session else "SESSION IS NONE")
        player_role = session.user_roles[idx]
        player_idx = session.lst_players[idx]
        game.send_role_message(session.subsidiary, idx, call, player_idx, player_role)

    elif action == 'hide-role':
        session.player_index += 1
        idx = session.player_index
        total_players = len(session.lst_players)
        bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        if idx < total_players:
            bot.send_message(chat_id, printer.TEXT_NEXT_PLAYER, "Markdown", reply_markup=button.markup_chek_role())

        else:
            game_session.delete_game(chat_id)
            bot.send_message(chat_id, printer.TEXT_FINISH_ROLES,"Markdown", reply_markup=button.markup_back(["main-menu", "game"], "🔙 Назад в Главное меню"))


@bot.callback_query_handler(func=lambda call: call.data.startswith('themes_'))
def call_themes(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    call_data = call.data.split('_')
    if call_data[0] == 'nav':
        call_data.pop(0)
    action = call_data[1]

    if action == "start":
        utils.edit_message(printer.TEXT_THEMES, call, button.markup_main_create([button.markup_themes], ["main-menu", "game"]))

    elif action == 'create':
        utils.edit_message(printer.TEXT_MENU_CREATE, call, button.markup_main_create([button.markup_go, "themes_create-theme"],["themes", "start"]))

    elif action == 'create-theme':
        sent = utils.edit_message(printer.TEXT_CREATE_THEME, call, button.markup_back(["themes", "create"], "🔙 Назад"))
        bot.clear_step_handler_by_chat_id(chat_id)
        bot.register_next_step_handler(sent, themes.get_theme_name, themes.db_all_themes())

    elif action == 'delete':
        if db.db_only_themes(chat_id, "user") == {}:
            bot.answer_callback_query(call.id, printer.TEXT_ALERT_NO_THEME, show_alert=True)
            logic.edit_message(printer.TEXT_DELETE_NO_THEME, call, button.markup_back(["themes", "start"], "🔙 Назад в 📂 ТЕМЫ"))
        else:
            utils.edit_message(printer.TEXT_MENU_DELETE, call, button.markup_main_create([button.markup_go, "themes_delete-theme"], ["themes", "start"]))

    elif action == 'delete-theme':
        utils.edit_message(printer.TEXT_THEME_DELETE, call,
                           button.markup_main_create([button.markup_delete_theme, db.db_only_themes(chat_id, "user"), chat_id], ["themes", "delete"]))

    elif action == 'delete-finish':
        themes.delete_theme(call_data[2], str(chat_id))
        utils.edit_message(printer.TEXT_FINISH_DELETE, call, button.markup_back(["themes", "start"], "🔙 Назад в 📂 ТЕМЫ"))

    elif action == 'extra':
        utils.edit_message(printer.TEXT_INF_ABOUT_THEME, call,
                button.markup_main_create([button.markup_all_themes, logic.db_only_themes(chat_id), str(chat_id), "themes"], ["themes", "start"]))

    elif action == 'theme':
        name_theme = call_data[2]
        ALL_THEMES = db.db_all_themes()
        if name_theme in db.db_only_themes(chat_id, "main"):
            num_words = len(ALL_THEMES["Main_themes"][name_theme])
        else:
            num_words = len(ALL_THEMES[str(chat_id)][name_theme])
        utils.edit_message(printer.text_settings_theme(name_theme, num_words), call,
                button.markup_main_create([button.markup_settings_theme, name_theme], ["themes","extra"]))

    elif action == 'view-words':
        lst_words, choice_theme, status = themes.view_words(db.db_all_themes(chat_id), call_data[2], chat_id, "view")
        utils.edit_message(printer.text_view_words(lst_words, choice_theme, status), call, button.markup_main_create([button.markup_download_txt, choice_theme], ["themes", "theme", choice_theme]))

    elif action == "download-txt":
        lst_words, choice_theme, status = themes.view_words(db.db_all_themes(chat_id), call_data[2], chat_id, "download")
        utils.send_txt(chat_id, lst_words)

    elif action == "rename":
        choice_theme = call_data[2]
        sent = utils.edit_message(printer.TEXT_CREATE_THEME, call, button.markup_go_or_back())
        bot.clear_step_handler_by_chat_id(chat_id)
        bot.register_next_step_handler(sent, themes.get_theme_name, db.db_all_themes(chat_id), "no", choice_theme)

    elif action == "add_words":
        choice_theme = call_data[2]
        sent = utils.edit_message(printer.TEXT_CREATE_WORDS, call, button.markup_go_or_back())
        bot.clear_step_handler_by_chat_id(chat_id)
        bot.register_next_step_handler(sent, themes.get_theme_words, choice_theme, db.db_all_themes(chat_id), add_words="add")

    elif action == "words_rename":
        choice_theme = call_data[2]
        sent = utils.edit_message(printer.TEXT_CREATE_WORDS, call, button.markup_go_or_back())
        bot.clear_step_handler_by_chat_id(chat_id)
        bot.register_next_step_handler(sent, themes.get_theme_words, choice_theme, db.db_all_themes(chat_id))


@bot.callback_query_handler(func=lambda call: call.data.startswith('inf_'))
def call_information(call: types.CallbackQuery):
    call_data = call.data.split('_')
    if call_data[0] == 'nav':
        call_data.pop(0)
    action = call_data[1]

    if action == 'start':
        utils.edit_message(printer.TEXT_ABOUT_BOT, call, button.markup_main_create([button.markup_about_bot], ["main-menu", "inf"]))

    elif action == "help":
        utils.edit_message(printer.TEXT_CONNECT_AUTHOR, call, button.markup_main_create([button.markup_contact_author], ["inf", "start"]))

    elif action == "tell-friends":
        utils.edit_message(printer.TEXT_SHARE_FRIEND, call, button.markup_back(["inf", "help"]))


@bot.callback_query_handler(func=lambda call: call.data.startswith('nav_'))
def call_nav(call: types.CallbackQuery):
    call_data = call.data.split('_')
    action = call_data[1]


    if action == 'main-menu':
        utils.edit_message(printer.TEXT_WELCOME, call, button.markup_start())

    elif action == 'game':
        call_game(call)

    elif action == 'themes':
        call_themes(call)

    elif action == 'inf':
        call_information(call)

# server.start_server()

bot.polling(none_stop=True)
