from config import Config
import mysql.connector

class DataBase:

    def __init__(self, user, password, host, port, database):
        self.cnx = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        self.cursor = self.cnx.cursor(dictionary=True)

    async def add_user(self, user_id, name, premium):
        role = 'admin' if user_id == Config.admin_ids else 'user'
        return self.cursor.execute("""INSERT IGNORE INTO users(`user_id`, `name`, `role`, `premium`) 
                                VALUES(%s, %s, %s, %s)""", (user_id, name, role, premium))

    async def add_interests(self, interests, user_id):
        return self.cursor.execute("""UPDATE users SET interests=(%s) WHERE user_id=(%s)""",
                                   (interests, user_id))

    async def update_reacts(self, likes, dislikes, ads, post_id):
        return self.cursor.execute("""UPDATE posts SET likes=(%s), dislikes=(%s), ads=(%s) WHERE post_id=(%s)""",
                                   (likes, dislikes, ads, post_id))








