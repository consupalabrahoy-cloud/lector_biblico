import streamlit as st
import json
import os
from github import Github, GithubException
from unidecode import unidecode # Importar la nueva biblioteca

# --- Configuración de GitHub ---
GITHUB_TOKEN = st.secrets.get("github_token", os.environ.get("GITHUB_TOKEN"))
REPO_NAME = "consupalabrahoy-cloud/lector_biblico" 
FILE_PATH = "vocabulario_nt.json"
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
    except GithubException as e:
        st.warning(f"Archivo '{FILE_PATH}' no encontrado en el repositorio. Creando una nueva lista vacía.")
        return []

def save_data_to_github(data):
    """Guarda los datos en el archivo JSON en el repositorio de GitHub."""
    repo = get_github_repo()
    try:
        # Obtener el contenido del archivo para su SHA
        contents = repo.get_contents(FILE_PATH, ref=BRANCH)
        commit_message = f"Actualizar vocabulario: {st.session_state.input_palabra}"
        
        # Codificar los datos JSON para guardarlos
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        repo.update_file(contents.path, commit_message, json_data, contents.sha, branch=BRANCH)
        
        # Limpiar el caché para forzar una recarga en la siguiente operación
        st.cache_data.clear()
        st.success(f"¡La palabra '{st.session_state.input_palabra}' ha sido guardada con éxito en GitHub!")
        return True
    except GithubException as e:
        st.error(f"Ocurrió un error al guardar los datos en GitHub: {e}")
        return False

def save_callback():
    """Callback para el botón de guardar."""
    if not st.session_state.input_palabra:
        st.error("El campo 'Palabra' no puede estar vacío.")
        return

    # Cargar los datos desde el caché
    vocab_data = load_data_from_github()
    palabra_nueva = st.session_state.input_palabra

    new_entry = {
        "palabra": palabra_nueva,
        "transliteracion": st.session_state.input_transliteracion,
        "traduccion_literal": st.session_state.input_traduccion_literal,
        "analisis_gramatical": st.session_state.input_analisis_gramatical
    }

    # Búsqueda y actualización más eficiente
    word_updated = False
    for i, entry in enumerate(vocab_data):
        if entry.get('palabra') == palabra_nueva:
            vocab_data[i] = new_entry
            word_updated = True
            break
    
    if not word_updated:
        vocab_data.append(new_entry)

    save_data_to_github(vocab_data)
    clear_fields_callback()

def search_callback():
    """Callback para el botón de búsqueda."""
    if not st.session_state.search_term:
        st.warning("El campo de búsqueda no puede estar vacío.")
        return

    # Cargar los datos desde el caché
    vocab_data = load_data_from_github()
    
    # Normalizar el término de búsqueda a minúsculas y sin diacríticos
    search_term_normalized = unidecode(st.session_state.search_term).lower()
    
    # Buscar la palabra en los datos, también normalizando
    word_data = next((item for item in vocab_data if unidecode(item.get("palabra", "")).lower() == search_term_normalized), None)
    
    if word_data:
        st.session_state.input_palabra = word_data.get('palabra', '')
        st.session_state.input_transliteracion = word_data.get('transliteracion', '')
        st.session_state.input_traduccion_literal = word_data.get('traduccion_literal', '')
        st.session_state.input_analisis_gramatical = word_data.get('analisis_gramatical', '')
        st.success(f"Palabra '{st.session_state.search_term}' encontrada. Puedes editar los campos y guardar los cambios.")
    else:
        st.warning(f"No hay datos para la palabra '{st.session_state.search_term}'.")
        clear_fields_callback()

def clear_fields_callback():
    """Callback para el botón de limpiar campos."""
    st.session_state.input_palabra = ''
    st.session_state.input_transliteracion = ''
    st.session_state.input_traduccion_literal = ''
    st.session_state.input_analisis_gramatical = ''
    st.session_state.search_term = ''
    st.success("Campos limpiados.")

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
st.text_input("Ingresa la palabra a buscar:", key="search_term", on_change=search_callback)

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
```
eof

### Siguientes pasos

1.  **Actualiza tu `requirements.txt`**: Agrega la línea `Unidecode` al archivo.
    ```
    streamlit
    requests
    PyGithub
    Unidecode
    
