import sqlite3
from uuid import uuid4

from config import DATABASE_FILE


class Database:
    def __init__(self, db_file=DATABASE_FILE):
        self.db_file = db_file

        database = sqlite3.connect(self.db_file)
        cursor = database.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT,
            desc TEXT,
            likes INT,
            dislikes INT,
            author_name TEXT
            )""")

        database.commit()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT,
            password TEXT,
            email TEXT,
            uuid TEXT
            )""")

        database.commit()
        database.close()

    def create_acc(self, username: str, password: str, email: str):
        database = sqlite3.connect(self.db_file)
        cursor = database.cursor()

        _uuid = uuid4()

        print(_uuid)

        cursor.execute(f"""
                INSERT INTO accounts (username, password, email, uuid) 
                VALUES ('{username}', '{password}', '{email}', '{_uuid}')""")

        database.commit()
        database.close()

    def get_acc_by_username(self, username: str):
        database = sqlite3.connect(self.db_file)
        cursor = database.cursor()

        cursor.execute(f"SELECT * FROM accounts WHERE username = '{username}'")
        acc = cursor.fetchone()

        database.close()

        return acc

    def get_acc_by_uuid(self, _uuid: str):
        database = sqlite3.connect(self.db_file)
        cursor = database.cursor()

        cursor.execute(f"SELECT * FROM accounts WHERE uuid = '{_uuid}'")
        acc = cursor.fetchone()

        database.close()

        return acc

    def add_video(self, name, desc, author_name):
        database = sqlite3.connect(self.db_file)
        cursor = database.cursor()

        cursor.execute("""
        INSERT INTO videos (name, desc, likes, dislikes, author_name) 
        VALUES (?, ?, 0, 0, ?)""", (name, desc, author_name))

        database.commit()
        database.close()

    def get_video(self, video_id):
        database = sqlite3.connect(self.db_file)
        cursor = database.cursor()

        cursor.execute("SELECT * FROM videos WHERE id = ?", (video_id,))
        r = cursor.fetchone()

        database.close()

        if not r:
            return None

        columns = [desc[0] for desc in cursor.description]
        video_dict = dict(zip(columns, r))

        return video_dict

    def change_video(self, video_id, name=None, desc=None, author_name=None):
        old_v = self.get_video(video_id)

        database = sqlite3.connect(self.db_file)
        cursor = database.cursor()

        if name is None:
            name = old_v["name"]
        if desc is None:
            desc = old_v["desc"]
        if author_name is None:
            author_name = old_v["author_name"]

        cursor.execute("UPDATE videos SET name = ?, desc = ?, author_name = ? WHERE id = ?", (name, desc, author_name, video_id))

        database.commit()
        database.close()

    def like_video(self, video_id):
        database = sqlite3.connect(self.db_file)
        cursor = database.cursor()

        cursor.execute("UPDATE videos SET likes = likes + 1 WHERE id =?", (video_id,))

        database.commit()
        database.close()

    def dislike_video(self, video_id):
        database = sqlite3.connect(self.db_file)
        cursor = database.cursor()

        cursor.execute("UPDATE videos SET dislikes = dislikes + 1 WHERE id =?", (video_id,))

        database.commit()
        database.close()

    def get_videos(self):
        database = sqlite3.connect(self.db_file)
        cursor = database.cursor()

        cursor.execute("SELECT * FROM videos")
        videos = cursor.fetchall()

        # Convert tuples to dictionaries
        columns = [desc[0] for desc in cursor.description]
        videos = [dict(zip(columns, row)) for row in videos]

        videos.sort(key=lambda x: x["likes"] - x["dislikes"], reverse=True)

        database.close()

        return videos


if __name__ == "__main__":
    db = Database()
    db.add_video("Как устроен PNG", "Описание потом придумаю", "eleday")
    db.add_video("Автомонтаж видео на Python", "писание потом придумаю", "eleday")
