import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, BitsAndBytesConfig, DataCollatorForSeq2Seq
from peft import LoraConfig, get_peft_model
from datasets import load_dataset

# ✅ 1️⃣ Liberar Memoria Antes de Cargar el Modelo
torch.cuda.empty_cache()
torch.cuda.reset_peak_memory_stats()

# 📂 Ruta del modelo base (Phi-3-mini-4k-instruct)
model_path = "D:/Phi-3-mini-4k-instruct"

# ✅ 2️⃣ Cuantización en 4-bit con `float32`
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float32,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

# 📥 Cargar el modelo con 4-bit y optimización de memoria
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map="auto",
    quantization_config=bnb_config,
    torch_dtype=torch.float32 
)

# 📥 Cargar el tokenizador
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

# 🔹 **Asegurar que `use_cache=False`**
model.config.use_cache = False  

# ✅ 3️⃣ Configurar LoRA con los módulos correctos de Phi-3-mini-4k
lora_config = LoraConfig(
    r=8, 
    lora_alpha=32, 
    lora_dropout=0.1, #Dato de aleatoriedad, antes en 0.05 
    bias="none", 
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],  
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)

# ✅ Habilitar `gradient_checkpointing` para ahorro de memoria
model.gradient_checkpointing_disable()

# ✅ 4️⃣ Asegurar que solo los parámetros de LoRA sean entrenables
for param in model.parameters():
    param.requires_grad = False  

# 🔹 Activar solo los parámetros de LoRA
for name, param in model.named_parameters():
    if "lora" in name or "adapter" in name:
        param.requires_grad = True

# 🔥 Asegurar que el modelo esté en modo entrenamiento
model.train()

# 🚀 Verificar si hay parámetros entrenables
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
total_params = sum(p.numel() for p in model.parameters())
print(f"🔍 Parámetros entrenables: {trainable_params} / {total_params}")

if trainable_params == 0:
    raise ValueError("❌ ERROR: No hay parámetros entrenables en el modelo.")

print(f"✅ Modelo cargado en: {model.device}")

# 📂 Cargar dataset JSONL
dataset_path = r"D:/serveria/Asistente-main/Finetuning/dataset.jsonl"
dataset = load_dataset("json", data_files=dataset_path)["train"]

# 🔍 Verificar estructura del dataset antes de tokenizar
print("Ejemplo de dataset antes de tokenizar:", dataset[0])

# 🔠 Función de Tokenización con Labels
def tokenize_function(examples):
    if "prompt" not in examples or "completion" not in examples:
        raise ValueError("❌ Error: El dataset no tiene los campos 'prompt' y 'completion'.")

    combined_texts = [p + " " + c for p, c in zip(examples["prompt"], examples["completion"]) if p and c]
    
    if not combined_texts:
        raise ValueError("❌ Error: Algunos ejemplos en el dataset están vacíos o mal formateados.")

    tokenized = tokenizer(combined_texts, truncation=True, padding="max_length", max_length=100)
    
    # ✅ Agregar labels (necesarios para calcular loss)
    tokenized["labels"] = tokenized["input_ids"].copy()
    
    return tokenized

# 📌 Tokenizar dataset
tokenized_dataset = dataset.map(tokenize_function, batched=True)

# ⚙️ 5️⃣ Configuración del Entrenamiento Optimizado
training_args = TrainingArguments(
    output_dir="D:/finetuned_phi3",
    per_device_train_batch_size=2,  
    gradient_accumulation_steps=4,  
    save_strategy="epoch",
    save_steps=50,
    logging_dir="D:/logs",
    logging_steps=5,
    max_steps=500,  
    fp16=True,
    evaluation_strategy="no",
    push_to_hub=False,
    learning_rate=5e-5  # 🔹 Ajustado para mejor precisión
    #learning_rate=1e-4
)

# 🔹 **Añadir `data_collator` optimizado**
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model, padding="longest")

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator  
)

# 🚀 Iniciar el Fine-Tuning
trainer.train()

# 📥 Guardar el modelo fine-tuneado
save_path = "D:/finetuned_phi3"
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

print(f"✅ Modelo fine-tuneado guardado en: {save_path}")
