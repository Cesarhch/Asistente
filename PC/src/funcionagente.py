from agentelocal import consultar_modelo_local  # Importar el agente local
from contexto import Contexto  # Importar el contexto para acceder al prompt
from memoria import memoria_global
from gmail import gmail_leer
import subprocess
import re
from escribirdatos import escribirdatos

def recogerfuncion(funcion_nombre: str):
    """ Busca la función en el módulo actual y la ejecuta si existe """
    if funcion_nombre in globals():
        print(f"Ejecutando función: {funcion_nombre}")
        return globals()[funcion_nombre]()
    print(f"La función '{funcion_nombre}' no está definida en funcionagente.")
    return modelo()

def get_weather():
    print("Estoy dentro de la función get_weather")
    return "Información meteorológica obtenida."

def calendar():
    """
    Llama a `calendario.py` para obtener los eventos y tareas del usuario en Google Calendar.
    """
    print("Consultando Google Calendar...")

    try:
        resultado = subprocess.run(["python", "calendario.py"], capture_output=True, text=True)

        if resultado.returncode == 0:
            return resultado.stdout.strip()
        else:
            return "Hubo un error al obtener los eventos y tareas del calendario."

    except Exception as e:
        return f"Error al ejecutar calendario.py: {e}"

def extraer_tema(pregunta):
    """
    Extrae el tema de la consulta de noticias y elimina palabras irrelevantes.
    """
    # Lista de palabras clave que pueden aparecer en la pregunta y no son parte del tema
    palabras_irrelevantes = ["qué", "que", "dime", "noticias", "nuevas", "tenemos", "en", "sobre", "hay", "últimas", "información", "ultimas", "las"]
    
    # Convertir pregunta a minúsculas y dividir en palabras
    palabras = pregunta.lower().split()

    # Filtrar palabras irrelevantes
    tema_filtrado = [palabra for palabra in palabras if palabra not in palabras_irrelevantes]

    # Unir las palabras restantes para formar el tema
    tema = " ".join(tema_filtrado).strip()

    return tema if tema else None  # Si no hay tema, devuelve None

def noticias():
    """
    Obtiene la última consulta del usuario desde Contexto.prompt, extrae el tema y ejecuta noticias.py.
    """
    pregunta = Contexto.prompt  # Obtener la última pregunta del usuario
    tema = extraer_tema(pregunta)  # Extraer el tema de la consulta

    if not tema:
        return "Por favor, especifica el tema de las noticias que quieres buscar."

    print(f"Buscando noticias sobre: {tema}")

    try:
        # Ejecutar el script noticias.py con el tema detectado
        resultado = subprocess.run(["python", "noticias.py", tema], capture_output=True, text=True)

        if resultado.returncode == 0:
            return resultado.stdout.strip()
        else:
            return "Hubo un error al obtener noticias."

    except Exception as e:
        return f"Error al ejecutar noticias.py: {e}"

def modelo():
    print("Estoy dentro de la función modelo")

    # Obtener memoria previa para contexto
    memoria_prev = memoria_global.obtener_memoria()

    # Construir el contexto con la memoria de conversación
    contexto_memoria = "\n".join([f"Usuario: {m['usuario']}\nAsistente: {m['asistente']}" for m in memoria_prev])

    # Incluir la memoria en el prompt si hay datos previos
    if contexto_memoria:
        prompt_final = f"{contexto_memoria}\nUsuario: {Contexto.prompt}\nAsistente:"
    else:
        prompt_final = f"Usuario: {Contexto.prompt}\nAsistente:"

    # Llamar al modelo con el nuevo prompt
    respuesta = consultar_modelo_local(prompt_final)

    # Almacenar la nueva interacción en memoria
    memoria_global.actualizar_memoria(Contexto.prompt, respuesta)

    return respuesta

def gmail():
    #print("Estoy dentro de la función gmail")
    return gmail_leer()

def acciones_usb():
    print("Estoy dentro de la función acciones_usb")
    return "Activando acciones por dispositivo."

def search_net():
    pregunta = Contexto.prompt  # Obtener la última consulta del usuario
    tema = extraer_tema(pregunta)  # Intentar extraer el tema

    if not tema:
        return "Por favor, especifica el tema de las noticias que quieres buscar."

    print(f"Buscando noticias sobre: {tema}")

    try:
        resultado = subprocess.run(["python", "noticias.py", tema], capture_output=True, text=True)

        if resultado.returncode == 0:
            return resultado.stdout.strip()
        else:
            return "Hubo un error al obtener noticias."

    except Exception as e:
        return f"Error al ejecutar noticias.py: {e}"

def sensor_db():
    print("Estoy dentro de la función sensor_db")
    return "Obtener informacion de los sensores de la casa."

def escribir():
    """
    Llama directamente a la función `escribir()` pasando `Contexto.prompt`.
    """
    print(f"Ejecutando escritura con prompt: {repr(Contexto.prompt)}")

    if Contexto.prompt is None or not Contexto.prompt.strip():
        return "No hay texto para escribir."

    return escribirdatos(Contexto.prompt.strip())
