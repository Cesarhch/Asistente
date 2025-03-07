from memoria import BaseDatos
from chromadb import Client, Settings

class Contexto:
    retriever = None  # Almacena el recuperador de información para búsquedas en bases de datos vectoriales.
    vectorstore = None  # Guarda la base de datos vectorial donde se almacenan embeddings.
    llm = None  # Instancia del modelo de lenguaje que se usará para la inferencia.
    chroma_client = None  # Cliente para interactuar con la base de datos vectorial ChromaDB.
    ventana = None  # Referencia a la ventana de la interfaz gráfica (Tkinter o similar).
    mic = None  # Controla el acceso al micrófono para reconocimiento de voz.
    stream = None  # Variable para manejar el flujo de audio en tiempo real.
    audio_thread = None  # Hilo dedicado a la reproducción de audio en segundo plano.
    stop_audio = None  # Evento utilizado para detener la reproducción de audio.
    creadoAsistente = 0  # Indica qué asistente está activo (ejemplo: 1 = agente local, 2 = técnico).
    
    db = BaseDatos()  # Instancia de la base de datos de memoria para almacenar interacciones pasadas.
    chroma_client = Client(Settings(allow_reset=True))  # Cliente para la base de datos vectorial ChromaDB.
    
    db_borrada = False  # Indica si la base de datos ha sido eliminada (evita eliminaciones múltiples).

    memoriaCorta = None  # Guarda la información temporal de varias inferencias, útil para el contexto inmediato.
    prompt = None  # Contiene la última entrada del usuario, utilizada para decidir qué agente manejará la respuesta.
