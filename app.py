import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# Configuración de página
st.set_page_config(page_title="Predicción de Temperatura", page_icon="🌡️", layout="wide")

# Título y Encabezado
st.title("🌡️ Conversor Inteligente: Celsius a Fahrenheit")
st.markdown("""
Esta aplicación utiliza **Inteligencia Artificial (Regresión Lineal)** para aprender y predecir 
temperaturas en base a datos históricos. ¡Descubre cómo se relacionan los grados Celsius y Fahrenheit!
""")

# Cargar los datos de forma optimizada
@st.cache_data
def load_data():
    return pd.read_csv('celsius.csv')

df = load_data()

# Preparar y entrenar modelo
X = df[['Celsius']]
y = df['Fahrenheit']
modelo = LinearRegression()
modelo.fit(X, y)

# Crear un diseño de dos columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader("🤖 Predicción Interactiva")
    st.markdown("Usa el deslizador de abajo para probar el modelo con cualquier temperatura:")
    
    # Input interactivo
    celsius_input = st.slider("Selecciona °Celsius:", min_value=-50, max_value=100, value=25, step=1)
    
    # Realizar la predicción
    fahrenheit_pred = modelo.predict([[celsius_input]])[0]
    
    # Tarjeta de métrica con un diseño más limpio
    st.metric(label="Resultado en Fahrenheit", value=f"{fahrenheit_pred:.2f} °F")
    
    st.success(f"¡El modelo estima que **{celsius_input} °C** son **{fahrenheit_pred:.2f} °F**!")

with col2:
    st.subheader("📈 Relación de Datos")
    # Gráfico mejorado que ocupa su columna
    st.line_chart(df, x="Celsius", y="Fahrenheit")

st.divider()

# Datos brutos al final en un desplegable para mantener la interfaz limpia
with st.expander("📊 Ver los datos originales (Dataset)"):
    col_data1, col_data2 = st.columns(2)
    with col_data1:
        st.markdown("**Vista rápida (primeras filas):**")
        st.dataframe(df.head(), use_container_width=True)
    with col_data2:
        st.markdown("**Dataset completo:**")
        st.dataframe(df, use_container_width=True)
