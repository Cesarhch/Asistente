from langchain_community.llms import HuggingFaceHub, HuggingFaceEndpoint
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.schema import HumanMessage
from contexto import Contexto
import shutil
import os

# Configuración del modelo local (Ollama)
def consultar_modelo_local(pregunta):
    # Guardar referencias globales para cerrarlas después
    Contexto.llm = ChatOllama(model="phi4")

    # Directorio donde se guardará la base de datos
    base_path = "D:/serveria/Asistente-main/PC/src/rag/"
    collection_name = "managment"
    chroma_db_path = os.path.join(base_path, "chroma_db")  #  Asegura un subdirectorio

    #  1. CREAR EL DIRECTORIO SI NO EXISTE
    os.makedirs(chroma_db_path, exist_ok=True)

    #  2. ELIMINAR BASES DE DATOS FUERA DE `rag/`
    if os.path.exists("chroma.sqlite3"):
        os.remove("chroma.sqlite3")
        #print(" Eliminando base de datos creada fuera del directorio correcto.")

    #  3. ELIMINAR BASES DE DATOS CON UUID
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path) and "-" in folder:  # Si contiene "-" (UUID)
            shutil.rmtree(folder_path)
            #print(f" Eliminando base de datos con UUID: {folder_path}")

    #  4. VERIFICAR SI LA BASE YA EXISTE
    if os.path.exists(os.path.join(chroma_db_path, "chroma.sqlite3")):
        #print(f" Cargando base de datos existente: {collection_name}")
        Contexto.vectorstore = Chroma(
            collection_name=collection_name,
            persist_directory=chroma_db_path,  #  Asegurar que usa `rag/chroma_db`
            embedding_function=OllamaEmbeddings(model="phi3")
        )
    else:
        print(" Base de datos no encontrada. Creando una nueva...")

        # Archivos de datos
        archivos = [
            os.path.join(base_path, "managment.txt"),
            os.path.join(base_path, "conocimiento.txt")
        ]

        # Cargar documentos
        documentos = []
        for archivo in archivos:
            if os.path.exists(archivo):
                loader = TextLoader(file_path=archivo)
                documentos.extend(loader.load())

        # Dividir en fragmentos para indexar
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
        chunks = text_splitter.split_documents(documentos)

        #  5. CREAR LA BASE DE DATOS FORZANDO EL NOMBRE "managment"
        Contexto.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=OllamaEmbeddings(model="phi3"),
            collection_name=collection_name,  #  Asegurar el nombre correcto
            persist_directory=chroma_db_path  #  Forzar la ubicación en `rag/chroma_db`
        )

    QUERY_PROMPT = ChatPromptTemplate.from_messages([
        HumanMessage(content="""Responde de forma directa, breve y concisa a la última pregunta realizada. 
        Pregunta: {question}""")
    ])

    # Guardar la referencia del retriever globalmente
    Contexto.retriever = MultiQueryRetriever.from_llm(
        Contexto.vectorstore.as_retriever(),
        Contexto.llm,
        prompt=QUERY_PROMPT
    )

    # Recuperar documentos relevantes
    documentos = Contexto.retriever.invoke(pregunta)
    if not documentos:
        return "No se encontraron documentos relevantes para esta consulta."

    contexto = "\n".join([doc.page_content for doc in documentos])

    # Construir el prompt final
    template = """Contexto: {context}
    Pregunta: {question}
    """

    prompt_content = template.format(context=contexto, question=pregunta)

    prompt = ChatPromptTemplate.from_messages([
        HumanMessage(content=prompt_content)
    ])

    chain = (
        {"context": Contexto.retriever, "question": RunnablePassthrough()}
        | prompt
        | Contexto.llm
        | StrOutputParser()
    )

    respuesta = chain.invoke({"question": pregunta})
    return respuesta
