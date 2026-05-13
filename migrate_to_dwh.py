import pandas as pd
from sqlalchemy import create_engine
import os

def migrate_data():
    # 1. Configuración de rutas
    csv_file = 'celsius.csv'
    db_file = 'data werehouse/data_warehouse.db'
    
    if not os.path.exists(csv_file):
        print(f"Error: No se encontró el archivo {csv_file}")
        return

    # 2. Cargar datos desde el CSV
    print(f"Leyendo datos de {csv_file}...")
    df = pd.read_csv(csv_file)
    
    # 3. Conectar al "Data Warehouse" (SQLite local)
    print(f"Conectando al Data Warehouse {db_file}...")
    engine = create_engine(f'sqlite:///{db_file}')
    
    # 4. Cargar datos en la tabla 'temperature_data'
    # Usamos if_exists='replace' para esta demostración
    df.to_sql('temperature_data', con=engine, if_exists='replace', index=False)
    
    print("Migracion completada con exito.")
    print(f"Los datos ahora residen en la tabla 'temperature_data' dentro de {db_file}")

if __name__ == "__main__":
    migrate_data()
