# Подключаем свои модули:
from loader import supabase 

# Нужные функции:
def db_only_themes(chat_id: str, how_theme="both") -> dict:
    """Выгружает темы пользователя из базы данных Supabase.

    Returns:
        Возвращает словарь всех тем со словами.
    """
    if how_theme == "main":
        result = supabase.table("themes").select("chat_id, theme_name").eq("chat_id", -1).execute()
    elif how_theme == "user":
        result = supabase.table("themes").select("theme_name").eq("chat_id", chat_id).execute()
    else:
        result = supabase.table("themes").select("chat_id, theme_name").in_("chat_id", [-1, chat_id]).execute()
    rows = result.data
    
    themes = {"Main_themes": []}
    for row in rows:
        theme_name =  row["theme_name"]
        if row["chat_id"] == -1:
            themes["Main_themes"].append(theme_name)
        else:
            if chat_id not in themes:
                themes = {chat_id: []}
            themes[chat_id].append(theme_name)
    return themes


def db_all_themes(chat_id: int) -> dict:
    """Выгружает темы из базы данных Supabase.

    Returns:
        Возвращает словарь всех тем со словами.
    """
    result = supabase.table("themes").select("chat_id, theme_name, words").in_("chat_id", [chat_id, -1]).execute()
    rows = result.data


    themes = {"Main_themes": {}}
    for row in rows:
        chat_id, theme_name, words = row["chat_id"], row["theme_name"], row["words"]
        if chat_id == -1:
            themes["Main_themes"][theme_name] = tuple(word.strip() for word in words.split(',') if word.strip())
        else:
            if chat_id not in themes:
                themes = {chat_id: {}}
            themes[chat_id][theme_name] = tuple(word.strip() for word in words.split(',') if word.strip())

    return themes