import sqlite3
import uuid
import random
import string
import bcrypt

class User:
    def __init__(self, db_name='users.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                uuid TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def unique_user_id_generator(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    def signup(self, username, password):
        user_uuid = self.unique_user_id_generator()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            self.cursor.execute('INSERT INTO users (uuid, username, password) VALUES (?, ?, ?)', 
                                (user_uuid, username, hashed_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def login(self, username, password):
        self.cursor.execute('SELECT password FROM users WHERE username=?', (username,))
        user = self.cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
            return True
        else:
            return False

    def add_user(self, username, password):
        return self.signup(username, password)

    def get_user_uuid(self, username):
        return self.cursor.execute('SELECT uuid FROM users WHERE username=?', (username,)).fetchone()[0]

    def delete_user(self, username):
        self.cursor.execute('DELETE FROM users WHERE username=?', (username,))
        self.conn.commit()
        if self.cursor.rowcount > 0:
            return True
        else:
            return False

    def close_connection(self):
        self.conn.close()

# Example usage:
if __name__ == "__main__":
    user_manager = User()
    # print(user_manager.signup("alice", "password123"))  # Sign up a user
    # print(user_manager.login("alice", "password123"))    # Log in the user
    # print(user_manager.delete_user("alice"))              # Delete the user
    # user_manager.close_connection()

    # brand_manager = BrandRegistration()
    
    # # Adding a brand
    # success = brand_manager.add_data(
    #     brand_name="Tech Innovators",
    #     brand_tagline="Innovating the Future",
    #     industry="Technology",
    #     brand_description="A leading tech company focusing on innovative solutions.",
    #     primary_color="#FF5733",
    #     secondary_color="#C70039",
    #     complementary_color="#FFC300",
    #     brand_keywords="technology, innovation, future"
    # )
    # print("Brand added:", success)

    # # Editing a brand
    # success = brand_manager.edit_data("some-uuid", brand_tagline="Shaping Tomorrow")  # Replace with a valid UUID
    # print("Brand updated:", success)

    # # Deleting a brand
    # success = brand_manager.delete_data("some-uuid")  # Replace with a valid UUID
    # print("Brand deleted:", success)

    # # Closing connection
    # brand_manager.close_connection()