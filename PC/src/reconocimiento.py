import vosk
import pyaudio
import json 
from voz import play_audio, stop_audio_thread
from hardware import obtener_texto
from contexto import Contexto

def record_audio():
    model=vosk.Model(r"/Users/cesarhernandez/Documents/PlatformIO/Projects/server_IA/voz/vosk-model-es-0.42")
    recognizer = vosk.KaldiRecognizer(model, 16000)
    creadoAsistente=0
    Contexto.mic = pyaudio.PyAudio()
    Contexto.stream = Contexto.mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
    Contexto.stream.start_stream()
    while True:
        data = Contexto.stream.read(2048, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            text=recognizer.Result()
            try:
              text = json.loads(text)['text']
            except KeyError:
              continue
            if not text:
              print(text)
              continue
            if text:
              stop_audio_thread()  # Detener cualquier audio previo
              if text.lower() == "apaga micro":
                creadoAsistente=0 
                play_audio("microfono apagado")
                continue
              if text.lower() == "terminar micro":
                creadoAsistente=0
                play_audio("desconecto micro") 
                Contexto.stream.stop_stream()
                Contexto.stream.close()
                Contexto.mic.terminate()
                break 
              if text.lower() == "terminar todo":
                creadoAsistente=0
                obtener_texto(text)
                break     
              if text.lower() == "stop":
                play_audio("ok")
                continue   
  #            if text.lower() == "enciende la luz del comedor":
  #              creadoAsistente=0
  #              play_audio("enciendo el comedor")
  #              ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
  #              dato="c1"
  #              ser.write(dato.encode('utf-8'))
  #              ser.close()
  #              continue  
  #            if text.lower() == "apaga la luz del comedor":
  #              creadoAsistente=0
  #              play_audio("apago el comedor")
  #              ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
  #              dato="c0"
  #              ser.write(dato.encode('utf-8'))
  #              ser.close()
  #              continue                    
              if text.lower() == "hola lara":
                play_audio("Hola, en que puedo ayudarte.")
                creadoAsistente=1
                continue
              elif creadoAsistente==1:
                obtener_texto(text)                   
