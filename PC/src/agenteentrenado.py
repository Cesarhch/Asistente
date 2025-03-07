import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
from contexto import Contexto  # Importar el contexto global
import funcionagente  # Importar todas las funciones disponibles
import re  # Importar regex para filtrar funciones

#  Rutas del modelo base y modelo fine-tuneado
base_model_path = r"C:/Phi-3-mini-4k-instruct"
finetuned_model_path = r"D:/finetuned_phi3"

#  Cargar el tokenizador
tokenizer = AutoTokenizer.from_pretrained(base_model_path)

#  Configurar Offload para ahorrar VRAM si es necesario
offload_dir = "C:/finetuned_phi3/offload"

#  Configuración de cuantización (para ejecutar en GPU con menos VRAM)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

#  Cargar el modelo base con cuantización
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    torch_dtype=torch.float16,
    device_map="auto",
    quantization_config=bnb_config
)

#  Cargar los pesos fine-tuneados
model = PeftModel.from_pretrained(
    base_model,
    finetuned_model_path,
    device_map="auto",
    offload_folder=offload_dir
)

# Verificar si el modelo está usando los pesos fine-tuneados
print(" Modelo cargado con éxito:")
print(f"Base Model: {base_model_path}")
print(f"Fine-tuned Model: {finetuned_model_path}")

def extraer_primera_funcion(respuesta: str):
    """ Extrae el nombre de la primera función dentro de <call_function> y descarta el resto del texto """
    match = re.search(r"<call_function>([^<]*)", respuesta)
    if match:
        funcion = match.group(1).strip()
        funcion = re.sub(r"[()\s]", "", funcion)  # Eliminar paréntesis y espacios extra
        print(f" Función extraída: {funcion}")  # Depuración
        return funcion
    return None

def generar_respuesta(prompt: str):
    #print(f" Prompt enviado al modelo:\n{prompt}")  # Depuración
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

    output = model.generate(
        **inputs,
        max_length=100,
        do_sample=True,  # Activar sampling para evitar advertencias
        temperature=0.7,  # Ajustar temperatura para variabilidad
        top_p=0.9,  # Ajustar top-p para muestreo
        early_stopping=True,
        num_beams=5  # Reducir el número de beams
    )

    respuesta = tokenizer.decode(output[0], skip_special_tokens=True).strip()
    print(f" Respuesta generada: {respuesta}")  # Depuración
    
    # Extraer solo la primera función dentro de <call_function> y descartar el resto del texto
    funcion_nombre = extraer_primera_funcion(respuesta)
    
    if funcion_nombre:
        return funcionagente.recogerfuncion(funcion_nombre)
    
    # Si la respuesta está vacía o no contiene función válida, llamar a la función modelo()
    print(" No se encontró una función válida, llamando a modelo().")
    return funcionagente.modelo()
