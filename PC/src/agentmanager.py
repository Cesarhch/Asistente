from modelos import consultar_modelo_local
from agentetecnico import consultar_agente_tecnico
from unidecode import unidecode
import string

def responder_agente_managment(pregunta):
    
    #Responde preguntas utilizando la base de datos vectorial del agente managment.
    
    print("Consultando al agente managment...")
    respuesta = consultar_modelo_local(pregunta)
    respuesta_normalizada = unidecode(respuesta)
    respuesta_normalizada = respuesta_normalizada.rstrip(string.punctuation)
    if respuesta_normalizada.strip().lower()=="agente tecnico":
        print(respuesta_normalizada)
        respuesta=consultar_agente_tecnico(pregunta)
    
    return respuesta
