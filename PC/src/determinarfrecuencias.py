#Archivo para determinar las frecuencias de voz de los usuarios
import librosa
import numpy as np

# Ruta del archivo de audio
audio_file = "/ruta_al _archivo/usuario.mp3"

# Cargar el archivo de audio
audio_data, sr = librosa.load(audio_file, sr=None)

# Calcular las frecuencias dominantes
pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sr)
freqs = []
for i in range(pitches.shape[1]):
    index = magnitudes[:, i].argmax()
    freqs.append(pitches[index, i])

# Filtrar frecuencias válidas
freqs = [f for f in freqs if f > 50 and f < 500]
if freqs:
    freqs_min = round(min(freqs), 6)
    freqs_max = round(max(freqs), 6)
    print(f"Frecuencia mínima: {freqs_min} Hz, máxima: {freqs_max} Hz")
else:
    print("No se detectaron frecuencias válidas.")
    freqs_min = None
    freqs_max = None

# Calcular los MFCCs (timbre)
mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13)  # Usa sr aquí
mfccs_mean = [round(val, 6) for val in np.mean(mfccs, axis=1)]  # Promedio con 6 decimales

# Calcular la amplitud (RMS)
rms = librosa.feature.rms(y=audio_data)
rms_mean = round(np.mean(rms), 6)  # Promedio con 6 decimales

# Obtener resultados en un array
resultados = {
    "frecuencias_dominantes": {
        "min": freqs_min,
        "max": freqs_max
    },
    "mfccs_promedio": mfccs_mean,
    "rms_promedio": rms_mean
}

# Imprimir resultados
print("\nResultados del análisis de audio:")
print(resultados)
