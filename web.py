import sqlite3


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = self.create_connection(db_name)
        self.cursor = self.conn.cursor()
        self.initialize_database()

    def create_connection(self, db_name):
        conn = sqlite3.connect(db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def search_games(self, name):
        self.cursor.execute("SELECT id, title FROM games WHERE title LIKE ?", ('%' + name + '%',))
        return self.cursor.fetchall()

    def get_game(self, game_id):
        self.cursor.execute("SELECT * FROM games WHERE id=?", (game_id,))
        return self.cursor.fetchone()

    def initialize_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT NOT NULL
            )
        ''')



import pandas as pd
import streamlit as st
import bs4
import requests

def main():
    st.title("Game Search App")

    db_manager = DatabaseManager("fitgirl.db")

    # Search Games
    search_term = st.text_input("Search for games", key='search_input')
    if search_term:
        games = db_manager.search_games(search_term)
        if games:  # ensure games are not empty
            games_df = pd.DataFrame(games, columns=["id", "title"]).set_index("id")
            st.dataframe(games_df)

    # Get Game URL
    game_id = st.number_input("Enter Game ID to get URL", min_value=0, value=0, step=1, key='id_input')
    if game_id:
        game = db_manager.get_game(game_id)
        if game is None:
            st.write(f"Game with id {game_id} is not found.")
        else:
            req = requests.get(game['url'])
            soup = bs4.BeautifulSoup(req.text, 'html.parser')
            magnet = soup.find('a', string='magnet')
            st.write(f"{magnet.attrs.get("href")}")


if __name__ == "__main__":
    main()