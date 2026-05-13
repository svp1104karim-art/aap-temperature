import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine

# Configuración de página
st.set_page_config(page_title="Predicción de Temperatura", page_icon="🌡️", layout="wide")

# Título y Encabezado
st.title("🌡️ Conversor Inteligente: Celsius a Fahrenheit")
st.markdown("""
Esta aplicación utiliza **Inteligencia Artificial (Regresión Lineal)** para aprender y predecir 
temperaturas en base a datos históricos. ¡Descubre cómo se relacionan los grados Celsius y Fahrenheit!
""")
st.sidebar.success("✅ Conectado al Data Warehouse: Datos Limpios y Auditados")

# Cargar los datos de forma optimizada
@st.cache_data
def load_data():
    # Conexión al Data Warehouse (SQLite)
    # Usamos la tabla LIMPIA para el entrenamiento
    engine = create_engine('sqlite:///data werehouse/data_warehouse.db')
    return pd.read_sql('SELECT * FROM temperature_data_cleaned', con=engine)

df = load_data()

# Preparar y entrenar modelo
X = df[['Celsius']]
y = df['Fahrenheit']
modelo = LinearRegression()
modelo.fit(X, y)

def save_prediction(celsius, fahrenheit):
    engine = create_engine('sqlite:///data werehouse/data_warehouse.db')
    log_df = pd.DataFrame({
        'timestamp': [datetime.datetime.now()],
        'celsius_input': [celsius],
        'fahrenheit_output': [fahrenheit]
    })
    log_df.to_sql('predictions_log', con=engine, if_exists='append', index=False)

# Organización por Pestañas
tab_predict, tab_analysis, tab_history = st.tabs(["🔮 Predicción Interactiva", "📊 Análisis Avanzado", "📜 Historial (DWH Audit)"])

with tab_predict:
    # Crear un diseño de dos columnas
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🤖 Probar el Modelo")
        st.markdown("Usa el deslizador para predecir temperaturas:")
        
        # Input interactivo
        celsius_input = st.slider("Selecciona °Celsius:", min_value=-50, max_value=100, value=25, step=1)
        
        # Realizar la predicción
        fahrenheit_pred = modelo.predict([[celsius_input]])[0]
        
        # Tarjeta de métrica
        st.metric(label="Resultado en Fahrenheit", value=f"{fahrenheit_pred:.2f} °F")
        
        st.success(f"¡El modelo estima que **{celsius_input} °C** son **{fahrenheit_pred:.2f} °F**!")
        
        # Botón para registrar la predicción en el DWH
        if st.button("📥 Registrar esta predicción en el Data Warehouse"):
            save_prediction(celsius_input, fahrenheit_pred)
            st.info("Predicción guardada exitosamente en la tabla de logs.")

    with col2:
        st.subheader("📈 Línea de Regresión")
        # Gráfico interactivo con Plotly
        fig = px.scatter(df, x="Celsius", y="Fahrenheit", trendline="ols", 
                         title="Relación Lineal Aprendida",
                         labels={"Celsius": "Grados Celsius (°C)", "Fahrenheit": "Grados Fahrenheit (°F)"},
                         template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

with tab_analysis:
    st.subheader("🔬 Profundización en los Datos del Warehouse")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("**Distribución de Temperaturas (Celsius)**")
        fig_dist = px.histogram(df, x="Celsius", nbins=10, 
                                color_discrete_sequence=['#ff4b4b'],
                                marginal="box")
        st.plotly_chart(fig_dist, use_container_width=True)
        
    with col_b:
        st.markdown("**Análisis de Residuos (Errores)**")
        # Calculamos los residuos (predicho - real)
        y_pred = modelo.predict(X)
        residuos = y - y_pred
        fig_res = px.scatter(x=df['Celsius'], y=residuos, 
                             labels={'x': 'Celsius', 'y': 'Error (Residuo)'},
                             title="Distribución del Error")
        fig_res.add_hline(y=0, line_dash="dash", line_color="white")
        st.plotly_chart(fig_res, use_container_width=True)

    with st.expander("📊 Ver Datos Crudos del DWH (Cleaned)"):
        st.dataframe(df, use_container_width=True)

with tab_history:
    st.subheader("🕵️ Auditoría del Data Warehouse")
    st.markdown("Este historial se recupera directamente de la tabla de logs del DWH.")
    engine = create_engine('sqlite:///data werehouse/data_warehouse.db')
    try:
        history_df = pd.read_sql('SELECT * FROM predictions_log ORDER BY timestamp DESC LIMIT 15', con=engine)
        if not history_df.empty:
            st.dataframe(history_df, use_container_width=True)
        else:
            st.info("Aún no hay predicciones registradas en el historial.")
    except Exception as e:
        st.error(f"Error al cargar el historial: {e}")
