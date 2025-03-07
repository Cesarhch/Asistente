import os
from memoria import memoria_global

ARCHIVO_DATOS = "escribirdatos.txt"

def obtener_ultimo_texto():
    """Obtiene la última interacción usuario-asistente desde la memoria."""
    memoria = memoria_global.obtener_memoria()
    print(memoria)
    if not memoria:
        return "No hay conversaciones recientes para escribir."

    ultima_interaccion = memoria[-1]
    usuario_texto = ultima_interaccion.get("usuario", "")
    asistente_texto = ultima_interaccion.get("asistente", "")

    return f"Usuario: {usuario_texto}\nAsistente: {asistente_texto}"

def escribir_en_archivo(texto):
    """Escribe el texto en `escribirdatos.txt`, creando el archivo si no existe."""
    try:
        with open(ARCHIVO_DATOS, "a", encoding="utf-8") as archivo:
            archivo.write(texto + "\n")
        return f"Texto guardado: {texto}"
    except Exception as e:
        return f"Error al escribir en el archivo: {e}"

def escribirdatos(texto_usuario):
    """Guarda el texto en el archivo, ya sea ingresado por el usuario o la última conversación."""
    if not texto_usuario.strip():
        return "No hay texto para escribir."

    if texto_usuario.lower() in ["escribe esto último", "escribe esto ultimo", "escribe esto", "guarda esto"]:
        texto_a_guardar = obtener_ultimo_texto()
    else:
        texto_a_guardar = texto_usuario

    return escribir_en_archivo(texto_a_guardar)
