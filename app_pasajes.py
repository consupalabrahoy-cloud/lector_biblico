import streamlit as st
import json
import os
from github import Github, GithubException
from unidecode import unidecode
import re

# --- Configuración de GitHub ---
GITHUB_TOKEN = st.secrets.get("github_token", os.environ.get("GITHUB_TOKEN"))
REPO_NAME = "consupalabrahoy-cloud/lector_biblico" # ¡Importante! Reemplaza con tu usuario y nombre de repositorio
FILE_PATH = "pasajes_biblicos.json"
BRANCH = "main"

# Función con caché para obtener el repositorio. Se ejecuta una sola vez.
@st.cache_resource(ttl=3600)
def get_github_repo():
    """Obtiene una instancia del repositorio de GitHub."""
    if not GITHUB_TOKEN:
        st.error("Error: No se encontró el token de GitHub. Asegúrate de configurarlo en Streamlit Secrets.")
        st.stop()
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        return repo
    except GithubException as e:
        st.error(f"Error al conectar con el repositorio: {e}. Revisa el nombre del repo y el token.")
        st.stop()

# Función con caché para cargar los datos. Se ejecuta una sola vez por sesión.
@st.cache_data(show_spinner="Cargando datos...")
def load_data_from_github():
    """Carga los datos del archivo JSON desde el repositorio de GitHub."""
    repo = get_github_repo()
    try:
        contents = repo.get_contents(FILE_PATH, ref=BRANCH)
        data = json.loads(contents.decoded_content)
        return data
    except GithubException:
        st.warning(f"Archivo '{FILE_PATH}' no se encontró en el repositorio. Creando una nueva lista vacía.")
        return []

def save_data_to_github(data):
    """Guarda los datos en el archivo JSON en el repositorio de GitHub."""
    repo = get_github_repo()
    try:
        # Codificar los datos JSON para guardarlos
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        
        # Obtener el contenido del archivo para su SHA si ya existe
        try:
            contents = repo.get_contents(FILE_PATH, ref=BRANCH)
            repo.update_file(contents.path, f"Actualizar pasaje: {st.session_state.referencia_biblica}", json_data, contents.sha, branch=BRANCH)
        except GithubException:
            # Si el archivo no existe, lo creamos
            repo.create_file(FILE_PATH, f"Crear archivo de pasajes", json_data, branch=BRANCH)
            
        st.cache_data.clear()
        st.success(f"¡El pasaje '{st.session_state.referencia_biblica}' ha sido guardado con éxito en GitHub!")
        return True
    except GithubException as e:
        st.error(f"Ocurrió un error al guardar los datos en GitHub: {e}")
        return False

def save_callback():
    """Callback para el botón de guardar."""
    if not st.session_state.referencia_biblica:
        st.error("El campo 'Referencia Bíblica' no puede estar vacío.")
        return

    # Cargar los datos desde el caché
    pasajes_data = load_data_from_github()
    
    new_entry = {
        "referencia": st.session_state.referencia_biblica,
        "texto_griego": st.session_state.texto_griego,
        "informacion": st.session_state.informacion
    }

    # Búsqueda y actualización más eficiente
    word_updated = False
    for i, entry in enumerate(pasajes_data):
        if entry.get('referencia') == st.session_state.referencia_biblica:
            pasajes_data[i] = new_entry
            word_updated = True
            break
    
    if not word_updated:
        pasajes_data.append(new_entry)

    save_data_to_github(pasajes_data)
    clear_fields_callback()

def search_callback():
    """Callback para el botón de búsqueda."""
    if not st.session_state.search_term:
        st.warning("El campo de búsqueda no puede estar vacío.")
        return

    # Cargar los datos desde el caché
    pasajes_data = load_data_from_github()
    
    # Normalizar el término de búsqueda
    search_term_normalized = unidecode(st.session_state.search_term).lower()
    search_term_normalized = re.sub(r'[^a-z0-9]', '', search_term_normalized)

    # Buscar la referencia en los datos, también normalizando
    found_data = None
    for item in pasajes_data:
        normalized_ref = unidecode(item.get("referencia", "")).lower()
        normalized_ref = re.sub(r'[^a-z0-9]', '', normalized_ref)
        if normalized_ref == search_term_normalized:
            found_data = item
            break
    
    if found_data:
        st.session_state.referencia_biblica = found_data.get('referencia', '')
        st.session_state.texto_griego = found_data.get('texto_griego', '')
        st.session_state.informacion = found_data.get('informacion', '')
        st.success(f"Pasaje '{st.session_state.search_term}' encontrado. Puedes editar los campos y guardar los cambios.")
    else:
        st.warning(f"No hay información para el pasaje '{st.session_state.search_term}'.")
        clear_fields_callback()

def clear_fields_callback():
    """Callback para el botón de limpiar campos."""
    st.session_state.referencia_biblica = ''
    st.session_state.texto_griego = ''
    st.session_state.informacion = ''
    st.session_state.search_term = ''
    st.success("Campos limpiados.")

# --- Interfaz de Streamlit ---
st.title("Herramienta de Curación de Pasajes Bíblicos 📖")
st.write("Ingresa una nueva referencia o busca una existente para editar.")

# Inicializar el estado de la sesión si no existe
if 'referencia_biblica' not in st.session_state: st.session_state.referencia_biblica = ''
if 'texto_griego' not in st.session_state: st.session_state.texto_griego = ''
if 'informacion' not in st.session_state: st.session_state.informacion = ''
if 'search_term' not in st.session_state: st.session_state.search_term = ''

# Sección de búsqueda
st.subheader("Buscar Pasaje")
st.text_input("Ingresa la referencia (ej. Mateo 1:1-2):", key="search_term", on_change=search_callback)

# Sección de entrada de datos
st.subheader("Ingresar o Editar Datos")
st.text_input("Referencia Bíblica:", key="referencia_biblica")
st.text_area("Texto Griego:", key="texto_griego", height=200)
st.text_area("Información adicional (en español y/o griego):", key="informacion", height=300)

# Botones de acción
col1, col2 = st.columns(2)
with col1:
    st.button("Guardar Pasaje", on_click=save_callback)
with col2:
    st.button("Limpiar Campos", on_click=clear_fields_callback)
