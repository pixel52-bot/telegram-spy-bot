# Подключаем встроенные модули и библиотеки:
from telebot import types

# Нужные функции:
def markup_start() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками главного меню.

    Returns:
        Объект разметки с кнопками навигации по боту.
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='🎮 Начать игру', callback_data='game'))
    bt2 = types.InlineKeyboardButton(text='ℹ️ О Боте', callback_data='about_bot')
    bt3 = types.InlineKeyboardButton(text='📂 Темы', callback_data='themes')
    markup.row(bt2, bt3)
    return markup


def markup_num_players() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для выбора количества игроков.

    Returns:
        Объект разметки с кнопками-цифрами, означающими количество игроков.
    """
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('3️⃣ ', callback_data='3')
    bt2 = types.InlineKeyboardButton('4️⃣', callback_data='4')
    bt3 = types.InlineKeyboardButton('5️⃣', callback_data='5')
    bt4 = types.InlineKeyboardButton('6️⃣', callback_data='6')
    markup.row(bt1, bt2, bt3, bt4)
    bt5 = types.InlineKeyboardButton('7️⃣', callback_data='7')
    bt6 = types.InlineKeyboardButton('8️⃣', callback_data='8')
    bt7 = types.InlineKeyboardButton('9️⃣', callback_data='9')
    bt8 = types.InlineKeyboardButton('🔟', callback_data='10')
    markup.row(bt5, bt6, bt7, bt8)
    return markup


def markup_all_themes(themes: dict, chat_id: str, callback_prefix: str) -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для выбора темы.

    Args:
       themes: Словарь тем со словами.
       chat_id: ID чата пользователя.
       callback_prefix: Вид вызова функции.

    Returns:
        Объект разметки с кнопками доступных тем.
    """
    chat_id = str(chat_id)
    if chat_id in list(themes):
        need_themes = list(themes["Main_themes"]) + list(themes[chat_id])
    else:
        need_themes = themes["Main_themes"]
    markup = types.InlineKeyboardMarkup()
    for num in need_themes:
        markup.add(types.InlineKeyboardButton(f"📂 {num}", callback_data=f"{callback_prefix}_{num}"))
    return markup


def markup_game_mode() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для выбора режима.

    Returns:
        Объект разметки с кнопками режимов игры.
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📜 Классика", callback_data="classic"))
    markup.add(types.InlineKeyboardButton("🎲 Хаос", callback_data="chaos"))
    return markup


def markup_num_shpions() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для выбора количества Шпионов.

    Returns:
        Объект разметки с кнопками-цифрами, означающими количество Шпионов.
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🕵️‍♂️ 1', callback_data='num_shpion_1'))
    markup.add(types.InlineKeyboardButton('🕵️‍♂️️ 2 🕵️‍♂️', callback_data='num_shpion_2'))
    return markup


def markup_chek_role() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопкой проверки роли.

    Returns:
        Объект разметки с кнопкой: 'Посмотреть кто я... 🕵️‍♂️👀'
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Посмотреть кто я... 🕵️‍♂️👀', callback_data='chek_role'))
    return markup


def markup_hide_role() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопкой для скрытия роли игрока.

    Returns:
        Объект разметки с кнопкой: 'Скрыть роль 🔒❌'.
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Скрыть роль 🔒❌', callback_data='hide_role'))
    return markup


def markup_about_bot() -> types.InlineKeyboardMarkup:
    """Создаёт инлайн-клавиатуру с кнопками для раздела "ℹ️ О Боте".

    Returns:
        Объект разметки с кнопками: ссылки и связь с автором.
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='📜 Правила игры', url='https://telegra.ph/Pravila-igry-SHpion-06-16'))
    markup.add(types.InlineKeyboardButton(text='💻 Проэкт на GitHub', url="https://github.com/pixel52-bot/telegram-spy-bot"))
    markup.add(types.InlineKeyboardButton(text='👤 Связь с автором', callback_data='author'))
    markup.add(types.InlineKeyboardButton(text='❌ Назад в Главное меню', callback_data="back"))
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
    bt3 = types.InlineKeyboardButton(text='📢 Рассказать друзьям', callback_data="tell_friends")
    bt4 = types.InlineKeyboardButton(text='❤️ Поддержать', url='https://t.me/Step20110')
    markup.row(bt3, bt4)
    markup.add(types.InlineKeyboardButton(text='❌ Назад в Главное меню', callback_data="back"))
    return markup


def markup_themes() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для раздела "📂 Темы".

        Returns:
            Объект разметки с кнопками: ссылки на мой ТГ и c кнопкой: "📢 Рассказать друзьям".
        """
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton(text='➕ Создать тему', callback_data='create')
    bt2 = types.InlineKeyboardButton(text='🗑️ Удалить тему', callback_data='delete')
    markup.row(bt1, bt2)
    markup.add(types.InlineKeyboardButton(text='📋 Дополнительно', callback_data='extra'))
    markup.add(types.InlineKeyboardButton(text='❌ Назад в Главное меню', callback_data="back"))
    return markup


def markup_delete_theme(themes: dict, chat_id: str) -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для выбора удаления темы и кнопкой назад.

    Args:
        themes: Словарь тем со словами.
        chat_id: ID чата пользователя.

    Returns:
        Объект разметки с кнопками: доступные для удаления темы и кнопкой назад.
    """
    markup = types.InlineKeyboardMarkup()
    for nam in themes[chat_id]:
        markup.add(types.InlineKeyboardButton(text=nam, callback_data=f"delete_{nam}"))
    markup.add(types.InlineKeyboardButton(f'❌ Назад в Главное меню', callback_data="back"))
    return markup


def markup_settings_theme() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для раздела "📋 Дополнительно" из отдела "📂 Темы".

    Returns:
        Объект разметки с кнопками для редактирования тем.
        """
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton(text='👁️ Посмотреть слова', callback_data='view_word')
    bt2 = types.InlineKeyboardButton(text='✏️ Переименовать тему', callback_data='rename_theme')
    markup.row(bt1, bt2)
    bt3 = types.InlineKeyboardButton(text='➕ Добавить слова', callback_data='add_words')
    bt4 = types.InlineKeyboardButton(text='✏️ Изменить слова', callback_data='rename_words')
    markup.row(bt4, bt3)
    markup.add(types.InlineKeyboardButton(text='❌ Назад в Главное меню', callback_data="back"))
    return markup


def markup_go_or_back(have_go: int = 1, callback: str = "go", smail: str = '❌') -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для выбора назад и возможно вперёд.

    Args:
        have_go: Флажок, для проверки на надобность кнопки: '🚀 Поехали! / Начать'
        callback: Строка, которая нужна, для действия кнопки 'Вперёд'.
        smail: Смайл, который подставляеться в кнопку 'Назад'.

    Returns:
        Объект разметки с кнопками.
    """
    markup = types.InlineKeyboardMarkup()
    if have_go == 2:
        markup.add(types.InlineKeyboardButton('🚀 Поехали! / Начать', callback_data=callback))
    markup.add(types.InlineKeyboardButton(f'{smail} Назад в Главное меню', callback_data="back"))
    return markup
