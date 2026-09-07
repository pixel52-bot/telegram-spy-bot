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
"""
lst_inf_func1 = ["ing"]
print(lst_inf_func1[0])
print((lst_inf_func1[1:]))