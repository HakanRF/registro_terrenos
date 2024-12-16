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
# Pestaña 4: Exportar Datos
# -----------------------
with menu[3]:
    st.header("Exportar Datos a Excel")
    if st.button("Exportar a Excel"):
        registros = []
        for i, terreno in enumerate(datos_registro['Terreno']):
            registros.append({
                'Terreno': terreno,
                'Ubicación': datos_registro['Ubicación'][i],
                'Metraje (hectáreas)': datos_registro['Metraje (hectáreas)'][i],
                'Sacos de Abono': datos_registro['Abono'][i],
                'Sacos de Fertilizante (Wuano)': datos_registro['Fertilizante'][i],
                'Forma (Base64)': datos_registro['Forma'][i]
            })

        df = pd.DataFrame(registros)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Registro de Cultivos")
        st.success("Datos exportados correctamente.")

        # Descargar archivo
        output.seek(0)
        st.download_button(
            label="Descargar Excel",
            data=output,
            file_name="registro_cultivos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
