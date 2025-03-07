from langchain_community.llms import HuggingFaceHub, HuggingFaceEndpoint
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_community.document_loaders import TextLoader
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.schema import HumanMessage
from unidecode import unidecode
from funciones import contar_archivos_en_directorio


# Configuración del modelo local (Ollama)
def consultar_agente_tecnico(pregunta):

    # Verificar si la pregunta solicita conteo de archivos
    # pregunta = "cuantos archivos hay en el directorio documentos"
    
    if "archivos" in unidecode(pregunta.lower()):
        # Extraer el nombre del directorio de la pregunta (puedes ajustar el parseo)
        palabras = pregunta.split()
        indice_directorio = palabras.index("en") + 1 if "en" in palabras else -1
        if indice_directorio != -1 and indice_directorio < len(palabras):
            directorio = palabras[indice_directorio]
            return contar_archivos_en_directorio(directorio)
        else:
            return "Por favor, especifica un directorio para contar los archivos."

    llm_local = ChatOllama(model="deepseek-r1:7b")
    local_path="C:/ruta/rag/tecnico.txt"
    collection_name="tecnico-rag"
    custom_db_directory="C:/ruta/rag/tecnico"
    loader = TextLoader(file_path=local_path)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
    chunks = text_splitter.split_documents(data)

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=OllamaEmbeddings(model="phi3"),
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
    documentos = retriever.invoke(pregunta)
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

