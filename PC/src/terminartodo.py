import shutil
import os
import sys
from contexto import Contexto
from interfaz import cerrar_todo

def detener_procesos():
    if Contexto.stream is not None and Contexto.stream.is_active():
        try:
            Contexto.stream.stop_stream()
            Contexto.stream.close()
            print("Stream detenido correctamente.")
        except Exception as e:
            print(f"Error al detener el stream: {e}")
    else:
        print("No hay stream activo para detener.")

    if Contexto.mic is not None:
        try:
            Contexto.mic.terminate()
            print("Micrófono terminado correctamente.")
        except Exception as e:
            print(f"Error al terminar el micrófono: {e}")
    else:
        print("No hay micrófono activo para terminar.")

            
def borrar_base_datos_chroma():
    RUTA_BASE_DATOS = "/Users/cesarhernandez/Documents/PlatformIO/Projects/server_IA/rag/managment"
    RUTA_BASE_DATOS_TECNICO = "/Users/cesarhernandez/Documents/PlatformIO/Projects/server_IA/rag/tecnico"
    try:
        if os.path.exists(RUTA_BASE_DATOS):
            shutil.rmtree(RUTA_BASE_DATOS)
            print(f"Base de datos en {RUTA_BASE_DATOS} eliminada exitosamente.")
        else:
            print(f"La ruta {RUTA_BASE_DATOS} no existe.")
        if os.path.exists(RUTA_BASE_DATOS_TECNICO):
            shutil.rmtree(RUTA_BASE_DATOS_TECNICO)
            print(f"Base de datos en {RUTA_BASE_DATOS_TECNICO} eliminada exitosamente.")
        else:
            print(f"La ruta {RUTA_BASE_DATOS_TECNICO} no existe.")
    except Exception as e:
        print(f"Error al eliminar la base de datos: {e}")

def finalizar_todo():
    print("Iniciando cierre completo del sistema...")
    borrar_base_datos_chroma()
    detener_procesos()
    cerrar_todo()
    print("Cierre completo realizado.")
    sys.exit(0)
