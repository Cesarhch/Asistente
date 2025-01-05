from tkinter import *
from reconocimiento import record_audio
import threading
import subprocess
import io
import contextlib
from interfaz import mostrar_ventana
from hardware import obtener_texto

# Ejecutar el segundo código en un subshell
subprocess.Popen(["python3", "datostxt.py"])

# Context manager para suprimir la salida estándar y la salida de error
@contextlib.contextmanager
def suppress_stdout_stderr():
    with open(io.StringIO(), 'w') as f, contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
        yield


def main():
    # Se inicia la grabación de audio en una función separada
    record_audio_thread = threading.Thread(target=record_audio)
    
    record_audio_thread.start()
    
    ventana=mostrar_ventana(callback_obtener_texto=obtener_texto)
    ventana.mainloop()  
if __name__ == "__main__":

    main()