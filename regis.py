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

# Crear pestañas con Streamlit
menu = st.tabs(["Registro", "Actualización", "Dashboard General"])

# -----------------------
# Pestaña 1: Registro
# -----------------------
with menu[0]:
    st.header("Registro de Terrenos y Cultivos")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Registro de Terreno")
        terreno = st.text_input("Nombre del Terreno")
        ubicacion = st.text_input("Ubicación del Terreno")
        metraje = st.number_input("Metraje (en hectáreas)", min_value=0.0, step=0.1)
    
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
    
    if st.button("Registrar Terreno"):
        if terreno and ubicacion and metraje > 0:
            datos_registro['Terreno'].append(terreno)
            datos_registro['Ubicación'].append(ubicacion)
            datos_registro['Metraje (hectáreas)'].append(metraje)
            datos_registro['Forma'].append(forma.image_data if forma.image_data is not None else None)
            datos_registro['Cultivos'].append([])
            st.success(f"Terreno '{terreno}' registrado exitosamente.")
        else:
            st.error("Por favor, complete todos los campos obligatorios del terreno.")

    st.subheader("Registro de Cultivo")
    terreno_seleccionado = st.selectbox("Seleccione el Terreno", options=datos_registro['Terreno'], key="selectbox_terreno_cultivo")
    if terreno_seleccionado:
        cultivo = st.text_input("Cultivo Sembrado")
        if st.button("Registrar Cultivo"):
            if cultivo:
                index = datos_registro['Terreno'].index(terreno_seleccionado)
                datos_registro['Cultivos'][index].append({
                    'Nombre del Cultivo': cultivo,
                    'Etapas': []
                })
                st.success(f"Cultivo '{cultivo}' registrado exitosamente en el terreno '{terreno_seleccionado}'.")
            else:
                st.error("Por favor, complete todos los campos obligatorios del cultivo.")

# -----------------------
# Pestaña 2: Actualización
# -----------------------
with menu[1]:
    st.header("Actualizar Etapas de Manejo")
    terreno_seleccionado = st.selectbox("Seleccione el Terreno", options=datos_registro['Terreno'], key="selectbox_actualizar_terreno")
    if terreno_seleccionado:
        index_terreno = datos_registro['Terreno'].index(terreno_seleccionado)
        cultivos_terreno = [c['Nombre del Cultivo'] for c in datos_registro['Cultivos'][index_terreno]]
        cultivo_seleccionado = st.selectbox("Seleccione el Cultivo", options=cultivos_terreno, key="selectbox_actualizar_cultivo")
        
        if cultivo_seleccionado:
            nombre_etapa = st.text_input("Nombre de la Etapa")
            fecha_inicio = st.date_input("Fecha de Inicio")
            fecha_fin = st.date_input("Fecha de Fin")
            actividad = st.text_area("Actividad Realizada")

            if st.button("Actualizar Etapa"):
                for cultivo in datos_registro['Cultivos'][index_terreno]:
                    if cultivo['Nombre del Cultivo'] == cultivo_seleccionado:
                        cultivo['Etapas'].append({
                            'Etapa': nombre_etapa,
                            'Fecha Inicio': fecha_inicio,
                            'Fecha Fin': fecha_fin,
                            'Actividad': actividad
                        })
                        st.success(f"Etapa '{nombre_etapa}' con actividad actualizada exitosamente para el cultivo '{cultivo_seleccionado}'.")

# -----------------------
# Pestaña 3: Dashboard General
# -----------------------
with menu[2]:
    st.header("Dashboard General del Registro")
    if not datos_registro['Terreno']:
        st.info("No hay registros disponibles.")
    else:
        terreno_dashboard = st.selectbox("Seleccione un Terreno para visualizar sus etapas de manejo", options=datos_registro['Terreno'], key="selectbox_dashboard")
        index_terreno = datos_registro['Terreno'].index(terreno_dashboard)
        registros_completos = []

        for cultivo in datos_registro['Cultivos'][index_terreno]:
            for etapa in cultivo['Etapas']:
                registros_completos.append({
                    'Terreno': terreno_dashboard,
                    'Cultivo': cultivo['Nombre del Cultivo'],
                    'Etapa': etapa['Etapa'],
                    'Fecha Inicio': etapa['Fecha Inicio'],
                    'Fecha Fin': etapa['Fecha Fin'],
                    'Actividad': etapa['Actividad']
                })

        if registros_completos:
            df_dashboard = pd.DataFrame(registros_completos)
            st.dataframe(df_dashboard)
        else:
            st.info("No hay etapas de manejo registradas para este terreno.")

