from agenteentrenado import generar_respuesta
from voz import play_audio, stop_audio_thread
from terminartodo import finalizar_todo
from contexto import Contexto
from funciones import limpiar_texto
from memoria import memoria_global
from interfaz import actualizar_conversacion

def obtener_texto(entrada, ventana=None):
    if hasattr(entrada, "get"):
        texto_introducido_ventana = entrada.get()
    else:
        texto_introducido_ventana = entrada
    
    texto_introducido = texto_introducido_ventana.strip().lower() if texto_introducido_ventana.strip() else ""

    if texto_introducido:
        stop_audio_thread()
    
    Contexto.prompt = texto_introducido

    if texto_introducido in ["terminar todo", "terminar micro", "terminar ventana"]:
        play_audio("ok, cerrando sesión")
        finalizar_todo()
        return

    try:
        resultado = generar_respuesta(Contexto.prompt)

        if hasattr(resultado, "content") and resultado.content:
            texto_a_reproducir = resultado.content.strip()
        else:
            texto_a_reproducir = resultado

    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
        texto_a_reproducir = "Hubo un error al procesar la solicitud."
        return

    if not texto_a_reproducir.strip():
        texto_a_reproducir = "No hay respuesta."

    memoria_global.actualizar_memoria(texto_introducido, texto_a_reproducir)

    print(f"Pregunta: {texto_introducido}")
    print(f"Respuesta: {texto_a_reproducir}")

    actualizar_conversacion(texto_introducido, texto_a_reproducir)  # Actualiza la interfaz con la conversación

    play_audio(texto_a_reproducir)
    return texto_a_reproducir
