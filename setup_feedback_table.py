import sqlite3
import datetime

def setup_table():
    db_file = 'data werehouse/data_warehouse.db'
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Crear tabla de logs si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            celsius_input REAL,
            fahrenheit_output REAL
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Tabla 'predictions_log' configurada en {db_file}")

if __name__ == "__main__":
    setup_table()
