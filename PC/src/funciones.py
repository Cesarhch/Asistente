import unicodedata
import os

def save_cesar(information):
  with open("/Users/cesarhernandez/Documents/PlatformIO/Projects/RAG-1/prueba2/datoscasa2.txt", "a", newline="") as file:  # Open in append mode
    file.write(information + "\n")
    file.close()

def limpiar_texto(texto):
    # Elimina acentos
    texto_sin_acentos = ''.join(
        c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'
    )
    # Elimina espacios al inicio y al final
    return texto_sin_acentos.strip()

def contar_archivos_en_directorio(directorio):
    #Cuenta los archivos en un directorio dado.
    directorio="/Users/cesarhernandez/Documents/PlatformIO/Projects"
    if not os.path.exists(directorio):
        return f"El directorio {directorio} no existe."
    
    if not os.path.isdir(directorio):
        return f"{directorio} no es un directorio válido."
    
    archivos = []
    carpetas = []

    # Clasificar elementos en archivos y carpetas
    for item in os.listdir(directorio):
        ruta_completa = os.path.join(directorio, item)
        if os.path.isfile(ruta_completa):
            archivos.append(item)
        elif os.path.isdir(ruta_completa):
            carpetas.append(item)

    # Crear la respuesta
    respuesta = (
        f"El directorio {directorio} contiene:\n"
        f"- {len(archivos)} archivos\n"
        f"- {len(carpetas)} carpetas\n"
    )

    if archivos:
        respuesta += "\nArchivos:\n" + "\n".join(archivos)
    if carpetas:
        respuesta += "\n\nCarpetas:\n" + "\n".join(carpetas)

    return respuesta