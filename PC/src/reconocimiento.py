import vosk
import pyaudio
import json
from terminartodo import finalizar_todo 
from voz import play_audio, stop_audio_thread
from hardware import obtener_texto
from contexto import Contexto
from funciones import limpiar_texto, diferenciar_voz
import numpy as np
import librosa

def record_audio():
    model = vosk.Model(r"/Users/cesarhernandez/Documents/PlatformIO/Projects/server_IA/voz/vosk-model-es-0.42")
    recognizer = vosk.KaldiRecognizer(model, 16000)
    Contexto.creadoAsistente = 0
    Contexto.mic = pyaudio.PyAudio()
    Contexto.stream = Contexto.mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
    Contexto.stream.start_stream()

    # Definir referencias para usuario y asistente
    referencia_usuario = [-452.66672, 174.96278, 21.917921, 9.660542, -20.76454, -3.944893, 2.895618, 0.7380168, -12.437665, -2.38877, 1.9748857, -2.9671273, -5.552887]
    referencia_asistente = [-543.682, 94.14762, -5.437878, 8.3973, -35.455864, 8.672268, 13.015623, 10.601723, 6.9968357, 11.419529, -2.7003953, 4.6719046, 3.073822]

    una_palabra=0
    umbral_silencio=0.0004
    acumulador_audio = []

    while True:
        data = Contexto.stream.read(2048, exception_on_overflow=False) 
        audio = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0

        # Extraer características
        mfccs = librosa.feature.mfcc(y=audio, sr=16000, n_mfcc=13)

        rms = np.sqrt(np.mean(np.square(audio)))
        #print(rms)
        
        # Clasificar: ¿Es usuario o asistente?
        clasificacion = diferenciar_voz(mfccs, referencia_usuario, referencia_asistente)

        if clasificacion == "asistente" and rms > umbral_silencio:
            # Guardar la referencia del asistente
            Contexto.referencia_asistente = audio
            #print("dentro de asistente")
            continue  # Ignorar el audio identificado como asistente
            
        if clasificacion == "usuario" or (una_palabra == 1 and rms < umbral_silencio):
            # Comparar con la referencia del asistente y eliminar coincidencias
            una_palabra=1
            if hasattr(Contexto, "referencia_asistente"):
                # Asegurar que las longitudes coinciden antes de restar
                min_len = min(len(audio), len(Contexto.referencia_asistente))
                audio_residual = audio[:min_len] - Contexto.referencia_asistente[:min_len]
            else:
                audio_residual = audio
            if rms < umbral_silencio:
                acumulador_audio.append(np.zeros_like(audio))
            else:
                audio_residual_int16 = (audio_residual * 32768.0).astype(np.int16)
                acumulador_audio.append(audio_residual_int16)
            audio_completo = np.concatenate(acumulador_audio).astype(np.int16).tobytes()
            acumulador_audio = []
            # Procesar el audio residual con Vosk
            if recognizer.AcceptWaveform(audio_completo):
                Contexto.text = recognizer.Result()
                try:
                    Contexto.text = json.loads(Contexto.text)['text']
                    print(f"Texto reconocido: {Contexto.text}")
                    una_palabra=0
                    acumulador_audio = []
                    # Responder a comandos específicos
                    if Contexto.text.lower() == "termina micro":
                        Contexto.creadoAsistente = 0 
                        play_audio("microfono apagado")
                        continue
                    if Contexto.text.lower() == "desconecta micro":
                        Contexto.creadoAsistente = 0
                        play_audio("desconecto micro") 
                        Contexto.stream.stop_stream()
                        Contexto.stream.close()
                        Contexto.mic.terminate()
                        break 
                    if Contexto.text.lower() == "terminar todo":
                        Contexto.creadoAsistente = 0
                        play_audio("cierro sesion")
                        Contexto.stream.stop_stream()
                        Contexto.stream.close()
                        Contexto.mic.terminate()
                        finalizar_todo()
                        break     
                    if Contexto.text.lower() == "para":
                        play_audio("ok")
                        stop_audio_thread()
                        Contexto.asis_usuario = False
                        Contexto.cont_usuario = 0
                        continue   
                    if Contexto.text.lower() == "hola lara":
                        play_audio("Hola, en que puedo ayudarte.")
                        Contexto.creadoAsistente = 1
                        Contexto.asis_usuario = False
                        Contexto.cont_usuario = 0
                        continue
                    if limpiar_texto(Contexto.text.lower()) == "hola tecnico":
                        play_audio("Hola, en que puedo ayudarte.")
                        Contexto.creadoAsistente = 2
                        continue
                    if limpiar_texto(Contexto.text.lower()) == "pasame con lara":
                        play_audio("ok, te paso con lara.")
                        Contexto.creadoAsistente = 1
                        continue
                    if limpiar_texto(Contexto.text.lower()) == "pasame con tecnico":
                        play_audio("ok, te paso con tecnico.")
                        Contexto.creadoAsistente = 2
                        continue
                    elif (Contexto.creadoAsistente==1 or Contexto.creadoAsistente==2) and Contexto.text:
                        #print(Contexto.text)
                        Contexto.asis_usuario = False
                        Contexto.cont_usuario = 0
                        obtener_texto(Contexto.text)
                except KeyError:
                    continue
