import sqlite3

CONN = sqlite3.connect('player_results.db')
CURSOR = CONN.cursor()