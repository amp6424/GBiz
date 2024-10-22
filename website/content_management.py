import sqlite3
import uuid

class ContentDataManagement:
    def __init__(self):
        self.connection = sqlite3.connect('content_data.db')
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY,
                    uuid TEXT UNIQUE,
                    prompt TEXT,
                    data TEXT
                )
            ''')
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS blogs (
                    id INTEGER PRIMARY KEY,
                    uuid TEXT UNIQUE,
                    prompt TEXT,
                    data TEXT
                )
            ''')
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS captions (
                    id INTEGER PRIMARY KEY,
                    uuid TEXT UNIQUE,
                    prompt TEXT,
                    data TEXT
                )
            ''')

    def add_post(self, uuid, prompt, data):
        with self.connection:
            self.connection.execute('''
                INSERT INTO posts (uuid, prompt, data) VALUES (?, ?, ?)
            ''', (uuid, prompt, data))

    def delete_post(self, uuid):
        with self.connection:
            self.connection.execute('''
                DELETE FROM posts WHERE uuid = ?
            ''', (uuid,))

    def add_blog(self, uuid, prompt, data):
        with self.connection:
            self.connection.execute('''
                INSERT INTO blogs (uuid, prompt, data) VALUES (?, ?, ?)
            ''', (uuid, prompt, data))

    def delete_blog(self, uuid):
        with self.connection:
            self.connection.execute('''
                DELETE FROM blogs WHERE uuid = ?
            ''', (uuid,))

    def add_caption(self, uuid, prompt, data):
        with self.connection:
            self.connection.execute('''
                INSERT INTO captions (uuid, prompt, data) VALUES (?, ?, ?)
            ''', (uuid, prompt, data))

    def delete_caption(self, uuid):
        with self.connection:
            self.connection.execute('''
                DELETE FROM captions WHERE uuid = ?
            ''', (uuid,))

# Example usage
if __name__ == "__main__":
    content_manager = ContentDataManagement()
    pass
    
    # Adding a post
    # content_manager.add_post("Sample Post", "This is the content of the sample post.")
    
    # Adding a blog
    # content_manager.add_blog("Sample Blog", "This is the content of the sample blog.")
    
    # Adding a caption
    # content_manager.add_caption("Sample Caption", "This is the content of the sample caption.")
    
    # Replace with valid UUIDs for deletion
    # content_manager.delete_post("some-uuid")
    # content_manager.delete_blog("some-uuid")
    # content_manager.delete_caption("some-uuid")
