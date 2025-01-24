import os
from gtts import gTTS
#import pyttsx3
import threading
from contexto import Contexto
import subprocess

# Variables globales para manejar el hilo de audio
Contexto.audio_thread = None
Contexto.stop_audio = threading.Event()

def play_audio(text):
    
    Contexto.stop_audio.clear()
    #Convierte texto a voz y lo reproduce.
    #Usa gTTS por defecto y pyttsx3 con la voz 'Mónica' como respaldo si gTTS falla.
    def audio_worker():
        audio_file = "C:/Users/cesar/Desktop/serveria/Asistente-main/PC/src/temp.mp3"
        try:
            # Intentar usar gTTS
            tts = gTTS(text=text, lang="es")
            tts.save(audio_file)
            # Reproducir el audio usando subprocess
            with subprocess.Popen(["mpg123.exe", audio_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) as process:
                while process.poll() is None:
                    if Contexto.stop_audio.is_set():
                        process.terminate()  # Detener la reproducción
                        break
            if os.path.exists(audio_file):
                os.remove(audio_file)  
        except Exception as e:
            print(f"Error con gTTS: {e}")
            #print("Usando motor de texto a voz local con la voz 'Mónica'...")
            """
            try:
                # Respaldo con pyttsx3 y configuración directa de 'Mónica'
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)  # Velocidad de habla
                engine.setProperty('volume', 0.9)  # Volumen
                engine.setProperty('voice', 'com.apple.speech.synthesis.voice.monica')  # Voz 'Mónica'
                text_de_fallo="No hay motor renderizado en linea, paso a teclado"
                engine.say(text_de_fallo)
                engine.runAndWait()
            except Exception as local_e:
                print(f"Error con pyttsx3: {local_e}")
            """
    # Detiene cualquier audio previo
    stop_audio_thread()

    # Crea un nuevo hilo para la reproducción de audio
    Contexto.audio_thread = threading.Thread(target=audio_worker)
    Contexto.audio_thread.start()

def stop_audio_thread():
    #Detiene la reproducción de audio.
    if Contexto.audio_thread and Contexto.audio_thread.is_alive():
        Contexto.stop_audio.set()
        Contexto.audio_thread.join()
        Contexto.audio_thread = None