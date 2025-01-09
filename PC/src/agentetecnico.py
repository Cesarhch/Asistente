from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama
from langchain.llms import HuggingFaceHub
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.schema import HumanMessage
import os
from unidecode import unidecode

def contar_archivos_en_directorio(directorio):
    #Cuenta los archivos en un directorio dado.
    directorio="/Users/cesarhernandez/Documents/PlatformIO/Projects"
    if not os.path.exists(directorio):
        return f"El directorio {directorio} no existe."
    
    if not os.path.isdir(directorio):
        return f"{directorio} no es un directorio válido."
    
    archivos = []
    carpetas = []

    # Clasificar elementos en archivos y carpetas
    for item in os.listdir(directorio):
        ruta_completa = os.path.join(directorio, item)
        if os.path.isfile(ruta_completa):
            archivos.append(item)
        elif os.path.isdir(ruta_completa):
            carpetas.append(item)

    # Crear la respuesta
    respuesta = (
        f"El directorio {directorio} contiene:\n"
        f"- {len(archivos)} archivos\n"
        f"- {len(carpetas)} carpetas\n"
    )

    if archivos:
        respuesta += "\nArchivos:\n" + "\n".join(archivos)
    if carpetas:
        respuesta += "\n\nCarpetas:\n" + "\n".join(carpetas)

    return respuesta

# Configuración del modelo local (Ollama)
def consultar_agente_tecnico(pregunta):

    # Verificar si la pregunta solicita conteo de archivos
    pregunta="cuantos archivos hay en el directorio documentos"
    
    if "archivos" in unidecode(pregunta.lower()):
        # Extraer el nombre del directorio de la pregunta (puedes ajustar el parseo)
        palabras = pregunta.split()
        indice_directorio = palabras.index("en") + 1 if "en" in palabras else -1
        if indice_directorio != -1 and indice_directorio < len(palabras):
            directorio = palabras[indice_directorio]
            return contar_archivos_en_directorio(directorio)
        else:
            return "Por favor, especifica un directorio para contar los archivos."

    llm_local = ChatOllama(model="phi3")
    local_path="/Users/cesarhernandez/Documents/PlatformIO/Projects/server_IA/rag/tecnico.txt"
    collection_name="tecnico-rag"
    custom_db_directory="/Users/cesarhernandez/Documents/PlatformIO/Projects/server_IA/rag/tecnico"
    loader = TextLoader(file_path=local_path)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
    chunks = text_splitter.split_documents(data)

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=OllamaEmbeddings(model="phi3", show_progress=False),
        collection_name=collection_name,
        persist_directory=custom_db_directory
    )
    
    QUERY_PROMPT = ChatPromptTemplate.from_messages([
        HumanMessage(content="""Eres una asistente y te llamas Agente Tecnico. 
        Pregunta: {question}""")
    ])
    retriever = MultiQueryRetriever.from_llm(
      vector_db.as_retriever(),
      llm_local,
      prompt=QUERY_PROMPT
    )
    
    # Configura el retriever
    #retriever = vector_db.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    # Recupera documentos relevantes
    documentos = retriever.get_relevant_documents(pregunta)
    if not documentos:
        return "No se encontraron documentos relevantes para esta consulta."

    contexto = "\n".join([doc.page_content for doc in documentos])

    # Construye el prompt
    template = """Contexto: {context}
    Pregunta: {question}
    """

    prompt_content = template.format(context=contexto, question=pregunta)
    
    prompt = ChatPromptTemplate.from_messages([
        HumanMessage(content=prompt_content)
    ])

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm_local
        | StrOutputParser()
    )
    respuesta = chain.invoke({"question": pregunta})
    return respuesta

