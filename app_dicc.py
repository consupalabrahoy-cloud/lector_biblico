import streamlit as st
import json
import requests
from github import Github, GithubException
import os

# --- Configuración de GitHub ---
# Usamos st.secrets para obtener el token de manera segura
# El nombre de la clave debe coincidir con el nombre que usarás en Streamlit Cloud
GITHUB_TOKEN = st.secrets.get("github_token", os.environ.get("GITHUB_TOKEN"))
REPO_NAME = "tu_usuario/tu_repositorio" # Reemplaza con tu usuario y nombre de repositorio
FILE_PATH = "vocabulario_nt.json"

def get_github_repo():
    """Obtiene una instancia del repositorio de GitHub."""
    if not GITHUB_TOKEN:
        st.error("No se encontró el token de GitHub. Configúralo en Streamlit Secrets.")
        return None
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        return repo
    except GithubException as e:
        st.error(f"Error al conectar con el repositorio: {e}")
        return None

def load_data_from_github():
    """Carga los datos del archivo JSON desde el repositorio de GitHub."""
    repo = get_github_repo()
    if not repo:
        return []
    try:
        contents = repo.get_contents(FILE_PATH, ref="main") # O "master", según tu rama principal
        data = json.loads(contents.decoded_content)
        return data
    except GithubException as e:
        st.warning(f"El archivo '{FILE_PATH}' no se encontró en el repositorio. Creando una nueva lista vacía.")
        return []

def save_data_to_github(data):
    """Guarda los datos en el archivo JSON en el repositorio de GitHub."""
    repo = get_github_repo()
    if not repo:
        return False
    try:
        contents = repo.get_contents(FILE_PATH, ref="main")
        commit_message = f"Actualizar vocabulario: {st.session_state.input_palabra}"
        repo.update_file(contents.path, commit_message, json.dumps(data, indent=4, ensure_ascii=False), contents.sha, branch="main")
        return True
    except GithubException as e:
        st.error(f"Ocurrió un error al guardar los datos en GitHub: {e}")
        return False

def find_word_in_data(data, palabra):
    """Busca una palabra en la lista de datos."""
    for entry in data:
        if entry.get('palabra') == palabra:
            return entry
    return None

def save_callback():
    """Callback para el botón de guardar."""
    if not st.session_state.input_palabra:
        st.error("El campo 'Palabra' no puede estar vacío.")
        return

    palabra_nueva = st.session_state.input_palabra

    # Cargar los datos actuales de GitHub
    vocab_data = load_data_from_github()

    # Crear el nuevo diccionario de datos
    new_entry = {
        "palabra": palabra_nueva,
        "transliteracion": st.session_state.input_transliteracion,
        "traduccion_literal": st.session_state.input_traduccion_literal,
        "analisis_gramatical": st.session_state.input_analisis_gramatical
    }

    # Verificar si la palabra ya existe
    word_found = False
    for i, entry in enumerate(vocab_data):
        if entry.get('palabra') == palabra_nueva:
            # Actualizar la entrada existente
            vocab_data[i] = new_entry
            word_found = True
            break

    # Si la palabra no existe, la añadimos
    if not word_found:
        vocab_data.append(new_entry)

    # Guardar los datos actualizados en GitHub
    if save_data_to_github(vocab_data):
        st.success(f"¡La palabra '{palabra_nueva}' ha sido guardada con éxito en GitHub!")
    else:
        st.error("Error al guardar en GitHub.")

def search_callback():
    """Callback para el botón de búsqueda."""
    if st.session_state.search_term:
        vocab_data = load_data_from_github()
        word_data = find_word_in_data(vocab_data, st.session_state.search_term)
        if word_data:
            st.session_state.input_palabra = word_data.get('palabra', '')
            st.session_state.input_transliteracion = word_data.get('transliteracion', '')
            st.session_state.input_traduccion_literal = word_data.get('traduccion_literal', '')
            st.session_state.input_analisis_gramatical = word_data.get('analisis_gramatical', '')
            st.success(f"Palabra '{st.session_state.search_term}' encontrada. Puedes editar los campos y guardar los cambios.")
        else:
            st.warning(f"No se encontró la palabra '{st.session_state.search_term}'.")
            clear_fields_callback()

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

# Inicializar el estado de la sesión si no existe
if 'input_palabra' not in st.session_state: st.session_state.input_palabra = ''
if 'input_transliteracion' not in st.session_state: st.session_state.input_transliteracion = ''
if 'input_traduccion_literal' not in st.session_state: st.session_state.input_traduccion_literal = ''
if 'input_analisis_gramatical' not in st.session_state: st.session_state.input_analisis_gramatical = ''
if 'search_term' not in st.session_state: st.session_state.search_term = ''

# Sección de búsqueda
st.subheader("Buscar Palabra")
st.text_input("Ingresa la palabra a buscar:", key="search_term")

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

