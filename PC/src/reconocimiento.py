import torchaudio
import torchaudio.transforms as transforms
import torch
import vosk
import pyaudio
import json
import numpy as np
import librosa
import joblib
import time
from scipy.spatial.distance import cosine
from scipy.signal import butter, lfilter
from terminartodo import finalizar_todo
from voz import play_audio, stop_audio_thread
from hardware import obtener_texto
from contexto import Contexto
from funciones import limpiar_texto, diferenciar_voz

# Ruta a los modelos
VOSK_MODEL_PATH = r"C:\ruta\src\vosk-model-es-0.42"
EMBEDDING_PATH = "cesar_embedding.pkl"

# Cargar el embedding de César con 80 dimensiones
try:
    embeddings = joblib.load(EMBEDDING_PATH)
    cesar_embedding = embeddings["César"]
    if len(cesar_embedding) != 80:
        raise ValueError(f"El embedding de César tiene {len(cesar_embedding)} dimensiones en lugar de 80.")
except Exception as e:
    print(f"ERROR al cargar el perfil de voz: {e}")
    exit(1)

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

# Extraer características de audio con 80 dimensiones
def extraer_caracteristicas(audio):
    mel_spectrogram = torchaudio.transforms.MelSpectrogram(
        sample_rate=16000, 
        n_mels=80, 
        n_fft=400,
        win_length=400,
        hop_length=160
    )
    waveform_tensor = torch.from_numpy(audio).float().unsqueeze(0)
    features = mel_spectrogram(waveform_tensor)
    return features.mean(dim=2).squeeze().numpy()

# Determinar si la voz es de César
def es_cesar(audio, umbral=0.4):
    caracteristicas_actual = extraer_caracteristicas(audio)
    distancia = cosine(caracteristicas_actual, cesar_embedding)
    return distancia <= umbral

# Umbral dinámico de silencio
def calcular_umbral_silencio(audio, factor=1.5):
    return np.mean(np.abs(audio)) * factor

def record_audio():
    print("Cargando modelo Vosk...")
    model = vosk.Model(VOSK_MODEL_PATH)
    recognizer = vosk.KaldiRecognizer(model, 16000)
    print("Modelo Vosk cargado con éxito.")

    # Configuración del micrófono
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
    stream.start_stream()

    print("Esperando voz...")
    time.sleep(1)

    try:
        while True:
            data = stream.read(2048, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)

            # Evitar que el programa termine si no hay audio capturado
            if len(audio_data) == 0:
                continue  

            waveform = np.array(audio_data)
            if es_cesar(waveform):
                if recognizer.AcceptWaveform(data):
                    resultado = json.loads(recognizer.Result())["text"]
                    if resultado.strip():
                        print(f"Texto reconocido: {resultado}")
                        
                        # Procesar solo si la voz es de César
                        if resultado.lower() in ["terminar micro", "terminar un micro", "termina micro", "termina un micro"]:
                            play_audio("microfono apagado")
                            Contexto.creadoAsistente = 0 
                            continue
                        if resultado.lower() == "desconecta micro":
                            Contexto.creadoAsistente = 0
                            play_audio("desconecto micro") 
                            stream.stop_stream()
                            stream.close()
                            audio.terminate()
                            break 
                        if resultado.lower() in ["terminar todo", "termina todo"]:
                            Contexto.creadoAsistente = 0
                            play_audio("cierro sesion")
                            stream.stop_stream()
                            stream.close()
                            audio.terminate()
                            finalizar_todo()
                            break     
                        if resultado.lower() in ["para", "ya para", "ok", "ya ok"]:
                            play_audio("ok")
                            stop_audio_thread()
                            Contexto.asis_usuario = False
                            Contexto.cont_usuario = 0
                            continue   
                        if resultado.lower() in ["hola lara", "hola clara"]:
                            play_audio("Hola, en qué puedo ayudarte.")
                            Contexto.creadoAsistente = 1
                            Contexto.asis_usuario = False
                            Contexto.cont_usuario = 0
                            continue
                        if limpiar_texto(resultado.lower()) == "hola tecnico":
                            play_audio("Hola, en qué puedo ayudarte.")
                            Contexto.creadoAsistente = 2
                            continue
                        if limpiar_texto(resultado.lower()) == "pasame con lara":
                            play_audio("ok, te paso con lara.")
                            Contexto.creadoAsistente = 1
                            continue
                        if limpiar_texto(resultado.lower()) == "pasame con tecnico":
                            play_audio("ok, te paso con tecnico.")
                            Contexto.creadoAsistente = 2
                            continue
                        elif (Contexto.creadoAsistente == 1 or Contexto.creadoAsistente == 2) and resultado:
                            Contexto.asis_usuario = False
                            Contexto.cont_usuario = 0
                            obtener_texto(resultado)
            else:
                continue  # Ignorar cualquier voz que no sea César

    except KeyboardInterrupt:
        print("Reconocimiento interrumpido.")
    finally:
        print("Liberando recursos...")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        del model

if __name__ == "__main__":
    record_audio()
