# Подключаем встроенные модули и библиотеки:
from telebot import types
import os

# Подключаем свои модули:
from loader import bot

# Нужные функции:
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


def send_foto(subsidiary, themes, idx):
    """Отправляет сообщение с ролью игрока и соответствующим изображением."""
    
    if subsidiary[-1] in themes["Main_themes"]:
        lst_parts = subsidiary[idx].split("_")
        path = f"images/{subsidiary[-1]}/{lst_parts[2]}.jpg"

    elif subsidiary[-2] not in themes["Main_themes"]:
        return None
    
    elif subsidiary[idx] == "live":
        path = f"images/{subsidiary[-2]}/{subsidiary[-1]}.jpg"
    else:
        path = f"images/shpion.jpg"

    with open(path, 'rb') as file:
        return file.read()