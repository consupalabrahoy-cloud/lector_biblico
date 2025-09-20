import sqlite3
import json
import os

# --- Configuración de los archivos ---
DB_FILE = 'vocabulario.db'
JSON_FILE = 'vocabulario_nt.json'

def export_db_to_json():
    """
    Exporta todos los datos de la tabla 'vocabulario' de la base de datos SQLite
    a un archivo JSON.
    """
    if not os.path.exists(DB_FILE):
        print(f"Error: La base de datos '{DB_FILE}' no se encontró.")
        return

    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        # Obtener los nombres de las columnas
        c.execute("PRAGMA table_info(vocabulario)")
        column_names = [column[1] for column in c.fetchall()]

        # Obtener todos los datos de la tabla
        c.execute("SELECT * FROM vocabulario")
        rows = c.fetchall()
        
        # Convertir los datos a una lista de diccionarios
        data = []
        for row in rows:
            entry = dict(zip(column_names, row))
            # Cargar el campo 'analisis_gramatical' como un objeto JSON si es posible
            try:
                if entry['analisis_gramatical']:
                    entry['analisis_gramatical'] = json.loads(entry['analisis_gramatical'])
            except json.JSONDecodeError:
                # Si no es un JSON válido, déjalo como está
                pass
            data.append(entry)

        # Escribir los datos en un archivo JSON
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        print(f"¡Exportación exitosa! El archivo '{JSON_FILE}' ha sido creado.")
        print(f"Ahora puedes subir '{JSON_FILE}' a GitHub.")

    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    export_db_to_json()
