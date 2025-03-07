import unicodedata
import os
from contexto import Contexto
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def save_cesar(information):
  with open("/ruta/RAG-1/prueba2/datoscasa2.txt", "a", newline="") as file:  # Open in append mode
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
    directorio="/ruta/Projects"
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

def es_ruido(mfccs, rms, mfcc_umbral=(-700, -600), rms_umbral=0.0006):
    """
    Determina si la entrada es ruido basado en los valores de MFCC y RMS.
    """
    # Verificar si RMS está por debajo del umbral
    if rms < rms_umbral:
        return True

    # Verificar si MFCC promedio está en el rango del ruido
    if np.mean(mfccs) > mfcc_umbral[0] and np.mean(mfccs) < mfcc_umbral[1]:
        return True

    return False

def diferenciar_voz(mfccs, referencia_usuario, referencia_asistente):
    """
    Determina si el audio corresponde al usuario o al asistente.
    """
    similarity_user = cosine_similarity([np.mean(mfccs, axis=1)], [referencia_usuario])[0][0]
    similarity_assistant = cosine_similarity([np.mean(mfccs, axis=1)], [referencia_asistente])[0][0]

    if similarity_user > similarity_assistant:
        return "usuario"
    else:
        return "asistente"
