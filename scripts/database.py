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
    
    def add_user(self, id, name):
        self.cursor.execute(f"INSERT INTO users (name, discord_id) VALUES ('{name}', {id})")
        
    def add_anime_char(self, id, name, animeeng, animejp):
        self.cursor.execute(f"INSERT INTO char_inventory (discord_id, char_name, char_anime_eng, char_anime_rom) VALUES ({id}, '{name}', '{animeeng}', '{animejp}')")
        
database = Connector(Config.host, Config.user, Config.password, Config.db)