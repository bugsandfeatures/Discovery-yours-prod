from config import Config
import mysql.connector

class DataBase:

    def __init__(self, user, password, host, port, database):
        self.cnx = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        self.cursor = self.cnx.cursor(dictionary=True)

    async def add_user(self, user_id, name, premium):
        role = 'admin' if user_id == Config.admin_ids else 'user'
        try:
            return self.cursor.execute("""INSERT IGNORE INTO users(`user_id`, `name`, `role`, `premium`) 
                                    VALUES(%s, %s, %s, %s)""", (user_id, name, role, premium))
        except Exception as e:
            print(e)

    async def add_interests(self, interests, user_id):
        try:
            return self.cursor.execute("""UPDATE users SET interests=(%s) WHERE user_id=(%s)""",
                                       (interests, user_id))
        except Exception as e:
            print(e)

    async def update_reacts(self, likes, dislikes, ads, post_id):
        try:
            return self.cursor.execute("""UPDATE posts SET likes=(%s), dislikes=(%s), ads=(%s) WHERE post_id=(%s)""",
                                       (likes, dislikes, ads, post_id))
        except Exception as e:
            print(e)

    async def insert_reacts_ads(self, user_id, post_id):
        try:
            return self.cursor.execute("""INSERT INTO reacts(user_id, post_id, rating, date) 
                                        VALUES (%s, %s, %s, CURRENT_TIMESTAMP)""",
                                       (user_id, post_id, 3))
        except Exception as e:
            print(e)

    async def insert_reacts_like(self, user_id, post_id):
        try:
            return self.cursor.execute("""INSERT INTO reacts(user_id, post_id, rating, date) 
                                        VALUES (%s, %s, %s, CURRENT_TIMESTAMP)""",
                                       (user_id, post_id, 2))
        except Exception as e:
            print(e)

    async def insert_reacts_dislike(self, user_id, post_id):
        try:
            return self.cursor.execute("""INSERT INTO reacts(user_id, post_id, rating, date) 
                                        VALUES (%s, %s, %s, CURRENT_TIMESTAMP)""",
                                       (user_id, post_id, 1,))
        except Exception as e:
            print(e)








