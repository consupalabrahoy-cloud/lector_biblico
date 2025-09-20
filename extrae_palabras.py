import requests
import csv

BOOKS_URLS = {
    "Mateo": "https://gist.githubusercontent.com/consupalabrahoy-cloud/e866f6e1554298f5c96601a500aad1b0/raw/1698e351a24d0ce1731f74eb5ffeede61f8936f1/Mateo.csv",
    "Marcos": "https://gist.githubusercontent.com/consupalabrahoy-cloud/279a23eb035734174d2f1ab934c60a4c/raw/f102760bab3a6c1bc0f5678736977ae1cb39d8b0/Marcos.csv",
    "Lucas": "https://gist.githubusercontent.com/consupalabrahoy-cloud/18caf9a4a6c7fbbb6cb737575226e2b2/raw/2c1f99c882cd48a5bbadc934a1ada265a54d67b2/Lucas.csv",
    "Juan": "https://gist.githubusercontent.com/consupalabrahoy-cloud/de1be45bd708b8e5a9faa27180928c6d/raw/21c37db0ad85a68c310976cb4da83cf3e37ff421/Juan.csv",
    "Hechos": "https://gist.githubusercontent.com/consupalabrahoy-cloud/57ad8a0d06aff8cc558ab049ecc986f6/raw/dd1cc2af6d04ddfff3738c43be53c638453eedfe/Hechos.csv",
    "Romanos": "https://gist.githubusercontent.com/consupalabrahoy-cloud/9ed5dd10e494b5a2b59fb72a27659494/raw/64a9f092ec80d0b41bddecf8d87e6b0529544209/romanos.csv",
    "1º a los Corintios": "https://gist.githubusercontent.com/consupalabrahoy-cloud/d91777893510b11a73c403472c3fc053/raw/4165385e2f3ea71c4184e2af76e1816890e85143/PrimeraCorintios.csv",
    "2º a los Corintios": "https://gist.githubusercontent.com/consupalabrahoy-cloud/23835350791d75a2fd2b74460c47f313/raw/a5b5e78264bd1101a4f342c3e34f80379695a93b/SegundaCorintios.csv",
    "Gálatas": "https://gist.githubusercontent.com/consupalabrahoy-cloud/191befa64bed89146535058beb193d73/raw/4f08d3626fd889b28446fa0736ed7ce1e257b94b/G%25C3%25A1latas.csv",
    "Efesios": "https://gist.githubusercontent.com/consupalabrahoy-cloud/e494aa96ec0921af3c26f5cb4e838070/raw/e50b7c28a97e241fca44622a27ac5c4addc0684a/Efesios.csv",
    "Filipenses": "https://gist.githubusercontent.com/consupalabrahoy-cloud/1410fab184350abc0456899fa275d922/raw/8122da6a4caafb3c57a4f0ef16c5e077e07d3ac9/Filipenses.csv",
    "Colosenses": "https://gist.githubusercontent.com/consupalabrahoy-cloud/513d84d430af573d6758e9111842834f/raw/5cb45edc3c349761add831d7c39799a3c5dd09cd/Colosenses.csv",
    "1º a los Tesalonicenses": "https://gist.githubusercontent.com/consupalabrahoy-cloud/5927763cc04e71fc1cb9d8077c71d4dd/raw/8ba01a0c3033439e1e1c645de299b99180687ca1/PrimeraTesalonicenses",
    "2º a los Tesalonicenses": "https://gist.githubusercontent.com/consupalabrahoy-cloud/c9eade95386dea0021d373b44ac43f77/raw/03b55d89cf5b0582e5fae419ad362bf746ca64cc/SegundaTesalonicenses.csv",
    "1º a Timoteo": "https://gist.githubusercontent.com/consupalabrahoy-cloud/b5c12c3507bc458ab7fc17f1f7f9b7df/raw/4876881d64d65c799a9731752e59de434f5ff221/PrimeraTimoteo.csv",
    "2º a Timoteo": "https://gist.githubusercontent.com/consupalabrahoy-cloud/28c5875b0f6212a46a42b11f7aa4d91d/raw/ac4181e903c690bd075d1023cc3c36d172f0beb5/SegundaTimoteo.csv",
    "Tito": "https://gist.githubusercontent.com/consupalabrahoy-cloud/ab4fc95416837371385d075957a56efc/raw/39e6dd720a19ce949aac4c54ba9715d02b00908a/Tito.csv",
    "Filemón": "https://gist.githubusercontent.com/consupalabrahoy-cloud/35f2c52e4199e169d375875052d7383c/raw/3efa655484184c07b5e54ab6deae493af20d9734/Filemon.csv",
    "Hebreos": "https://gist.githubusercontent.com/consupalabrahoy-cloud/82df333eb092948670371501c4863b4e/raw/e29329ac705757313e531bf124cea8b6c231ef33/Hebreos.csv",
    "Santiago": "https://gist.githubusercontent.com/consupalabrahoy-cloud/e825c31c8fa88560ec91f37cf52f8442/raw/6288124abc9b3e96c2fd60213703ecc02f112b7c/Santiago.csv",
    "1º de Pedro": "https://gist.githubusercontent.com/consupalabrahoy-cloud/9519dac9507f0518b6ab80208420c62a/raw/93d4fc402d7635bc251f6ed1386d9a9783b79667/PrimeraPedro.csv",
    "2º de Pedro": "https://gist.githubusercontent.com/consupalabrahoy-cloud/13f172ea05f41376ea3cd831c7816fd3/raw/245c8510ce8f750a63eef8f92d8f38435cdc6b07/SegundaPedro.csv",
    "1º de Juan": "https://gist.githubusercontent.com/consupalabrahoy-cloud/1666b27d0db16ae636d227cd974c5062/raw/d365df0d1f8c4956142749a55023532a818cf954/PrimeraJuan.csv",
    "2º de Juan": "https://gist.githubusercontent.com/consupalabrahoy-cloud/36ce60ee4f590f2e4dc3070dd065b97b/raw/577e514f43b19af0465a96711c9083f16681e1fd/SegundaJuan.csv",
    "3º de Juan": "https://gist.githubusercontent.com/consupalabrahoy-cloud/e9dbbe82c952fce14bf0e6704df144ab/raw/896226e6f87b9e596f1ddcb91e0ec9d8eb9285e3/TerceraJuan.csv",
    "Judas": "https://gist.githubusercontent.com/consupalabrahoy-cloud/fede1c609f50bd6e8607f2713df0eb8d/raw/7228ff11bc2319f1ef263028b0b5fbf2644f6136/Judas.csv",
    "Apocalipsis": "https://gist.githubusercontent.com/consupalabrahoy-cloud/50089fb1221cb00f8c7f7a2b8fc2c56f/raw/f08b0b312a8f564da935aecd3b6cd48ce5bad033/Apocalipsis.csv",
}

