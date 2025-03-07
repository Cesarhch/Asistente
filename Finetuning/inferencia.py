import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

# 📂 Rutas del modelo base y modelo fine-tuneado
base_model_path = r"D:/Phi-3-mini-4k-instruct"  # Ruta del modelo base original
finetuned_model_path = r"D:/finetuned_phi3"     # Ruta del modelo fine-tuneado

# 📥 Cargar el tokenizador
tokenizer = AutoTokenizer.from_pretrained(base_model_path)

# 📂 Configurar Offload para ahorrar VRAM si es necesario
offload_dir = "D:/finetuned_phi3/offload"

# 🚀 Configuración de cuantización (para ejecutar en GPU con menos VRAM)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

# 📥 Cargar el modelo base con cuantización
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    torch_dtype=torch.float16,
    device_map="auto",
    quantization_config=bnb_config
)

# 📥 Cargar los pesos fine-tuneados
model = PeftModel.from_pretrained(
    base_model,
    finetuned_model_path,
    device_map="auto",
    offload_folder=offload_dir
)

# 🚀 Loop interactivo para hacer preguntas
while True:
    prompt = input("📝 Ingresa tu pregunta (o escribe 'salir' para terminar): ")
    if prompt.lower() == "salir":
        break
    
    formatted_prompt = f"Pregunta: {prompt}\nRespuesta: "
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to("cuda")

    output = model.generate(
        **inputs,
        max_length=100,
        do_sample=False, 
        temperature=0.1,
        top_p=0.1,
        early_stopping=True,
        num_beams=10
    )

    respuesta = tokenizer.decode(output[0], skip_special_tokens=True).strip()
    print(f"🧠 Respuesta: {respuesta}\n")
