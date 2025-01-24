import vosk
import pyaudio
import json
import numpy as np
import librosa
from scipy.signal import butter, lfilter
from terminartodo import finalizar_todo
from voz import play_audio, stop_audio_thread
from hardware import obtener_texto
from contexto import Contexto
from funciones import limpiar_texto, diferenciar_voz

# Ruta al modelo Vosk
VOSK_MODEL_PATH = r"C:\Users\cesar\Desktop\serveria\Asistente-main\PC\src\vosk-model-es-0.42"

# Filtro paso banda para limpiar el audio
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut=300.0, highcut=3400.0, fs=16000, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Umbral dinámico de silencio
def calcular_umbral_silencio(audio, factor=1.5):
    return np.mean(np.abs(audio)) * factor

def record_audio():
    # Cargar modelo Vosk
    model = vosk.Model(VOSK_MODEL_PATH)
    recognizer = vosk.KaldiRecognizer(model, 16000)

    # Configuración inicial
    Contexto.creadoAsistente = 0
    Contexto.mic = pyaudio.PyAudio()
    Contexto.stream = Contexto.mic.open(
        format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048
    )
    Contexto.stream.start_stream()

    referencia_usuario = [-452.66672, 174.96278, 21.917921, 9.660542, -20.76454, -3.944893, 2.895618, 0.7380168, -12.437665, -2.38877, 1.9748857, -2.9671273, -5.552887]
    referencia_asistente = [-543.682, 94.14762, -5.437878, 8.3973, -35.455864, 8.672268, 13.015623, 10.601723, 6.9968357, 11.419529, -2.7003953, 4.6719046, 3.073822]

    acumulador_audio = []
    print("Iniciando reconocimiento de voz...")

    try:
        while True:
            data = Contexto.stream.read(2048, exception_on_overflow=False)
            audio = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0

            # Filtrar ruido
            audio_filtrado = bandpass_filter(audio)

            # Normalizar audio
            if np.max(np.abs(audio_filtrado)) > 0:
                audio_normalizado = audio_filtrado / np.max(np.abs(audio_filtrado))
            else:
                audio_normalizado = audio_filtrado

            # Calcular RMS y umbral dinámico
            rms = np.sqrt(np.mean(np.square(audio_normalizado)))
            umbral_silencio = calcular_umbral_silencio(audio_normalizado, factor=1.2)
            #print(f"RMS: {rms:.6f}, Umbral de silencio: {umbral_silencio:.6f}")

            if rms < umbral_silencio:
                #print("Silencio detectado...")
                continue

            # Clasificar: ¿Usuario o asistente?
            mfccs = librosa.feature.mfcc(y=audio_normalizado, sr=16000, n_mfcc=13)
            clasificacion = diferenciar_voz(mfccs, referencia_usuario, referencia_asistente)

            if clasificacion == "asistente" and rms > umbral_silencio:
                Contexto.referencia_asistente = audio_normalizado
                continue  # Ignorar el audio del asistente

            # Manejar audio del usuario
            acumulador_audio.append(audio_normalizado)
            if len(acumulador_audio) > 10:  # Acumula bloques para reconocimiento
                audio_completo = np.concatenate(acumulador_audio)
                audio_bytes = (audio_completo * 32768).astype(np.int16).tobytes()
                acumulador_audio = []  # Reinicia el acumulador

                if recognizer.AcceptWaveform(audio_bytes):
                    Contexto.text = recognizer.Result()
                    try:
                        Contexto.text = json.loads(Contexto.text)['text']
                        if Contexto.text.strip():
                            print(f"Texto reconocido: {Contexto.text}")

                        # Procesar comandos específicos
                        if Contexto.text.lower() == "terminar micro":
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
                        elif (Contexto.creadoAsistente == 1 or Contexto.creadoAsistente == 2) and Contexto.text:
                            Contexto.asis_usuario = False
                            Contexto.cont_usuario = 0
                            obtener_texto(Contexto.text)
                    except KeyError:
                        continue
    except KeyboardInterrupt:
        print("\nReconocimiento interrumpido.")
    finally:
        Contexto.stream.stop_stream()
        Contexto.stream.close()
        Contexto.mic.terminate()
