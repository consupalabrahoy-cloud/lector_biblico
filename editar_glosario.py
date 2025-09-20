import streamlit as st
import json
import os

# --- Configuración de la aplicación ---
st.set_page_config(page_title="Editor de Glosario Griego")

# --- Rutas de los archivos ---
JSON_FILE = 'glosario.json'

# --- Funciones de manejo de datos ---
def cargar_glosario():
    """Carga los datos del glosario desde el archivo JSON."""
    if os.path.exists(JSON_FILE) and os.path.getsize(JSON_FILE) > 0:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_glosario(glosario_data):
    """Guarda la lista de diccionarios en el archivo JSON."""
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(glosario_data, f, ensure_ascii=False, indent=4)

# --- Lógica de la aplicación Streamlit ---
# Cargar datos una sola vez usando el estado de sesión
if 'glosario' not in st.session_state:
    st.session_state.glosario = cargar_glosario()
    st.session_state.palabra_encontrada = None
    st.session_state.indice_encontrado = -1

st.title("Editor de Glosario Griego")
st.write("Busca una palabra para ver y editar su información.")

# Campo de búsqueda
palabra_a_buscar = st.text_input("Ingresa la palabra griega:")

# Botón de búsqueda
if st.button("Buscar"):
    indice_encontrado = -1
    for i, entry in enumerate(st.session_state.glosario):
        if entry['palabra'].lower() == palabra_a_buscar.lower():
            indice_encontrado = i
            break

    if indice_encontrado != -1:
        st.session_state.palabra_encontrada = st.session_state.glosario[indice_encontrado]
        st.session_state.indice_encontrado = indice_encontrado
        st.success("¡Palabra encontrada! Puedes editar los campos a continuación.")
    else:
        st.session_state.palabra_encontrada = None
        st.session_state.indice_encontrado = -1
        st.warning(f"❌ La palabra '{palabra_a_buscar}' no fue encontrada.")

# --- Formulario de edición (solo si se encontró una palabra) ---
if st.session_state.palabra_encontrada:
    entry = st.session_state.palabra_encontrada
    
    st.subheader(f"Editando: {entry['palabra']}")
    
    with st.form("form_edicion"):
        # Campos de texto para edición
        transliteracion = st.text_input("Transliteración:", value=entry['transliteracion'])
        traduccion = st.text_input("Traducción Literal:", value=entry['traduccion_literal'])
        analisis = st.text_area("Análisis Gramatical:", value=entry['analisis_gramatical'], height=300)
        
        # Botón para guardar los cambios
        submitted = st.form_submit_button("Guardar Cambios")
        
        if submitted:
            # Actualizar el diccionario en la lista de datos
            st.session_state.glosario[st.session_state.indice_encontrado]['transliteracion'] = transliteracion
            st.session_state.glosario[st.session_state.indice_encontrado]['traduccion_literal'] = traduccion
            st.session_state.glosario[st.session_state.indice_encontrado]['analisis_gramatical'] = analisis
            
            # Guardar los cambios en el archivo JSON
            guardar_glosario(st.session_state.glosario)
            st.success("✅ ¡Cambios guardados exitosamente en el archivo JSON!")