import torchaudio
import torchaudio.transforms as transforms
import torch
import numpy as np
import pyaudio
import joblib
import time

# Ruta donde se guardará el embedding de voz
EMBEDDING_PATH = "cesar_embedding.pkl"

# Configuración del micrófono
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 2048
RECORD_SECONDS = 10  # Ajusta a 10-15 segundos para mejorar precisión

# Inicializar PyAudio
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print(" Grabando... Habla claramente para generar tu perfil de voz.")
frames = []

for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK, exception_on_overflow=False)
    frames.append(np.frombuffer(data, dtype=np.int16))

print(" Grabación finalizada.")

# Cerrar el stream
stream.stop_stream()
stream.close()
audio.terminate()

# Convertir a un solo array
waveform = np.concatenate(frames).astype(np.float32)

# Extraer Mel Spectrogram con 80 dimensiones
mel_spectrogram = torchaudio.transforms.MelSpectrogram(
    sample_rate=RATE, 
    n_mels=80,  # Asegurar 80 dimensiones
    n_fft=400,
    win_length=400,
    hop_length=160
)

waveform_torch = torch.from_numpy(waveform).unsqueeze(0)  # Convertir a tensor
features = mel_spectrogram(waveform_torch.to(torch.float32))
embedding = features.mean(dim=2).squeeze().numpy()  # Obtener representación de la voz con 80 dimensiones

# Guardar el embedding
joblib.dump({"César": embedding}, EMBEDDING_PATH)
print(f" Perfil de voz guardado en {EMBEDDING_PATH}")
