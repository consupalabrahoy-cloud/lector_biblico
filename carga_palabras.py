import google.generativeai as genai
import json
import csv
import os

# --- Configuración de la API ---
# Reemplaza 'TU_CLAVE_DE_API_AQUI' con tu clave real.
genai.configure(api_key='TU_CLAVE_DE_API_AQUI')
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Rutas de los archivos ---
CSV_FILE = 'palabras_pendientes.csv'
JSON_FILE = 'glosario.json'

def cargar_glosario_existente():
    """Carga los datos del glosario si el archivo JSON ya existe."""
    if os.path.exists(JSON_FILE) and os.path.getsize(JSON_FILE) > 0:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_glosario(glosario_data):
    """Guarda la lista de diccionarios en el archivo JSON."""
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(glosario_data, f, ensure_ascii=False, indent=4)

def obtener_palabras_pendientes():
    """Lee el CSV y devuelve las palabras con estado 'pendiente'."""
    palabras = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['estado'].lower() == 'pendiente':
                palabras.append(row['palabra'])
    return palabras

def actualizar_estado_palabra(palabra, nuevo_estado):
    """Actualiza el estado de una palabra en el CSV."""
    filas = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        filas = list(reader)

    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['palabra', 'estado'])
        writer.writeheader()
        for row in filas:
            if row['palabra'] == palabra:
                row['estado'] = nuevo_estado
            writer.writerow(row)

def pedir_analisis_a_gemini(palabra):
    """Crea el prompt y solicita el análisis a la API de Gemini."""
    prompt = f"""
    Proporciona el análisis gramatical y el significado de la palabra griega "{palabra}".

    El resultado debe ser un objeto JSON con la siguiente estructura y en español:
    {{
        "palabra": "la palabra griega original",
        "transliteracion": "la transliteración en caracteres latinos",
        "traduccion_literal": "la traducción simple y directa al español",
        "analisis_gramatical": "un análisis detallado que incluya:
                                - Clase de palabra (sustantivo, verbo, adjetivo, etc.)
                                - Raíz (si aplica)
                                - Tiempo, voz, modo, persona, número, caso, género, etc. (según aplique)
                                - Una explicación del significado y su uso en el Nuevo Testamento,
                                  similar al que ya te he proporcionado en ejemplos anteriores.
                                  Asegúrate de que este campo no contenga caracteres de escape como '`'.
                                  Asegúrate de que este campo tenga saltos de línea donde se necesite."
    }}
    """
    response = model.generate_content(prompt)
    
    # Intenta limpiar la respuesta si contiene marcadores de código
    try:
        raw_text = response.text.strip()
        if raw_text.startswith('```json'):
            raw_text = raw_text.replace('```json', '').replace('```', '').strip()
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        print(f"\nError de formato JSON: {e}")
        print("Respuesta cruda de Gemini:", response.text)
        return None

def main():
    """Función principal que orquesta todo el proceso."""
    palabras_pendientes = obtener_palabras_pendientes()
    if not palabras_pendientes:
        print("No hay palabras pendientes para procesar. ¡Todo listo!")
        return

    glosario_data = cargar_glosario_existente()
    
    print(f"Encontradas {len(palabras_pendientes)} palabras pendientes.")
    
    for palabra in palabras_pendientes:
        print(f"\n--- Procesando: {palabra} ---")
        analisis = pedir_analisis_a_gemini(palabra)
        
        if analisis:
            # Mostrar la información para revisión
            print(json.dumps(analisis, ensure_ascii=False, indent=2))
            
            respuesta_usuario = input("\n¿Es correcto? (y/n/q para salir): ").lower()
            
            if respuesta_usuario == 'y':
                glosario_data.append(analisis)
                guardar_glosario(glosario_data)
                actualizar_estado_palabra(palabra, 'completado')
                print(f"✅ '{palabra}' guardada con éxito.")
            elif respuesta_usuario == 'n':
                actualizar_estado_palabra(palabra, 'error')
                print(f"❌ '{palabra}' marcada para revisión. No se guardó.")
            elif respuesta_usuario == 'q':
                print("Proceso terminado por el usuario.")
                break
        else:
            print(f"❌ Error al obtener el análisis para '{palabra}'. Marcando como error.")
            actualizar_estado_palabra(palabra, 'error')

if __name__ == "__main__":

    main()
