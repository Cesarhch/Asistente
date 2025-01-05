import os
from gtts import gTTS
import pyttsx3

def play_audio(text):
    
    #Convierte texto a voz y lo reproduce.
    #Usa gTTS por defecto y pyttsx3 con la voz 'Mónica' como respaldo si gTTS falla.
    
    try:
        # Intentar usar gTTS
        tts = gTTS(text=text, lang="es")
        audio_file = "/Users/cesarhernandez/Documents/PlatformIO/Projects/server_IA/temp.mp3"
        tts.save(audio_file)
        os.system(f"/opt/homebrew/bin/mpg123 {audio_file}")
        os.remove(audio_file)
    except Exception as e:
        print(f"Error con gTTS: {e}")
        print("Usando motor de texto a voz local con la voz 'Mónica'...")
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
