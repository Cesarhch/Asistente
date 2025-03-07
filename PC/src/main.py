from tkinter import *
from reconocimiento import record_audio
import threading
from interfaz import mostrar_ventana
from hardware import obtener_texto
from contexto import Contexto
from terminartodo import borrar_base_datos_chroma
import subprocess

#Ejecutamos actualizar_managment.py como un subproceso 
subprocess.run(["python", "actualizar_managment.py"])

def main():
    if not Contexto.db_borrada:
        borrar_base_datos_chroma()
        Contexto.db_borrada = True
    # Inicializar el evento para detener audio
    Contexto.stop_audio = threading.Event()
    
    # Se inicia la grabación de audio en una función separada
    record_audio_thread = threading.Thread(target=record_audio)
    
    record_audio_thread.start()
    
    Contexto.ventana=mostrar_ventana(callback_obtener_texto=obtener_texto)
    Contexto.ventana.mainloop()
 
if __name__ == "__main__":

    main()
