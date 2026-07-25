# Подключаем встроенные модули и библиотеки:
from telebot import types


# Нужные функции:

def markup_chek_role() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопкой проверки роли.

    Returns:
        Объект разметки с кнопкой: 'Посмотреть кто я... 🕵️‍♂️👀'
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Посмотреть кто я... 🕵️‍♂️👀', callback_data='chek_role'))
    return markup


def markup_start() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками главного меню.

    Returns:
        Объект разметки с кнопками навигации по боту.
    """
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton(text='Правила игры 📜', url='https://telegra.ph/Pravila-igry-SHpion-06-16')
    bt2 = types.InlineKeyboardButton(text='Поддержка 🤝', url='https://t.me/Step20110')
    markup.row(bt1, bt2)
    bt3 = types.InlineKeyboardButton(text='Начать игру 🎮', callback_data='game')
    bt4 = types.InlineKeyboardButton(text='Темы со словами 📄', url='https://telegra.ph/Temy-so-slovami-06-16')
    markup.row(bt3, bt4)
    bt5 = types.InlineKeyboardButton(text='Добавить тему со словами ➕', callback_data='create')
    bt6 = types.InlineKeyboardButton(text='Удалить тему со словами ➖', callback_data='delete')
    markup.row(bt5, bt6)
    return markup


def markup_all_theme(themes: dict, chat_id: str) -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для выбора темы.

    Args:
       themes: Словарь тем со словами.
       chat_id: ID чата пользователя.

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
        markup.add(types.InlineKeyboardButton(f"📂 {num}", callback_data=num))
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


def markup_hide_role() -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопкой для скрытия роли игрока.

    Returns:
        Объект разметки с кнопкой: 'Скрыть роль 🔒❌'.
    """
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Скрыть роль 🔒❌', callback_data='hide_role'))
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


def markup_delete_theme(themes: dict, chat_id: str) -> types.InlineKeyboardMarkup:
    """Создает инлайн-клавиатру с кнопками для выбора удаления темы и кнопкой назад.

    Args:
        themes: Словарь тем со словами.
        chat_id: ID чата пользователя.

    Returns:
        Объект разметки с кнопками - доступные для удаления темы и кнопкой назад.
    """
    markup = types.InlineKeyboardMarkup()
    for nam in themes[chat_id]:
        markup.add(types.InlineKeyboardButton(text=nam, callback_data=f"delete_{nam}"))
    markup.add(types.InlineKeyboardButton(f'❌ Назад в Главное меню', callback_data="back"))
    return markup


def markup_go_or_back(have_go: int = 1, callback: str = "go", smail: str= '❌') -> types.InlineKeyboardMarkup:
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
