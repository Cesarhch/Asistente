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

def configurar_modelo_remoto(question):
    
    #Configura el modelo remoto usando HuggingFaceEndpoint.
    #Returns:
    #    chain_remote: Cadena para ejecutar el modelo remoto.
    
    llm_remote = HuggingFaceEndpoint(
    endpoint_url="https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct",
    huggingfacehub_api_token="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_",
    temperature=0.8,  # Ajuste para respuestas más variadas
    top_k=100,
    top_p=0.9,
    model_kwargs={
        "max_length": 1000  # Mover aquí para eliminar la advertencia
        }
    )

    prompt_remote = PromptTemplate(
      input_variables=["question"],
      template=(
        "Responde a la siguiente pregunta de manera clara y breve.\n\n"
        "Pregunta: {question}\n"
        "Respuesta:"
      )
    )

    chain_remote = prompt_remote | llm_remote  # Uso de RunnableSequence
    return chain_remote

#Aqui empieza el modelo local

# Configuración del modelo local (Ollama)
def consultar_modelo_local(pregunta):
    
    llm_local = ChatOllama(model="phi3")
    local_path="/Users/cesarhernandez/Documents/PlatformIO/Projects/server_IA/rag/managment.txt"
    collection_name="managment-rag"
    custom_db_directory="/Users/cesarhernandez/Documents/PlatformIO/Projects/server_IA/rag/managment"
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
        HumanMessage(content="""Eres una asistente y te llamas Lara. 
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

