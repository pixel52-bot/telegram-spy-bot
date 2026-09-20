"""
themes = {
            "Main_themes": {
                "Локации 📍": [
                    "🏫 Школа", "🧸 Детский сад", "🎓 Университет", "🏥 Больница", "🩺 Поликлиника", "💊 Аптека",

                ],
                "Clash Royal 👑": [
                    "⚔️ Рыцарь", "🏹 Лучницы", "🪵 Гигант", "💣 Бомбер", "🏰 Принцесса(Башня)", "💀 Скелеты", "🟢 Гоблины"
                ],
                "Видеоигры🎮": [
                    "🧱 Minecraft", "🔫 Counter-strike 2 (CS 2)", "⚔️ Dota 2", "🚗 GTA 5", "🏡 Sims", "🧸 Roblox"
                ],

                "Minecraft 🧱": [
                    "🪨 Бедрок", "🧱 Булыжник", "🪨 Глубинный сланец", "🪨 Туф", "🪨 Кальцит", "🪨 Диорит", "🪨 Андезит"
                ],

            },
    "52": {
        "niga": ( " Бедрок", " Булыжник", " Глубинный сланец", " Туф", " Кальцит", " Диорит", " Андезит", ),
        "pencil": ( " Бедрок", " Булыжник", " Глубинный сланец", " Туф", ),
    }

}
choice_theme = "niga"
new_theme = "pisa"
themes[str(52)][new_theme] = themes[str(52)].pop(choice_theme)
print(themes["Main_themes"]["Локации 📍"])
themes["Main_themes"]["Локации 📍"].pop(0)
print(themes["Main_themes"]["Локации 📍"])


def gey():
    print("Hello")

def goy(need_func):
    need_func()

def gam():
    goy(gey)

gam()

lst_inf_func1 = ["ing"]
print(lst_inf_func1[0])
print((lst_inf_func1[1:]))

chat_id = "52"
class GAME:
    def __init__(self, user_id, theme, user_name):
        self.user_id = user_id
        self.theme = theme
        self.user_name = user_name


game_session = GAME([52, "пикачу"], "игорь", 52)
game_session.user_name += 1
print(game_session.user_id[1])
print(game_session.user_name)
"""
# import json

# import sqlite3

# ['Локации 📍', 'Clash Royal 👑', 'Видеоигры🎮', 'Minecraft 🧱']
# import json



# with open("themes.json", "r", encoding='utf-8') as f:
#     themes = json.load(f)


# db =  sqlite3.connect("bot.db")

# c = db.cursor()

# c.execute("""CREATE TABLE IF NOT EXISTS themes (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             chat_id integer,
#             theme_name text,
#             words text,



            
# )""")
# c.execute("ALTER TABLE themes DROP COLUMN is_system")
# words = ", ".join(words)
# c.execute("INSERT INTO themes (chat_id, theme_name, words) VALUES (?, ?,  ?)", (-1, 'Clash Royal 👑', words))
# c.execute("DELETE FROM themes WHERE theme_name = ?", ('Clash Royal 👑',))
# c.execute("SELECT chat_id, theme_name FROM themes")
# print(c.fetchall())
# themes = themes[0][0]
# n_themes = json.loads(themes)
# print(n_themes)
# index_word = n_themes["Main_themes"]['Локации 📍'].append("🏥 Больница")
# th = json.dumps(n_themes, ensure_ascii=False)
# c.execute("UPDATE niga SET themes = ?", (th,))
# db.commit()
# db.close()
# print(themes)
# for row in themes["Main_themes"]:
#     name_theme = row
#     words = list(themes["Main_themes"][name_theme])
#     words1 = ", ".join(words)
#     nice = {
#         "chat_id": -1,
#         "theme_name": name_theme,
#         "words": words1
#     }

# result = supabase.table("themes").insert({"chat_id": 52, "theme_name": "Новая", "words": "Слово1, Слово2"}).execute()

# result = supabase.table("themes").delete().eq("chat_id", 52).execute()

# from loader import supabase


# def db_all_themes() -> dict:
#     """Выгружает темы из базы данных Supabase.

#     Returns:
#         Возвращает словарь всех тем со словами.
#     """
#     result = supabase.table("themes").select("chat_id, theme_name, words").execute()
#     rows = result.data


#     themes = {"Main_themes": {}}
#     for row in rows:
#         chat_id, theme_name, words = row["chat_id"], row["theme_name"], row["words"]
#         if chat_id != -1:
#             themes[chat_id] = {}
#             themes[chat_id][theme_name] = tuple(word.strip() for word in words.split(',') if word.strip())
#         themes["Main_themes"][theme_name] = tuple(word.strip() for word in words.split(',') if word.strip())

#     return themes

# print(db_all_themes())

# def db_user_themes(chat_id: str) -> dict:
#     """Выгружает темы пользователя из базы данных Supabase.

#     Returns:
#         Возвращает словарь всех тем со словами.
#     """
#     result = supabase.table("themes").select("chat_id, theme_name").eq("chat_id", chat_id).execute()
#     rows = result.data
#     user_theme = {}
#     for row in rows:
#         chat_id, theme_name = row["chat_id"], row["theme_name"]
#         user_theme[chat_id] = [theme_name]
#         print(user_theme)
#     return user_theme

# db_user_themes(52)

# def letters_by_frequency(values):

#     dct = {}
#     for val in values:
#         dct[val] = values.count(val)
#     sorted_dct = sorted(dct.items(), key=lambda x: x[1])
#     print(sorted_dct)
#     lst = []
#     for i in range(len(sorted_dct)):
#         lst.append(sorted_dct[i][0])
#     print(lst)



# values = "abracadabra"
# letters_by_frequency(values)
# def letters_by_frequency(chars):
#     frequencies = {}
    
#     for char in chars:
#         char_lower = char.lower()
#         if 'a' <= char_lower <= 'z':
#             frequencies[char_lower] = frequencies.get(char_lower, 0) + 1
            
#     sorted_letters = sorted(frequencies.items(), key=lambda x: (x[1], x[0]))
#     return [letter for letter, count in sorted_letters]
# with open("input.txt") as f:
#     file = f.read()
#     values = file.split()
# N, K = values[0], values[1]
# values.pop(0)
# values.pop(1)
# print(values)
# shaded = 0
# for i in range(int(K + K)):
#     R, L = values[i], values[]
# print(values)

# import sqlite3

# db = sqlite3.connect("upload.sqlite")
# cursor = db.cursor() 

# i = 1
# while i != 301:
#     c.execute("SELECT base_price FROM products WHERE id=?", (i,))
#     price = c.fetchall()
#     price = price[0][0]
#     price = price + (price / 100 * 10)
#     print(price)
#     c.execute("UPDATE products SET price_with_markup = ? WHERE id = ?", (price, i))
#     i += 1
# cursor.execute("SELECT base_price FROM products LIMIT 10")
# print(cursor.fetchall())

# db.commit()
# db.close()

