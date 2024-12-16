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
menu = st.tabs(["Registro de Terrenos", "Registro de Cultivos", "Registro de Etapas", "Actualizar Terreno", "Dashboard"])

# -----------------------
# Pestaña 1: Registro de Terrenos
# -----------------------
with menu[0]:
    st.header("Registro de Terreno")
    col1, col2 = st.columns(2)
    
    with col1:
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

# -----------------------
# Pestaña 2: Registro de Cultivos
# -----------------------
with menu[1]:
    st.header("Registro de Cultivo")

    terreno_seleccionado = st.selectbox("Seleccione el Terreno", options=datos_registro['Terreno'], key="selectbox_terreno_cultivo")
    if terreno_seleccionado:
        cultivo = st.text_input("Cultivo Sembrado")
        estado_cultivo = st.selectbox("Estado del Cultivo", ["Preparación", "Siembra", "Crecimiento", "Fertilización", "Cosecha"], key="selectbox_estado_cultivo")

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

# -----------------------
# Pestaña 3: Registro de Etapas
# -----------------------
with menu[2]:
    st.header("Registro de Etapas de Manejo del Cultivo")

    terreno_etapa = st.selectbox("Seleccione el Terreno", options=datos_registro['Terreno'], key="selectbox_terreno_etapa")
    if terreno_etapa:
        index_terreno = datos_registro['Terreno'].index(terreno_etapa)
        cultivos_terreno = [c['Nombre del Cultivo'] for c in datos_registro['Cultivos'][index_terreno]]
        cultivo_seleccionado = st.selectbox("Seleccione el Cultivo", options=cultivos_terreno, key="selectbox_cultivo_etapa")
        
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
                        st.success(f"Etapa '{nombre_etapa}' registrada exitosamente para el cultivo '{cultivo_seleccionado}'.")

# -----------------------
# Pestaña 4: Actualizar Terrenos
# -----------------------
with menu[3]:
    st.header("Actualizar Datos del Terreno")
    terreno_seleccionado = st.selectbox("Seleccione el Terreno a Actualizar", options=datos_registro['Terreno'], key="selectbox_actualizar_terreno")
    
    if terreno_seleccionado:
        index = datos_registro['Terreno'].index(terreno_seleccionado)
        nueva_ubicacion = st.text_input("Nueva Ubicación", value=datos_registro['Ubicación'][index])
        nuevo_metraje = st.number_input("Nuevo Metraje (en hectáreas)", value=datos_registro['Metraje (hectáreas)'][index], min_value=0.0, step=0.1)
        st.text("Actualiza la forma del terreno")
        nueva_forma = canvas.st_canvas(
            fill_color="#ffffff",
            stroke_width=2,
            stroke_color="#000000",
            background_color="#eeeeee",
            width=300,
            height=300,
            drawing_mode="freedraw",
            key="canvas_actualizar_forma"
        )

        if st.button("Actualizar Terreno"):
            datos_registro['Ubicación'][index] = nueva_ubicacion
            datos_registro['Metraje (hectáreas)'][index] = nuevo_metraje
            if nueva_forma.image_data is not None:
                datos_registro['Forma'][index] = nueva_forma.image_data
            st.success(f"Terreno '{terreno_seleccionado}' actualizado exitosamente.")

# -----------------------
# Pestaña 5: Dashboard
# -----------------------
with menu[4]:
    st.header("Dashboard de Registros")
    
    registros_completos = []
    for i, terreno in enumerate(datos_registro['Terreno']):
        for cultivo in datos_registro['Cultivos'][i]:
            for etapa in cultivo['Etapas']:
                registros_completos.append({
                    'Terreno': terreno,
                    'Ubicación': datos_registro['Ubicación'][i],
                    'Cultivo': cultivo['Nombre del Cultivo'],
                    'Etapa': etapa['Etapa'],
                    'Fecha Inicio': etapa['Fecha Inicio'],
                    'Fecha Fin': etapa['Fecha Fin']
                })

    if registros_completos:
        df_dashboard = pd.DataFrame(registros_completos)
        st.dataframe(df_dashboard)
        
        st.subheader("Resumen General")
        st.write(f"**Total de Terrenos:** {len(datos_registro['Terreno'])}")
        st.write(f"**Total de Cultivos:** {sum(len(c) for c in datos_registro['Cultivos'])}")
        st.write(f"**Total de Etapas Registradas:** {sum(len(c['Etapas']) for cultivos in datos_registro['Cultivos'] for c in cultivos)}")
    else:
        st.info("No hay registros disponibles para visualizar en el dashboard.")
