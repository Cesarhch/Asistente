from tkinter import *
from reconocimiento import record_audio
import threading
from interfaz import mostrar_ventana
from hardware import obtener_texto
from contexto import Contexto

# Ejecutar el segundo código en un subshell
#subprocess.Popen(["python3", "datostxt.py"])

def main():
    # Inicializar el evento para detener audio
    Contexto.stop_audio = threading.Event()
    
    # Se inicia la grabación de audio en una función separada
    record_audio_thread = threading.Thread(target=record_audio)
    
    record_audio_thread.start()
    
    Contexto.ventana=mostrar_ventana(callback_obtener_texto=obtener_texto)
    Contexto.ventana.mainloop()
 
if __name__ == "__main__":

    main()