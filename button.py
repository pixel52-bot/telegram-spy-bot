# Подключаем встроенные модули и библиотеки:
from telebot import types

# Нужные функции:
def markup_start() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками главного меню.

    Returns:
        Объект разметки с кнопками навигации по боту.
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='🎮 Начать игру', callback_data='game_start'))
    bt2 = types.InlineKeyboardButton(text='ℹ️ О Боте', callback_data='inf_start')
    bt3 = types.InlineKeyboardButton(text='📂 Темы', callback_data='themes_start')
    markup.row(bt2, bt3)
    return markup


def markup_num_players() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для выбора количества игроков.

    Returns:
        Объект разметки с кнопками-цифрами, означающими количество игроков.
    """
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('3️⃣ ', callback_data='game_players_3')
    bt2 = types.InlineKeyboardButton('4️⃣', callback_data='game_players_4')
    bt3 = types.InlineKeyboardButton('5️⃣', callback_data='game_players_5')
    bt4 = types.InlineKeyboardButton('6️⃣', callback_data='game_players_6')
    markup.row(bt1, bt2, bt3, bt4)
    bt5 = types.InlineKeyboardButton('7️⃣', callback_data='game_players_7')
    bt6 = types.InlineKeyboardButton('8️⃣', callback_data='game_players_8')
    bt7 = types.InlineKeyboardButton('9️⃣', callback_data='game_players_9')
    bt8 = types.InlineKeyboardButton('🔟', callback_data='game_players_10')
    markup.row(bt5, bt6, bt7, bt8)
    return markup


def markup_all_themes(lst_inf_func) -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для выбора темы.

    Args:
       themes: Словарь тем со словами.
       chat_id: ID чата пользователя.
       callback_prefix: Вид вызова функции.

    Returns:
        Объект разметки с кнопками доступных тем.
    """
    themes = lst_inf_func[0]
    chat_id = str(lst_inf_func[1])
    callback_prefix = lst_inf_func[2]
    if chat_id in list(themes):
        need_themes = list(themes["Main_themes"]) + list(themes[chat_id])
    else:
        need_themes = themes["Main_themes"]
    markup = types.InlineKeyboardMarkup()
    for num in need_themes:
        markup.add(types.InlineKeyboardButton(f"📂 {num}", callback_data=f"{callback_prefix}_theme_{num}"))
    return markup


def markup_game_mode() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для выбора режима.

    Returns:
        Объект разметки с кнопками режимов игры.
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📜 Классика", callback_data="game_mode_classic"))
    markup.add(types.InlineKeyboardButton("🎲 Хаос", callback_data="game_mode_chaos"))
    return markup


def markup_num_shpions() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для выбора количества Шпионов.

    Returns:
        Объект разметки с кнопками-цифрами, означающими количество Шпионов.
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🕵️‍♂️ 1', callback_data='game_shpion_1'))
    markup.add(types.InlineKeyboardButton('🕵️‍♂️️ 2 🕵️‍♂️', callback_data='game_shpion_2'))
    return markup


def markup_chek_role() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопкой проверки роли.

    Returns:
        Объект разметки с кнопкой: 'Посмотреть кто я... 🕵️‍♂️👀'
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Посмотреть кто я... 🕵️‍♂️👀', callback_data='game_chek-role'))
    return markup


def markup_hide_role() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопкой для скрытия роли игрока.

    Returns:
        Объект разметки с кнопкой: 'Скрыть роль 🔒❌'.
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Скрыть роль 🔒❌', callback_data='game_hide-role'))
    return markup


