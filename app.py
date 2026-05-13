import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

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

# --- Modelo de Machine Learning ---
st.subheader("🤖 Predicción con Machine Learning")
st.write("Hemos entrenado un modelo de Regresión Lineal con los datos anteriores. Usa el deslizador para predecir.")

# Preparar los datos
X = df[['Celsius']] # Características (Input)
y = df['Fahrenheit'] # Etiqueta (Output)

# Crear y entrenar el modelo
modelo = LinearRegression()
modelo.fit(X, y)

# Input interactivo del usuario
celsius_input = st.slider("Selecciona una temperatura en Celsius:", min_value=-50, max_value=100, value=0)

# Realizar la predicción
fahrenheit_pred = modelo.predict([[celsius_input]])[0]

# Mostrar el resultado de forma destacada
st.success(f"**{celsius_input} °C** equivalen aproximadamente a **{fahrenheit_pred:.2f} °F** según el modelo.")
