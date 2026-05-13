import pandas as pd
from sqlalchemy import create_engine

def clean_data():
    db_file = 'data werehouse/data_warehouse.db'
    engine = create_engine(f'sqlite:///{db_file}')
    
    # 1. Cargar datos 'raw'
    print("Extrayendo datos raw del warehouse...")
    df = pd.read_sql('SELECT * FROM temperature_data', con=engine)
    initial_count = len(df)
    
    # 2. Limpieza de Duplicados
    df = df.drop_duplicates()
    
    # 3. Manejo de Valores Nulos
    df = df.dropna()
    
    # 4. Filtro de Outliers (Valores atípicos)
    # Por ejemplo, temperaturas Celsius entre -100 y 1000
    df = df[(df['Celsius'] >= -100) & (df['Celsius'] <= 1000)]
    
    # 5. Guardar en la tabla 'cleaned'
    print(f"Limpieza completada: {initial_count} -> {len(df)} filas.")
    df.to_sql('temperature_data_cleaned', con=engine, if_exists='replace', index=False)
    print("Datos limpios guardados en la tabla 'temperature_data_cleaned'.")

if __name__ == "__main__":
    clean_data()
