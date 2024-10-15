import mysql.connector

class Config:
    """Class for the database configs"""
    host = "127.0.0.1"
    user = "root"
    password = ""
    db = "hmh"
    
class Connector:
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self._init_db()
        
    def _init_db(self):
        self.database = mysql.connector.connect(host=self.host, user=self.user, password=self.password, autocommit=True)
        self.cursor = self.database.cursor(buffered=True)
        self.cursor.execute(f"USE {self.db}")
        
    def check_user(self, id):
        self.cursor.execute(f"SELECT discord_id FROM users WHERE discord_id = '{id}'")
        result = self.cursor.fetchall()
        if result:
            return True
        else:
            return False
    
    def add_user(self, id, name, level, xp, growth, messages, warns):
        self.cursor.execute(f"INSERT INTO users (name, discord_id, level, xp, growth, messages, warns) VALUES ('{name}', {id}, {level}, {xp}, {growth}, {messages}, {warns})")
        self.cursor.execute(f"INSERT INTO economy (user_id, balance) VALUES ({id}, 100)")
        
    def add_anime_char(self, id, name, animeeng, animejp, image, new_collection_id):
        self.cursor.execute(f"INSERT INTO char_inventory (discord_id, char_name, char_anime_eng, char_anime_rom, image_url, collection_id) VALUES ({id}, '{name}', '{animeeng}', '{animejp}', '{image}', {new_collection_id})")
        
    def add_xp(self, id, value):
        self.cursor.execute(f"UPDATE users SET xp = xp + {value} WHERE discord_id = '{id}'")
        
    def get_leveling_info(self, id):
        self.cursor.execute(f"SELECT level, xp, growth FROM users WHERE discord_id = '{id}'")
        return self.cursor.fetchall()[0]
    
    def level_up(self, id):
        self.cursor.execute(f"UPDATE users SET level = level + 1 WHERE discord_id = '{id}'")
        self.cursor.execute(f"UPDATE users SET xp = 0 WHERE discord_id = '{id}'")
        self.cursor.execute(f"UPDATE users SET growth = growth + 0.025 WHERE discord_id = '{id}'")
        
    def get_balance(self, id):
        self.cursor.execute(f"SELECT balance FROM economy WHERE user_id = '{id}'")
        return self.cursor.fetchall()[0][0]
    
    def get_level(self, id):
        self.cursor.execute(f'SELECT level FROM users WHERE discord_id = "{id}"')
        return self.cursor.fetchall()[0][0]
    
    def get_status(self, id):
        self.cursor.execute(f"SELECT status FROM users WHERE discord_id = '{id}'")
        return self.cursor.fetchall()[0][0]
    
    def get_message_count(self, id):
        self.cursor.execute(f"SELECT messages FROM users WHERE discord_id = '{id}'")
        return self.cursor.fetchall()[0][0]
        
database = Connector(Config.host, Config.user, Config.password, Config.db)