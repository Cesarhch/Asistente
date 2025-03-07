import serial
from agenteentrenado import generar_respuesta  # Importar el modelo entrenado
from voz import play_audio, stop_audio_thread
from terminartodo import finalizar_todo
from contexto import Contexto  # Importar el contexto global
from funciones import limpiar_texto
from memoria import memoria_global

def obtener_texto(entrada, ventana=None):
    # Si entrada es un widget de Tkinter
    if hasattr(entrada, "get"):
        texto_introducido_ventana = entrada.get()
    else:
        # Si entrada es un string directo
        texto_introducido_ventana = entrada
    
    texto_introducido = texto_introducido_ventana.strip().lower() if texto_introducido_ventana.strip() else ""
    
    if texto_introducido:
        stop_audio_thread()
    
    # Guardar el prompt en el contexto global
    Contexto.prompt = texto_introducido

    if texto_introducido_ventana.lower() == "terminar todo":
        play_audio("ok, cierro sesión")
        finalizar_todo()
        return
    if texto_introducido_ventana.lower() == "terminar micro":
        play_audio("ok, cierro micro")
        Contexto.creadoAsistente = 0
        return
    if texto_introducido_ventana.lower() == "terminar ventana":
        play_audio("adios, debes cerrar la ventana en manual")
        return   
    if texto_introducido_ventana.lower() == "para" or texto_introducido_ventana.lower() == "para ":
        play_audio("ok")
        return
    if texto_introducido_ventana.lower().startswith("escribir datos "):
        phrase_to_remember = texto_introducido_ventana[len("escribir datos "):].strip()
        play_audio("Información guardada, " + phrase_to_remember)
        return
    
    try:
        # Llamar al modelo entrenado con el prompt guardado en el contexto
        resultado = generar_respuesta(Contexto.prompt)

        if hasattr(resultado, "content") and resultado.content:
            texto_a_reproducir = resultado.content.strip()
        else:
            texto_a_reproducir = resultado

    except Exception as e:
        print(f"Error al usar el modelo local: {e}")
        texto_a_reproducir = "Hubo un error al procesar la solicitud."
        return
    
    if not texto_a_reproducir.strip():
        texto_a_reproducir = "La respuesta está vacía."

    # Actualizar la memoria de conversación solo si hay una respuesta válida
    memoria_global.actualizar_memoria(texto_introducido, texto_a_reproducir)

    # Reproducir el texto final
    print(f"Pregunta: {texto_introducido}")
    print(f"Respuesta: {texto_a_reproducir}")
    respuesta = texto_a_reproducir

    play_audio(respuesta)
    return respuesta
