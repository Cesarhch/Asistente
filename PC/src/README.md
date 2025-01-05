# Proyecto: Sistema Operativo con IA y Electrónica

Este proyecto combina inteligencia artificial, diseño electrónico y control de hardware utilizando un sistema operativo basado en Linux. Aquí se describen los archivos principales y sus funciones.

## Archivos principales

### 1. `funciones.py`
- **Descripción:** Contiene funciones auxiliares, como `save_cesar`, que guarda información en un archivo de texto.
- **Propósito:** Gestión de almacenamiento local para datos relevantes.

---

### 2. `ESP32yTPL5110.pdf`
- **Descripción:** Documento técnico que describe un circuito de bajo consumo basado en la ESP32, un temporizador TPL5110, y un sensor DHT11.
- **Propósito:** Diseño de un sistema autónomo alimentado por energía solar para medir y transmitir datos ambientales.

---

### 3. `reconocimiento.py`
- **Descripción:** Implementa reconocimiento de voz utilizando el modelo Vosk.
- **Funciones principales:**
  - `record_audio`: Captura audio, reconoce comandos de voz y ejecuta acciones específicas, como encender/apagar luces o cerrar ventanas.
- **Propósito:** Control por voz de dispositivos y funciones del sistema.

---

### 4. `agentmanager.py`
- **Descripción:** Gestiona consultas al agente de inteligencia artificial.
- **Funciones principales:**
  - `responder_agente_managment`: Responde preguntas utilizando un modelo RAG (retrieval-augmented generation).
- **Propósito:** Procesamiento de preguntas mediante modelos de lenguaje.

---

### 5. `hardware.py`
- **Descripción:** Contiene funciones para la interacción con hardware mediante comunicación serie.
- **Funciones principales:**
  - `obtener_texto`: Interpreta comandos y ejecuta acciones como el control de luces y válvulas electrónicas.
- **Propósito:** Interacción directa con hardware externo.

---

### 6. `modelos.py`
- **Descripción:** Configura modelos de lenguaje remoto y local.
- **Funciones principales:**
  - `configurar_modelo_remoto`: Configura un modelo alojado en Hugging Face para respuestas a preguntas.
  - `consultar_modelo_local`: Usa un modelo local basado en Phi3 para preguntas relacionadas con una base de datos vectorial.
- **Propósito:** Proporcionar capacidades de procesamiento de lenguaje natural.

---

### 7. `voz.py`
- **Descripción:** Convierte texto a voz y lo reproduce.
- **Funciones principales:**
  - `play_audio`: Genera audio usando gTTS o pyttsx3 como respaldo.
- **Propósito:** Comunicación auditiva con el usuario.

---

### 8. `main.py`
- **Descripción:** Punto de entrada del programa.
- **Funciones principales:**
  - Inicia la grabación de audio y muestra una interfaz gráfica para la interacción.
- **Propósito:** Coordinación general del sistema.

---

### 9. `interfaz.py`
- **Descripción:** Proporciona una interfaz gráfica básica para interactuar con el sistema.
- **Funciones principales:**
  - `mostrar_ventana`: Crea una ventana con entrada de texto y botones para procesar comandos.
- **Propósito:** Interacción visual con el usuario.

---

### 10. `managment.txt`
- **Descripción:** Documento de configuración para el agente de inteligencia artificial.
- **Contenido relevante:**
  - Define el nombre del agente como "Lara".
  - Especifica proyectos asociados, como un sistema operativo con IA y diseño de electrónica de bajo consumo.
- **Propósito:** Documentación y configuración del agente.

---

## Resumen del Proyecto
Este sistema combina la funcionalidad de un modelo de lenguaje para responder preguntas y ejecutar comandos, con capacidades de control de hardware y reconocimiento de voz. Además, incluye un diseño electrónico optimizado para bajo consumo, ideal para aplicaciones IoT y autónomas.

## Requisitos
- **Hardware:**
  - ESP32.
  - TPL5110.
  - Sensor DHT11.
  - Paneles solares y batería Li-ion.
- **Software:**
  - Python 3.9 o superior.
  - Librerías: `vosk`, `pyaudio`, `gTTS`, `pyttsx3`, `langchain`.

---

## Uso
1. Ejecutar `main.py` para iniciar el sistema.
2. Interactuar con la interfaz gráfica o mediante comandos de voz.
3. Monitorear y controlar dispositivos electrónicos conectados al sistema.

## Contribución
Se aceptan mejoras en las áreas de:
- Optimización del reconocimiento de voz.
- Integración de nuevos sensores o dispositivos IoT.
- Extensión de la funcionalidad del modelo de lenguaje.

---
