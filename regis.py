import streamlit as st
import pandas as pd
import datetime
import streamlit_drawable_canvas as canvas

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
        'Cultivos': []  # Almacena los cultivos para cada terreno
    }

datos_registro = st.session_state['datos_registro']

# Disposición de columnas
col1, col2 = st.columns(2)

# Sección de registro de terreno en la primera columna
with col1:
    st.header("Registro de Terreno")
    
    terreno = st.text_input("Nombre del Terreno")
    ubicacion = st.text_input("Ubicación del Terreno")
    metraje = st.number_input("Metraje (en hectáreas)", min_value=0.0, step=0.1)
    st.text("Dibuja la forma del terreno")
    forma = canvas.st_canvas(
        fill_color="#ffffff",  # Color de fondo
        stroke_width=2,
        stroke_color="#000000",
        background_color="#eeeeee",
        width=300,
        height=300,
        drawing_mode="freedraw",
        key="canvas_forma"
    )

    if st.button("Registrar Terreno"):
        if terreno and ubicacion and metraje > 0:
            datos_registro['Terreno'].append(terreno)
            datos_registro['Ubicación'].append(ubicacion)
            datos_registro['Metraje (hectáreas)'].append(metraje)
            datos_registro['Forma'].append(forma.image_data if forma.image_data is not None else None)
            datos_registro['Cultivos'].append([])  # Inicializar la lista de cultivos para este terreno
            st.success(f"Terreno '{terreno}' registrado exitosamente.")
        else:
            st.error("Por favor, complete todos los campos obligatorios del terreno.")

# Sección de visualización de terrenos en la segunda columna
with col2:
    st.header("Lista de Terrenos Registrados")
    
    if datos_registro['Terreno']:
        df_terrenos = pd.DataFrame({
            'Terreno': datos_registro['Terreno'],
            'Ubicación': datos_registro['Ubicación'],
            'Metraje (hectáreas)': datos_registro['Metraje (hectáreas)']
        })
        st.dataframe(df_terrenos)
    else:
        st.info("No hay terrenos registrados actualmente.")

# Sección de registro de cultivo
st.header("Registro de Cultivo")

terreno_seleccionado = st.selectbox("Seleccione el Terreno", options=datos_registro['Terreno'])
if terreno_seleccionado:
    cultivo = st.text_input("Cultivo Sembrado")
    estado_cultivo = st.selectbox("Estado del Cultivo", ["Preparación", "Siembra", "Crecimiento", "Fertilización", "Cosecha"])

    if st.button("Registrar Cultivo"):
        if cultivo:
            index = datos_registro['Terreno'].index(terreno_seleccionado)
            datos_registro['Cultivos'][index].append({
                'Nombre del Cultivo': cultivo,
                'Estado': estado_cultivo,
                'Etapas': []
            })
            st.success(f"Cultivo '{cultivo}' registrado exitosamente en el terreno '{terreno_seleccionado}'.")
        else:
            st.error("Por favor, complete todos los campos obligatorios del cultivo.")

# Sección de registro de etapas
st.header("Registro de Etapas de Manejo del Cultivo")

terreno_etapa = st.selectbox("Seleccione el Terreno", options=datos_registro['Terreno'])
if terreno_etapa:
    index_terreno = datos_registro['Terreno'].index(terreno_etapa)
    cultivos_terreno = [c['Nombre del Cultivo'] for c in datos_registro['Cultivos'][index_terreno]]
    cultivo_seleccionado = st.selectbox("Seleccione el Cultivo", options=cultivos_terreno)
    
    if cultivo_seleccionado:
        nombre_etapa = st.text_input("Nombre de la Etapa")
        fecha_inicio = st.date_input("Fecha de Inicio")
        fecha_fin = st.date_input("Fecha de Fin")
        
        if st.button("Registrar Etapa"):
            for cultivo in datos_registro['Cultivos'][index_terreno]:
                if cultivo['Nombre del Cultivo'] == cultivo_seleccionado:
                    cultivo['Etapas'].append({
                        'Etapa': nombre_etapa,
                        'Fecha Inicio': fecha_inicio,
                        'Fecha Fin': fecha_fin
                    })
                    st.success(f"Etapa '{nombre_etapa}' registrada exitosamente para el cultivo '{cultivo_seleccionado}' en el terreno '{terreno_etapa}'.")

# Sección de visualización de registros actuales
st.header("Visualización de Registros de Cultivos y Etapas")

if st.button("Mostrar Registros"):
    registros = []
    for i, terreno in enumerate(datos_registro['Terreno']):
        for cultivo in datos_registro['Cultivos'][i]:
            for etapa in cultivo['Etapas']:
                registros.append({
                    'Terreno': terreno,
                    'Cultivo': cultivo['Nombre del Cultivo'],
                    'Etapa': etapa['Etapa'],
                    'Fecha Inicio': etapa['Fecha Inicio'],
                    'Fecha Fin': etapa['Fecha Fin']
                })
    
    if registros:
        df = pd.DataFrame(registros)
        st.dataframe(df)
    else:
        st.info("No hay registros disponibles para mostrar.")