def markup_about_bot() -> types.InlineKeyboardMarkup:
    """Создаёт инлайн-клавиатуру с кнопками для раздела "ℹ️ О Боте".

    Returns:
        Объект разметки с кнопками: ссылки и связь с автором.
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='📜 Правила игры', url='https://telegra.ph/Pravila-igry-SHpion-06-16'))
    markup.add(types.InlineKeyboardButton(text='💻 Проэкт на GitHub', url="https://github.com/pixel52-bot/telegram-spy-bot"))
    markup.add(types.InlineKeyboardButton(text='👤 Связь с автором', callback_data='inf_help'))
    return markup


def markup_contact_author() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для раздела "👤 Связь с автором".

        Returns:
            Объект разметки с кнопками: ссылки на мой ТГ и c кнопкой: "📢 Рассказать друзьям".
        """
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton(text='🐞 Сообщить об ошибке', url='https://t.me/Step20110')
    bt2 = types.InlineKeyboardButton(text='💡 Предложить идею', url='https://t.me/Step20110')
    markup.row(bt1, bt2)
    bt3 = types.InlineKeyboardButton(text='📢 Рассказать друзьям', callback_data="inf_tell-friends")
    bt4 = types.InlineKeyboardButton(text='❤️ Поддержать', url='https://t.me/Step20110')
    markup.row(bt3, bt4)
    return markup


def markup_themes() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для раздела "📂 Темы".

        Returns:
            Объект разметки с кнопками: ссылки на мой ТГ и c кнопкой: "📢 Рассказать друзьям".
        """
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton(text='➕ Создать тему', callback_data='themes_create')
    bt2 = types.InlineKeyboardButton(text='🗑️ Удалить тему', callback_data='themes_delete')
    markup.row(bt1, bt2)
    markup.add(types.InlineKeyboardButton(text='📋 Дополнительно', callback_data='themes_extra'))
    return markup


def markup_delete_theme(lst_inf_func) -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для выбора удаления темы и кнопкой назад.

    Args:
        themes: Словарь тем со словами.
        chat_id: ID чата пользователя.

    Returns:
        Объект разметки с кнопками: доступные для удаления темы и кнопкой назад.
    """
    themes = lst_inf_func[0]
    chat_id = lst_inf_func[1]
    markup = types.InlineKeyboardMarkup()
    for name in themes[chat_id]:
        markup.add(types.InlineKeyboardButton(text=name, callback_data=f"themes_delete-finish_{name}"))
    return markup


def markup_settings_theme(lst_inf_func) -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для раздела "📋 Дополнительно" из отдела "📂 Темы".

    Returns:
        Объект разметки с кнопками для редактирования тем.
        """
    choice_theme = lst_inf_func[0]
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton(text='👁️ Посмотреть слова', callback_data=f'themes_view-words_{choice_theme}')
    bt2 = types.InlineKeyboardButton(text='✏️ Переименовать тему', callback_data=f'themes_rename_{choice_theme}')
    markup.row(bt1, bt2)
    bt3 = types.InlineKeyboardButton(text='➕ Добавить слова', callback_data=f'themes_add_words_{choice_theme}')
    bt4 = types.InlineKeyboardButton(text='✏️ Изменить слова', callback_data=f'themes_words-rename_{choice_theme}')
    markup.row(bt4, bt3)
    return markup


def markup_go(lst_inf_func) -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для выбора назад и возможно вперёд.

    Args:
        callback: Строка, которая нужна, для действия кнопки 'Вперёд'.


    Returns:
        Объект разметки с кнопками.
    """
    callback  = lst_inf_func[0]
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🚀 Поехали! / Начать', callback_data=callback))
    return markup


def markup_download_txt(lst_inf_func) -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопкой для скачивания файла со словами."""
    choice_theme = lst_inf_func[0]
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⬇️ Скачать файл со словами", callback_data=f"themes_download-txt_{choice_theme}"))
    return markup


def markup_back(lst_inf_func, text="🔙 Назад") -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    if len(lst_inf_func) == 2:
        information = ""
    else:
        information = lst_inf_func[2]
    markup.add(types.InlineKeyboardButton(text, callback_data=f"nav_{lst_inf_func[0]}_{lst_inf_func[1]}_{information}"))
    return markup


def markup_main_create(lst_inf_func: list, lst_inf_back: list, text="🔙 Назад") -> types.InlineKeyboardMarkup:
    if len(lst_inf_func) == 1:
        markup1 = lst_inf_func[0]()
    else:
        markup1 = lst_inf_func[0](lst_inf_func[1:])
    markup2 = markup_back(lst_inf_back, text)
    markup1.keyboard = markup1.keyboard + markup2.keyboard
    return markup1