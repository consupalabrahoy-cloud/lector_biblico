import streamlit as st
import sqlite3

# --- Configuración de la base de datos ---
DB_FILE = 'vocabulario.db'

def setup_database():
    """Crea la base de datos y la tabla 'vocabulario' si no existen."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS vocabulario (
                palabra TEXT PRIMARY KEY,
                transliteracion TEXT,
                traduccion_literal TEXT,
                analisis_gramatical TEXT
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error de base de datos: {e}")
    finally:
        if conn:
            conn.close()

# --- Funciones de base de datos ---
def save_data(palabra, transliteracion, traduccion_literal, analisis_gramatical):
    """
    Guarda o actualiza los datos en la base de datos SQLite.
    Si la palabra ya existe, la actualiza. Si no, la inserta.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        c.execute("""
            INSERT OR REPLACE INTO vocabulario (palabra, transliteracion, traduccion_literal, analisis_gramatical)
            VALUES (?, ?, ?, ?)
        """, (palabra, transliteracion, traduccion_literal, analisis_gramatical))
        
        conn.commit()
        st.success(f"¡La palabra '{palabra}' ha sido guardada o actualizada con éxito!")
    except sqlite3.Error as e:
        st.error(f"Ocurrió un error al guardar los datos: {e}")
    finally:
        if conn:
            conn.close()

def find_word_in_db(palabra):
    """Busca una palabra en la base de datos y devuelve sus datos si la encuentra."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM vocabulario WHERE palabra = ?", (palabra,))
        row = c.fetchone()
        
        if row:
            # Devuelve un diccionario con los datos encontrados
            return {
                "palabra": row[0],
                "transliteracion": row[1],
                "traduccion_literal": row[2],
                "analisis_gramatical": row[3]
            }
        return None
    except sqlite3.Error as e:
        st.error(f"Ocurrió un error al buscar la palabra: {e}")
        return None
    finally:
        if conn:
            conn.close()

def search_callback():
    """Callback para el botón de búsqueda."""
    if st.session_state.search_term:
        word_data = find_word_in_db(st.session_state.search_term)
        if word_data:
            # Rellenar los campos de la interfaz
            st.session_state.input_palabra = word_data.get('palabra')
            st.session_state.input_transliteracion = word_data.get('transliteracion')
            st.session_state.input_traduccion_literal = word_data.get('traduccion_literal')
            st.session_state.input_analisis_gramatical = word_data.get('analisis_gramatical')
            st.success(f"Palabra '{st.session_state.search_term}' encontrada. Puedes editar los campos y guardar los cambios.")
        else:
            st.warning(f"No se encontró la palabra '{st.session_state.search_term}'.")
            
def save_callback():
    """Callback para el botón de guardar."""
    if st.session_state.input_palabra:
        save_data(
            st.session_state.input_palabra,
            st.session_state.input_transliteracion,
            st.session_state.input_traduccion_literal,
            st.session_state.input_analisis_gramatical
        )
    else:
        st.error("El campo 'Palabra' no puede estar vacío.")

def clear_fields_callback():
    """Callback para el botón de limpiar campos."""
    st.session_state.input_palabra = ''
    st.session_state.input_transliteracion = ''
    st.session_state.input_traduccion_literal = ''
    st.session_state.input_analisis_gramatical = ''
    st.session_state.search_term = ''

# --- Interfaz de Streamlit ---
st.title("Herramienta de Curación de Datos 📖")
st.write("Ingresa una nueva palabra o busca una existente para editar.")

# Inicializar la base de datos
setup_database()

# Inicializar el estado de la sesión si no existe
if 'input_palabra' not in st.session_state: st.session_state.input_palabra = ''
if 'input_transliteracion' not in st.session_state: st.session_state.input_transliteracion = ''
if 'input_traduccion_literal' not in st.session_state: st.session_state.input_traduccion_literal = ''
if 'input_analisis_gramatical' not in st.session_state: st.session_state.input_analisis_gramatical = ''
if 'search_term' not in st.session_state: st.session_state.search_term = ''

# Sección de búsqueda
st.subheader("Buscar Palabra")
st.text_input("Ingresa la palabra griega a buscar:", key="search_term", on_change=search_callback)

# Sección de entrada de datos
st.subheader("Ingresar o Editar Datos")
st.text_input("Palabra Griega:", key="input_palabra")
st.text_input("Transliteración:", key="input_transliteracion")
st.text_input("Traducción Literal:", key="input_traduccion_literal")
st.text_area("Análisis Morfológico:", key="input_analisis_gramatical", height=150)

# Botones de acción
col1, col2 = st.columns(2)
with col1:
    st.button("Guardar Palabra", on_click=save_callback)
with col2:
    st.button("Limpiar Campos", on_click=clear_fields_callback)
