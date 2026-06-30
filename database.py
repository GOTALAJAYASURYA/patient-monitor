import sqlite3
from datetime import datetime

DB_FILE = "patient.db"

def init_db():
    """Creates the database file and the vitals table if it doesn't exist yet"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create a table with columns for tracking our simulated data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vitals_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            pulse INTEGER,
            spo2 INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()

def save_vitals(temperature, pulse, spo2):
    """Saves a single set of vitals into our database with the current time"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get current time in Hour:Minute:Second format
    current_time = datetime.now().strftime("%H:%M:%S")
    
    cursor.execute('''
        INSERT INTO vitals_history (timestamp, temperature, pulse, spo2)
        VALUES (?, ?, ?, ?)
    ''', (current_time, temperature, pulse, spo2))
    
    conn.commit()
    conn.close()