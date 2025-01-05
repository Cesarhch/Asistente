from modelos import configurar_rag, consultar_modelo_local

def responder_agente_managment(pregunta):
    
    #Responde preguntas utilizando la base de datos vectorial del agente managment.
    
    print("Consultando al agente managment...")
    respuesta = consultar_modelo_local(pregunta)
    
    return respuesta
