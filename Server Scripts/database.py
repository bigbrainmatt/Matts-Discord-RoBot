import sqlite3
import os

class Database:
    def __init__(self, guild_id):
        self.guild_id = guild_id
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_folder = os.path.join(base_dir, "databases")
        self.db_path = os.path.join(db_folder, f"{guild_id}.db")
        self._create_tables()

    def _create_tables(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_folder = os.path.join(base_dir, "databases")
        if not os.path.exists(db_folder):
            os.makedirs(db_folder)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS LOGS (
                log_type TEXT PRIMARY KEY,
                channel_id INTEGER PRIMARY KEY,
                enabled INTEGER NOT NULL DEFAULT 1,
                webhook_url TEXT,
            )
        ''')
        conn.commit()
        conn.close()

    def get_log_channel(self, log_type):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT channel_id FROM LOGS WHERE log_type = ?', (log_type,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def set_log_channel(self, log_type, channel_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO LOGS (log_type, channel_id) VALUES (?, ?)
            ON CONFLICT(log_type) DO UPDATE SET channel_id = ?
        ''', (log_type, channel_id, channel_id))
        conn.commit()
        conn.close()

    def get_webhook_url(self, log_type):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT webhook_url FROM LOGS WHERE log_type = ?', (log_type,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def set_webhook_url(self, log_type, webhook_url):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO LOGS (log_type, webhook_url) VALUES (?, ?)
            ON CONFLICT(log_type) DO UPDATE SET webhook_url = ?
        ''', (log_type, webhook_url, webhook_url))
        conn.commit()
        conn.close()

    def remove_log(self, log_type):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM LOGS WHERE log_type = ?', (log_type,))
        conn.commit()
        conn.close()