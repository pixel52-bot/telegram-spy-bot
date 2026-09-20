# Нужные классы:
class GameSession:
    def __init__(self, chat_id=None):
        self.chat_id = chat_id
        self.lst_players = None
        self.game_mode = None
        self.user_theme = None
        self.subsidiary = None
        self.user_roles = None
        self.num_shpions = 1
        self.player_index = 0


class ManagerGames:
    games_sessions = {}

    def create_game(self, chat_id):
        session = GameSession(chat_id)
        self.games_sessions[chat_id] = session
        return session


    def get_game(self, chat_id):
        return self.games_sessions.get(chat_id, None)


    def delete_game(self, chat_id):
        self.games_sessions.pop(chat_id, None)