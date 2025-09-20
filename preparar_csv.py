#agrega a cada palabra: ,pendiente
import csv

# --- Nombres de los archivos ---
archivo_original = 'palabras_griegas.csv'
archivo_preparado = 'palabras_pendientes.csv'

def preparar_archivo_csv(entrada, salida):
    """
    Transforma el archivo CSV con una sola columna en el formato requerido.
    """
    try:
        with open(entrada, 'r', encoding='utf-8') as infile, \
             open(salida, 'w', newline='', encoding='utf-8') as outfile:
            
            # Crea un escritor de CSV para el nuevo archivo
            writer = csv.writer(outfile)
            
            # Escribe el encabezado de las columnas
            writer.writerow(['palabra', 'estado'])
            
            # Lee cada línea del archivo original y la procesa
            for linea in infile:
                # Elimina espacios y saltos de línea
                palabra = linea.strip()
                if palabra: # Asegura que la línea no esté vacía
                    writer.writerow([palabra, 'pendiente'])
            
        print(f"🎉 ¡Éxito! El archivo '{salida}' ha sido creado con 17,000 palabras listas.")
    
    except FileNotFoundError:
        print(f"Error: El archivo '{entrada}' no se encontró. Asegúrate de que está en la misma carpeta.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# Llama a la función principal
preparar_archivo_csv(archivo_original, archivo_preparado)