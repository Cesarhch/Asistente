# Proyecto Lara: Sistema Operativo con IA y Diseño Electrónico de Bajo Consumo

Este proyecto combina tecnologías avanzadas de inteligencia artificial, diseño electrónico y programación en Python para crear un sistema operativo especializado. A continuación, se presenta una descripción detallada de los archivos incluidos:

## Estructura del Proyecto

### Archivos Principales

#### **1. `main.py`**
Archivo principal que inicializa la aplicación, gestiona la interfaz gráfica y coordina el flujo principal del programa.

#### **2. `agentmanager.py`**
Gestión del agente de manejo de tareas. Este módulo responde preguntas utilizando una base de datos vectorial y puede redirigir consultas a un agente técnico si es necesario.

#### **3. `modelos.py`**
Configura y gestiona los modelos de lenguaje locales y remotos. Utiliza `HuggingFaceEndpoint` para modelos remotos y Ollama para consultas locales.

#### **4. `funciones.py`**
Incluye funciones auxiliares, como la escritura de datos en archivos.

#### **5. `voz.py`**
Convierte texto a voz usando la biblioteca `gTTS` y maneja la reproducción de audio con la capacidad de detener audio en ejecución.

#### **6. `terminartodo.py`**
Gestiona el cierre completo del sistema, deteniendo procesos y eliminando bases de datos temporales.

#### **7. `interfaz.py`**
Crea y gestiona la interfaz gráfica usando `Tkinter`, incluyendo funciones para manejar entradas de texto y eventos.

#### **8. `contexto.py`**
Define una clase para manejar variables globales del programa, como la ventana, el micrófono y el hilo de audio.

#### **9. `reconocimiento.py`**
Implementa el reconocimiento de voz utilizando el modelo `vosk` para la transcripción y ejecución de comandos de voz.

### Otros Archivos

#### **`managment.txt`**
Incluye instrucciones básicas y definiciones relacionadas con el proyecto, como nombres de agentes y temas principales.

#### **`ESP32yTPL5110.pdf`**
Documento técnico que describe un circuito electrónico de bajo consumo basado en ESP32 y el temporizador TPL5110. Explica detalladamente el diseño y las conexiones eléctricas.

### Dependencias

El proyecto utiliza varias bibliotecas y herramientas, como:
- `gTTS` para conversión de texto a voz.
- `vosk` para reconocimiento de voz.
- `LangChain` para manejo de modelos de lenguaje.
- `Tkinter` para la interfaz gráfica.
- `pyaudio` para captura de audio.

### Instalación y Configuración
1. Clonar este repositorio.
2. Instalar las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configurar los modelos de lenguaje y bases de datos vectoriales siguiendo las instrucciones en `modelos.py`.

### Uso
1. Ejecutar `main.py` para iniciar el sistema.
   ```bash
   python main.py
   ```
2. Interactuar con la interfaz gráfica o mediante comandos de voz.

### Notas
- Este proyecto requiere configuraciones específicas para hardware externo, como el circuito basado en ESP32 descrito en `ESP32yTPL5110.pdf`.
- Es fundamental revisar las rutas y configuraciones en los archivos para garantizar su funcionamiento en el entorno deseado.

---

**Autor:** Lara AI System
**Propósito:** Desarrollo de un sistema operativo especializado con integración de IA y electrónica avanzada.
