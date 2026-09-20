# Подключаем встроенные модули и библиотеки:
from telebot import types

# Подключаем свои модули:
import button
import printer
from loader import bot
from loader import supabase 

# Нужные функции:
def create_theme(theme_name: str, words: tuple, chat_id: str):
    """Создаёт тему со словами от пользователя.

    Args:
        themes: Словарь тем со словами.
        theme_name: Тема, введённая от пользователя.
        words: Слова, введённая от пользователя
        chat_id: ID чата пользователя.
    """
    words = ", ".join(words)
    supabase.table("themes").insert({"chat_id": chat_id, "theme_name": theme_name, "words": words}).execute()


def rename_theme(choice_theme, new_theme, chat_id, themes):
    themes[str(chat_id)][new_theme] = themes[str(chat_id)].pop(choice_theme)


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

    need_words = list(word.strip() for word in message.text.split(',') if word.strip())

    if not need_words:
        bot.send_message(message.chat.id, printer.TEXT_ERROR_CREATE_WORDS, parse_mode='Markdown')
        return
    
    chat_id = message.chat.id
    create_theme(new_theme, need_words, str(chat_id))
    bot.send_message(chat_id, printer.TEXT_CREATE_FINISH, reply_markup=button.markup_back(["themes", "start"],"🔙 Назад в 📂 ТЕМЫ"), parse_mode='Markdown')


def delete_theme(delete_theme: str, chat_id: str):
    """Удаляет тему, выбранную пользователем, кроме 4 основных тем.

    Args:
        themes: Словарь тем со словами.
        delete_theme: Тема, которую нужно удалить
        chat_id: ID чата пользователя.
    """
    supabase.table("themes").delete().eq("chat_id" == chat_id, "theme_name" == delete_theme).execute()


def view_words(themes: dict, choice_theme: str, chat_id: int, act):
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