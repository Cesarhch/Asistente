import numpy as np
class Contexto:
    ventana = None
    mic = None
    stream = None
    audio_thread = None  # Variable para manejar el hilo de audio
    stop_audio = None 
    creadoAsistente = 0
    creadoAsistentev = 0
    audio_bloqueado = True
    text=""
    asistente_hablando = True
    cont_usuario = 0
    asis_usuario = False
    referencia_asistente = np.zeros(2048, dtype=np.float32)
