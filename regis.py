import streamlit as st
import pandas as pd
import datetime
import streamlit_drawable_canvas as canvas
import base64
from io import BytesIO
from PIL import Image

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
        'Cultivos': [],
        'Abono': [],
        'Fertilizante': []
    }

datos_registro = st.session_state['datos_registro']

# Función para convertir imagen a base64
def convertir_imagen_base64(image_data):
    if image_data is not None:
        img = Image.fromarray(image_data)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    return None

# -----------------------
# Pestaña 1: Registro
# -----------------------
menu = st.tabs(["Registro", "Actualización", "Dashboard General", "Exportar Datos"])

with menu[0]:
    st.header("Registro de Terreno y Cultivo")
    col1, col2 = st.columns(2)

    with col1:
        terreno = st.text_input("Nombre del Terreno")
        ubicacion = st.text_input("Ubicación del Terreno")
        metraje = st.number_input("Metraje (en hectáreas)", min_value=0.0, step=0.1)
        cultivo = st.text_input("Cultivo")
        abono = st.number_input("Sacos de Abono", min_value=0, step=1)
        fertilizante = st.number_input("Sacos de Fertilizante (Wuano)", min_value=0, step=1)

    with col2:
        st.text("Dibuja la forma del terreno")
        forma = canvas.st_canvas(
            fill_color="#ffffff",
            stroke_width=2,
            stroke_color="#000000",
            background_color="#eeeeee",
            width=300,
            height=300,
            drawing_mode="freedraw",
            key="canvas_forma_terreno"
        )

    if st.button("Registrar Terreno y Cultivo"):
        if terreno and ubicacion and metraje > 0 and cultivo:
            datos_registro['Terreno'].append(terreno)
            datos_registro['Ubicación'].append(ubicacion)
            datos_registro['Metraje (hectáreas)'].append(metraje)
            datos_registro['Forma'].append(convertir_imagen_base64(forma.image_data))
            datos_registro['Cultivos'].append([{'Nombre del Cultivo': cultivo, 'Etapas': []}])
            datos_registro['Abono'].append(abono)
            datos_registro['Fertilizante'].append(fertilizante)
            st.success(f"Terreno '{terreno}' con cultivo '{cultivo}' registrado exitosamente.")
        else:
            st.error("Por favor, complete todos los campos obligatorios del terreno y cultivo.")

# -----------------------
# Pestaña 2: Actualización
# -----------------------
with menu[1]:
    st.header("Actualizar Etapas de Manejo")
    if datos_registro['Terreno']:
        terreno_seleccionado = st.selectbox("Seleccione el Terreno", options=datos_registro['Terreno'])
        index_terreno = datos_registro['Terreno'].index(terreno_seleccionado)
        cultivos_terreno = [c['Nombre del Cultivo'] for c in datos_registro['Cultivos'][index_terreno]]

        cultivo_seleccionado = st.selectbox("Seleccione el Cultivo", options=cultivos_terreno)
        if cultivo_seleccionado:
            nombre_etapa = st.selectbox("Nombre de la Etapa", ["Preparación", "Siembra", "Crecimiento", "Fertilización", "Cosecha"])
            fecha_inicio = st.date_input("Fecha de Inicio")
            fecha_fin = st.date_input("Fecha de Fin")
            actividad = st.text_area("Actividad Realizada")

            if st.button("Actualizar Etapa"):
                for cultivo in datos_registro['Cultivos'][index_terreno]:
                    if cultivo['Nombre del Cultivo'] == cultivo_seleccionado:
                        cultivo['Etapas'].append({
                            'Etapa': nombre_etapa,
                            'Fecha Inicio': fecha_inicio.strftime('%Y-%m-%d'),
                            'Fecha Fin': fecha_fin.strftime('%Y-%m-%d'),
                            'Actividad': actividad
                        })
                        st.success(f"Etapa '{nombre_etapa}' con actividad '{actividad}' actualizada exitosamente.")
    else:
        st.info("No hay terrenos registrados aún. Registre un terreno primero.")

# -----------------------
# Pestaña 3: Dashboard General
# -----------------------
with menu[2]:
    st.header("Dashboard General del Registro")
    if datos_registro['Terreno']:
        terreno_dashboard = st.selectbox("Seleccione un Terreno", options=datos_registro['Terreno'])
        index_terreno = datos_registro['Terreno'].index(terreno_dashboard)
        registros = []

        for cultivo in datos_registro['Cultivos'][index_terreno]:
            for etapa in cultivo['Etapas']:
                registros.append({
                    'Terreno': terreno_dashboard,
                    'Cultivo': cultivo['Nombre del Cultivo'],
                    'Etapa': etapa['Etapa'],
                    'Fecha Inicio': etapa['Fecha Inicio'],
                    'Fecha Fin': etapa['Fecha Fin'],
                    'Actividad': etapa['Actividad']
                })

        if registros:
            df_dashboard = pd.DataFrame(registros)
            st.dataframe(df_dashboard)
            st.subheader("Información del Terreno")
            st.write(f"**Ubicación:** {datos_registro['Ubicación'][index_terreno]}")
            st.write(f"**Metraje (hectáreas):** {datos_registro['Metraje (hectáreas)'][index_terreno]}")
            st.write(f"**Sacos de Abono:** {datos_registro['Abono'][index_terreno]}")
            st.write(f"**Sacos de Fertilizante (Wuano):** {datos_registro['Fertilizante'][index_terreno]}")

            st.subheader("Visualización de la Forma del Terreno")
            forma = datos_registro['Forma'][index_terreno]
            if forma:
                st.image(Image.open(BytesIO(base64.b64decode(forma))), caption=f"Forma del Terreno: {terreno_dashboard}")
        else:
            st.info("No hay etapas registradas para este terreno.")
    else:
        st.info("No hay terrenos registrados aún. Registre un terreno primero.")