def is_greek_word(word):
    """
    Comprueba si la palabra contiene caracteres del alfabeto griego.
    """
    # Rango de caracteres Unicode para el alfabeto griego
    for char in word:
        if 'α' <= char <= 'ω' or 'Α' <= char <= 'Ω':
            return True
    return False

def extract_and_save_greek_words_to_csv(books_urls):
    """
    Recorre los archivos CSV desde las URLs, extrae las palabras griegas
    sin repetir y las guarda en un archivo CSV.
    """
    greek_words = set()
    
    # Recorrer cada libro en la lista de URLs
    for book_name, url in books_urls.items():
        print(f"Procesando el libro: {book_name}")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            content = response.text.splitlines()
            csv_reader = csv.reader(content)
            
            # Saltar la primera fila (encabezado)
            next(csv_reader, None)
            
            for row in csv_reader:
                # El texto con las palabras griegas está en la cuarta columna, índice 3.
                if len(row) > 3:
                    text_content = row[3].strip()
                    # Dividir el texto en palabras y buscar las griegas
                    words = text_content.split()
                    for word in words:
                        # Eliminar cualquier puntuación
                        clean_word = word.strip('.,;":\'()[]{}')
                        if is_greek_word(clean_word):
                            greek_words.add(clean_word)
        
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar {book_name} de {url}: {e}")
        except IndexError:
            print(f"Error: La fila en el CSV de {book_name} no tiene la estructura esperada.")
            
    # Guardar las palabras únicas en un nuevo archivo CSV
    output_filename = "palabras_griegas.csv"
    try:
        with open(output_filename, "w", newline="", encoding="utf-8") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["Palabra Griega"]) # Escribir el encabezado
            
            # Ordenar las palabras para que el archivo sea más consistente
            for word in sorted(list(greek_words)):
                csv_writer.writerow([word])
        
        print(f"\n¡Proceso completado! Se han guardado {len(greek_words)} palabras griegas únicas en '{output_filename}'.")
    except IOError as e:
        print(f"Error al escribir en el archivo '{output_filename}': {e}")


# Ejecutar la función principal
extract_and_save_greek_words_to_csv(BOOKS_URLS)