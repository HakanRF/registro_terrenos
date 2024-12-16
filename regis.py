import streamlit as st
import pandas as pd
import datetime
import folium
from streamlit_folium import st_folium

# Configurar la página de Streamlit
st.set_page_config(page_title="Registro de Cultivos", layout="wide")

# Título de la aplicación
st.title("Sistema de Registro y Proceso de Cultivos")

# Inicializar o cargar el almacenamiento de la sesión
if 'datos_registro' not in st.session_state:
    st.session_state['datos_registro'] = {
        'Terreno': [],
        'Ubicación': [],
        'Metraje (hectáreas)': [],
        'Forma': [],
        'Cultivo': [],
        'Estado del Cultivo': [],
        'Fecha de Actividad': [],
        'Actividad Realizada': []
    }

datos_registro = st.session_state['datos_registro']

# Sección de registro de terreno
st.header("Registro de Terreno")

# Entradas para el registro del terreno
terreno = st.text_input("Nombre del Terreno")
ubicacion = st.text_input("Ubicación del Terreno (latitud, longitud)")
metraje = st.number_input("Metraje (en hectáreas)", min_value=0.0, step=0.1)
forma = st.selectbox("Forma del Terreno", ["Rectangular", "Cuadrado", "Irregular"])

if st.button("Registrar Terreno"):
    if terreno and ubicacion and metraje > 0:
        datos_registro['Terreno'].append(terreno)
        datos_registro['Ubicación'].append(ubicacion)
        datos_registro['Metraje (hectáreas)'].append(metraje)
        datos_registro['Forma'].append(forma)
        st.success(f"Terreno '{terreno}' registrado exitosamente.")
    else:
        st.error("Por favor, complete todos los campos obligatorios del terreno.")

# Sección de visualización del mapa
st.header("Visualización del Mapa de Terrenos")

# Crear un mapa de Folium
m = folium.Map(location=[-12.0464, -77.0428], zoom_start=12)

# Agregar marcadores para cada terreno registrado
for i, ubicacion in enumerate(datos_registro['Ubicación']):
    try:
        lat, lon = map(float, ubicacion.split(','))
        folium.Marker(location=[lat, lon], popup=f"Terreno: {datos_registro['Terreno'][i]}").add_to(m)
    except ValueError:
        pass

st_folium(m, width=700, height=500)

# Sección de registro de cultivo
st.header("Registro de Cultivo")

# Seleccionar el terreno donde se siembra el cultivo
terreno_seleccionado = st.selectbox("Seleccione el Terreno", options=datos_registro['Terreno'])
cultivo = st.text_input("Cultivo Sembrado")
estado_cultivo = st.selectbox("Estado del Cultivo", ["Bueno", "Regular", "Malo"])

if st.button("Registrar Cultivo"):
    if terreno_seleccionado and cultivo:
        datos_registro['Cultivo'].append(cultivo)
        datos_registro['Estado del Cultivo'].append(estado_cultivo)
        st.success(f"Cultivo '{cultivo}' registrado exitosamente en el terreno '{terreno_seleccionado}'.")
    else:
        st.error("Por favor, complete todos los campos obligatorios del cultivo.")

# Sección de registro de actividades diarias
st.header("Registro de Actividades Diarias")

# Seleccionar el terreno donde se realizará la actividad
terreno_actividad = st.selectbox("Seleccione el Terreno para la Actividad", options=datos_registro['Terreno'])
fecha_actividad = st.date_input("Fecha de la Actividad", min_value=datetime.date.today())
actividad_realizada = st.text_area("Descripción de la Actividad Realizada")

if st.button("Registrar Actividad"):
    if terreno_actividad and actividad_realizada:
        datos_registro['Fecha de Actividad'].append(fecha_actividad)
        datos_registro['Actividad Realizada'].append(actividad_realizada)
        st.success(f"Actividad registrada exitosamente para el terreno '{terreno_actividad}' en la fecha {fecha_actividad}.")
    else:
        st.error("Por favor, complete todos los campos obligatorios de la actividad.")

# Visualización de los registros actuales
st.header("Visualización de Registros")

if st.button("Mostrar Registros"):
    df = pd.DataFrame(datos_registro)
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No hay registros disponibles para mostrar.")

# Guardar los registros en un archivo CSV
if st.button("Exportar a CSV"):
    df = pd.DataFrame(datos_registro)
    if not df.empty:
        df.to_csv("registro_cultivos.csv", index=False)
        st.success("Los registros se han exportado exitosamente a 'registro_cultivos.csv'.")
    else:
        st.error("No hay registros para exportar.")
