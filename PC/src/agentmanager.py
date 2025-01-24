from agentelocal import consultar_modelo_local
from agentetecnico import consultar_agente_tecnico
from unidecode import unidecode
import string
from contexto import Contexto

def responder_agente_managment(pregunta):
    # Determina a qué modelo consultar dependiendo del valor de creadoAsistente.
    print("Consultando al agente...")
    
    if Contexto.creadoAsistente==0:
      Contexto.creadoAsistente=1
      
    if Contexto.creadoAsistente == 1:
        print("Usando modelo local...")
        respuesta = consultar_modelo_local(pregunta)
    elif Contexto.creadoAsistente == 2:
        print("Usando agente técnico...")
        respuesta = consultar_agente_tecnico(pregunta)
    else:
        # Manejo de caso por defecto, si creadoAsistente no está configurado adecuadamente.
        respuesta = "No se ha seleccionado un modelo válido para responder la pregunta."

    # Normaliza la respuesta para eliminar caracteres especiales o mayúsculas innecesarias.
    respuesta_normalizada = unidecode(respuesta).rstrip(string.punctuation)

    return respuesta_normalizada

