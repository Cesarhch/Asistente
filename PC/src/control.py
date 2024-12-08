from tkinter import *
from voz import play_audio
from funciones import save_cesar
import vosk
import pyaudio
import threading
import json 
import serial
import subprocess
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

# Ejecutar el segundo código en un subshell
subprocess.Popen(["python3", "datostxt.py"])

local_path = "datoscasa2.txt"

# Local .txt file uploads
if local_path:
    loader = TextLoader(file_path=local_path)  # Use TextFileLoader for .txt
    data = loader.load()  # Load with explicit encoding
else:
    print("Upload a .txt file")
# Split and chunk 
text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
chunks = text_splitter.split_documents(data)

# Define a persistent collection name (avoid deletion after each interaction)
collection_name = "local-rag"
custom_db_directory = "/Users/cesarhernandez/Documents/PlatformIO/Projects/RAG-1/prueba2"


vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=OllamaEmbeddings(model="phi3", show_progress=False),
    collection_name=collection_name,
    persist_directory=custom_db_directory
)

# LLM from Ollama
local_model = "phi3"
llm = ChatOllama(model=local_model)

QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""Eres una asistente y te llamas Lara. 
    Pregunta original: {question}""",
)

retriever = MultiQueryRetriever.from_llm(
    vector_db.as_retriever(),
    llm,
    prompt=QUERY_PROMPT
)

# RAG prompt
template = """Debes de responder a cualquier pregunta:
{context}
Pregunta: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def record_audio():
    model=vosk.Model(r"/Users/cesarhernandez/Desktop/cesar/Infootec/Mypython/vosk-model-small-es-0.42")
    recognizer = vosk.KaldiRecognizer(model, 16000)
    creadoAsistente=0
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
    stream.start_stream()
    while True:
        data = stream.read(2048, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            text=recognizer.Result()
            try:
              text = json.loads(text)['text']
            except KeyError:
              continue
            if not text:
              print(text)
              continue
            if text.lower() == "salir":
              creadoAsistente=0 
              play_audio("adios")
              continue
            if text.lower() == "terminar micro":
              creadoAsistente=0
              play_audio("cierro micro") 
              stream.stop_stream()
              stream.close()
              mic.terminate()
              break 
            if text.lower() == "terminar todo":
              creadoAsistente=0
              play_audio("cierro todo")
              stream.stop_stream()
              stream.close()
              mic.terminate()
              ventana.destroy()
              break     
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
              play_audio(("Hola, en que puedo ayudarte."))
              creadoAsistente=1
              continue
            elif creadoAsistente==1:
              obtener_texto(text)                   

def mostrar_ventana():
    global entrada
    global ventana
    ventana = Tk()
    ventana.geometry("+%d+%d" % (ventana.winfo_screenwidth() - 300, 0))
    ventana.title("Lara")

    # Crear un widget de entrada de texto
    entrada = Entry(ventana)
    entrada.pack()
    entrada.bind('<Return>', obtener_texto)
    # Crear un botón para obtener el texto
    boton = Button(ventana, text="Obtener texto", command=obtener_texto)
    boton.pack()
    return ventana

def obtener_texto(texto_introducido):
  texto_introducido_ventana = entrada.get()
  if texto_introducido_ventana.strip():  
    texto_introducido = texto_introducido_ventana
    entrada.delete(0, END)
  if texto_introducido_ventana.lower() == "terminar ventana":
    play_audio("adios")
    ventana.destroy() 
  if texto_introducido_ventana.lower().startswith("escribir datos "):
    phrase_to_remember = texto_introducido_ventana[len("escribir datos "):].strip()
    save_cesar(phrase_to_remember)
    play_audio("Información guardada, " + phrase_to_remember)
    entrada.delete(0, END)
    return
  if texto_introducido_ventana.lower() == "enciende la luz del comedor":
    play_audio("enciendo el comedor")
    ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
    dato="c1"
    ser.write(dato.encode('utf-8'))
    ser.close()  
    entrada.delete(0, END)
    return
  if texto_introducido_ventana.lower() == "apaga la luz del comedor":
    play_audio("apago el comedor")
    ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
    dato="c0"
    ser.write(dato.encode('utf-8'))
    ser.close()
    entrada.delete(0, END)
    return
  else:
    resultado = chain.invoke(texto_introducido)
    print(resultado)
    respuesta=resultado
    if respuesta.lower() == " encender comedor":
      play_audio(respuesta)
      ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
      dato="c1"
      ser.write(dato.encode('utf-8'))
      ser.close()
      return
    if respuesta.lower() == " apagar comedor":
      play_audio(respuesta)
      ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
      dato="c0"
      ser.write(dato.encode('utf-8'))
      ser.close()
      return
    if respuesta.lower() == " encender cocina":
      play_audio(respuesta)
      ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
      dato="ci1"
      ser.write(dato.encode())
      ser.close()
    if respuesta.lower() == " apagar cocina":
      play_audio(respuesta)
      ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
      dato="ci0"
      ser.write(dato.encode())
      ser.close()
    if respuesta.lower() == " encender electrovalvula":
      play_audio(respuesta)
      ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
      dato="v1"
      ser.write(dato.encode())
      ser.close()
    if respuesta.lower() == " apagar electrovalvula":
      play_audio(respuesta)
      ser = serial.Serial('/dev/tty.usbserial-0001', 9600)
      dato="v0"
      ser.write(dato.encode())
      ser.close()
    play_audio(respuesta)
    entrada.delete(0, END)
    return

def main():
    # Se inicia la grabación de audio en una función separada
    record_audio_thread = threading.Thread(target=record_audio)
    
    record_audio_thread.start()
    
    ventana=mostrar_ventana()
    ventana.mainloop()  
if __name__ == "__main__":

    main()
