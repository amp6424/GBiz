import sqlite3
import google.generativeai as genai
from flask import jsonify

class ChatBot:
    def __init__(self, db_name='chatbot.db'):
        self.db_name = db_name
        self.setup_database()
        self.api_key = ""  # Replace with your actual API key
        genai.configure(api_key=self.api_key)

    def setup_database(self):
        """Set up the SQLite database and create the user_prompts table if it doesn't exist."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_prompts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                prompt TEXT NOT NULL,
                response TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def store_prompt_and_response(self, username, prompt, response):
        """Store a user prompt and the bot's response in the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user_prompts (username, prompt, response) VALUES (?, ?, ?)', 
                       (username, prompt, response))
        conn.commit()
        conn.close()

    def chat(self, username, user_input):
        """Store the prompt, get a response from the AI model, and store the response."""
        # Call the Gemini API
        model = genai.GenerativeModel("gemini-1.5-flash")  # Example model name
        response = model.generate_content(user_input + "answer everything in a plain text only. Keep it as concise as possilbe.")

        # Store the prompt and the response in the database
        self.store_prompt_and_response(username, user_input, response.text)

        return {"response": response.text}
