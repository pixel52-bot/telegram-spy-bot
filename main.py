# Подключаем встроенные модули и библиотеки:
from telebot import types

# Подключаем свои модули:
import logic
import distribution as dist
import button
import printer
from loader import bot

# Токен ВАШЕГО бота:

# Нужная переменная
current_games = {}  # Параметры текущей игры.

# Нужные функции:

def create_current_game(chat_id: types.CallbackQuery):
    """Создаёт все нужные данные о текущей игре.

    Args:
        chat_id: ID ата пользователя.

    Returns:
        Словарь с данными о игре.
    """
    current_games[chat_id] = {
        'themes': logic.json_load(),
        'lst_players': None,
        'game_mode': None,
        'user_theme': None,
        'num_shpions': 1,
        'player_index': 0,
        "user_roles": None,
    }

@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    """Выводит текст приветствия и кнопки главного меню.

    Args:
        message: Объект сообщения от пользователя, содержащий текст команды и данные о чате и пользователе.
    """
    start_markup = button.markup_start()
    bot.send_message(message.chat.id, printer.text_welcome(), reply_markup=start_markup, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def callback(call: types.CallbackQuery):
    """Отвечает за обработку нажатия и распределяет данные в функции и переменные.

    Args:
        call: Объект запроса, содержащий информацию о callback_data, пользователе и нажатой кнопке
    """
    chat_id = call.message.chat.id

    if chat_id not in current_games and call.data not in ('game', "create", 'delete'):
        bot.answer_callback_query(call.id, printer.text_reload_game(), show_alert=True)
        logic.edit_message(printer.text_old_session(), call, button.markup_start())
        return

    elif call.data == 'game':
        create_current_game(chat_id)
        logic.edit_message(printer.text_num_players(), call, button.markup_num_players())

    elif call.data == 'create':
        create_current_game(chat_id)
        logic.edit_message(printer.text_create_theme("clarification"), call, button.markup_go_or_back(2, 'create_theme'))

    elif call.data == 'delete':
        create_current_game(chat_id)
        themes = current_games[chat_id]['themes']

        if themes.get(str(chat_id)) is None:
            bot.answer_callback_query(call.id, printer.text_no_theme('alert'), show_alert=True)
            logic.edit_message(printer.text_no_theme(type_error="error_delete"), call, button.markup_go_or_back())
        else:
            logic.edit_message(printer.text_delete_theme("clarification"), call, button.markup_go_or_back(2, 'delete_theme'))

    elif call.data == 'delete_theme':
        themes = current_games[chat_id]['themes']
        logic.edit_message(printer.text_delete_theme("delete_theme"), call, button.markup_delete_theme(themes, str(chat_id)))

    elif call.data[:7] == 'delete_':
        themes = current_games[chat_id]['themes']
        logic.delete_theme(themes, call.data[7:], str(chat_id))
        logic.edit_message(printer.text_delete_theme("success"), call, button.markup_go_or_back(smail='🔄'))

    elif call.data == 'create_theme':
        sent = logic.edit_message(printer.text_create_theme("theme"), call, button.markup_go_or_back())
        themes = current_games[chat_id]['themes']
        bot.clear_step_handler_by_chat_id(chat_id)
        bot.register_next_step_handler(sent, logic.get_theme_name, themes)

    elif call.data.isdigit():
        lst_players = logic.players(int(call.data))
        current_games[chat_id]['lst_players'] = lst_players
        themes = current_games[chat_id]['themes']

        if not themes:
            bot.answer_callback_query(call.id, printer.text_no_theme('alert'), show_alert=True)
            start_markup = button.markup_start()
            logic.edit_message(printer.text_no_theme(type_error="error_startup"), call, start_markup)
            return

        else:
            logic.edit_message(printer.text_choice_theme(), call, button.markup_all_theme(themes, chat_id))

    elif call.data in ("Локации 📍", "Minecraft 🧱", "Видеоигры🎮", "Clash Royal 👑") or \
    call.data in current_games[chat_id]['themes'].get(str(chat_id), []):
        current_games[chat_id]['user_theme'] = call.data
        logic.edit_message(printer.text_game_mode(), call, button.markup_game_mode())

    elif call.data == 'classic' or call.data == 'chaos':
        lst_players = current_games[chat_id]['lst_players']
        current_games[chat_id]['game_mode'] = call.data

        if call.data == 'classic' and len(lst_players) > 5:
            logic.edit_message(printer.text_num_shpions(), call, button.markup_num_shpions())

        else:
            logic.edit_message(printer.text_current_game(current_games, chat_id), call,
                         button.markup_go_or_back(2, 'go_game'))

    elif call.data == 'num_shpion_1' or call.data == 'num_shpion_2':
        current_games[chat_id]['num_shpions'] = int(call.data[-1])
        logic.edit_message(printer.text_current_game(current_games, chat_id), call, button.markup_go_or_back(2, 'go_game'))

    elif call.data == 'back':
        start_markup = button.markup_start()
        logic.edit_message(printer.text_welcome(), call, start_markup)

    elif call.data == "go_game":
        first_player = current_games[chat_id]['lst_players'][0]
        logic.edit_message(printer.text_start_game(first_player), call, button.markup_chek_role())
        game_data = current_games[chat_id]
        user_roles = dist.game_dist(game_data, str(chat_id))
        current_games[chat_id]['user_roles'] = user_roles

    elif call.data == 'chek_role':
        idx = current_games[chat_id]['player_index']
        player_role = current_games[chat_id]['user_roles'][idx]
        player_name = current_games[chat_id]['lst_players'][idx]
        logic.edit_message(printer.text_chek_role(player_name, player_role), call, button.markup_hide_role())

    elif call.data == 'hide_role':
        current_games[chat_id]['player_index'] += 1
        idx = current_games[chat_id]['player_index']
        total_players = len(current_games[chat_id]['lst_players'])

        if idx < total_players:
            next_player_name = current_games[chat_id]['lst_players'][idx]
            logic.edit_message(printer.text_next_player(next_player_name), call, button.markup_chek_role())

        else:
            logic.edit_message(printer.text_finish_roles(), call, button.markup_go_or_back(smail='🔄'))


bot.polling(none_stop=True)
