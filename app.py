import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Conversión de Temperatura: Celsius a Fahrenheit")

# Cargar los datos desde el archivo CSV
df = pd.read_csv('celsius.csv')

# Mostrar las primeras filas usando df.head()
st.subheader("Primeras filas (datos.head())")
st.dataframe(df.head())

# Mostrar el DataFrame completo en la aplicación
st.subheader("Tabla de datos (DataFrame completo)")
st.dataframe(df)

# Mostrar un gráfico lineal para visualizar la relación
st.subheader("Gráfico de relación")
st.line_chart(df, x="Celsius", y="Fahrenheit")
