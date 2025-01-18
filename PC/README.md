# ServerIA - Proyecto Cesarhch/Asistente

ServerIA es un sistema integral diseñado para gestionar dispositivos IoT y realizar inferencias de modelos de lenguaje avanzados de manera local. Este proyecto combina hardware optimizado para el ahorro energético y un software sofisticado con capacidades de reconocimiento de voz, gestión de bases de datos vectoriales y comunicación en tiempo real.

---

## Contenidos del proyecto

### Archivos principales


1. **`datoscasa2.txt`**
   - Archivo con datos de ejemplo sobre monitorización ambiental y detección de presencia en habitaciones.
   - Formato ideal para pruebas con modelos de lenguaje y consultas personalizadas.

2. **`tecnico.txt`**
   - Describe las funciones y roles del asistente técnico (Lara), incluyendo:
     - Respuestas breves y precisas.
     - Gestión de datos ambientales y detección de eventos (e.g., presencia, temperatura).
     - Referencias a proyectos principales como "sistema operativo con IA" y "diseño electrónico bajo consumo".

3. **`managment.txt`**
   - Incluye datos organizativos y recordatorios:
     - Citas importantes.
     - Notificaciones de correos electrónicos relacionados con presentaciones técnicas y temarios educativos.

4. **Código Python**
   - **`agentetecnico.py`**: Implementa el asistente técnico con funciones de inferencia y comunicación basada en texto y voz.
   - **`agentelocal.py`**: Gestiona las interacciones locales con dispositivos IoT y modelos de lenguaje.
   - **`interfaz.py`**: Crea una interfaz para gestionar y supervisar los dispositivos conectados al sistema.
   - **`terminartodo.py`**: Finaliza todas las operaciones activas, asegurando una gestión segura de recursos.
   - **`hardware.py`**: Controla y supervisa los elementos físicos como sensores, relés y temporizadores.
   - **`funciones.py`**: Reúne funciones auxiliares y utilidades para soporte del sistema principal.
   - **`contexto.py`**: Define configuraciones de contexto, como rutas para bases de datos y modelos de lenguaje.
   - **`agentmanager.py`**: Coordina las interacciones entre diferentes agentes y recursos.
   - **`voz.py`**: Gestiona el reconocimiento y síntesis de voz utilizando motores como gTTS y pyttsx3.
   - **`main.py`**: Punto de entrada principal del sistema.
   - **`reconocimiento.py`**: Implementa el análisis y discriminación de voces.

---

## Instalación

### Requisitos previos
- **Hardware**:
  - ESP32 con soporte para NodeMCU.
  - Sensores DHT11.
  - TPL5110 y componentes asociados (MOSFET, condensadores, etc.).
- **Para manejo de modelos de lenguaje local (Phi-3):**
  - Procesador: CPU de al menos 8 núcleos o GPU NVIDIA RTX 4060 Ti o superior.
  - Memoria RAM: 16 GB como mínimo (32 GB recomendados).
  - Almacenamiento: SSD con al menos 20 GB de espacio libre.
  - Sistema operativo: Linux (Debian recomendado) con soporte para drivers CUDA (si se utiliza GPU).
- **Software**:
  - Python 3.8+.
  - Bibliotecas necesarias: `langchain`, `gTTS`, `pyttsx3`, `serial`, entre otras.

### Configuración inicial
1. Clona el repositorio:
   ```bash
   git clone https://github.com/cesarhch/asistente.git
   cd asistente
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura los modelos de lenguaje:
   - Define las rutas para bases de datos locales y remotas en el archivo `contexto.py`.
   - Agrega tus tokens de HuggingFace en `modelos.py`.

4. Conecta los dispositivos:
   - Sigue el esquema de conexiones descrito en la documentación técnica.

---

## Uso

1. **Iniciar el sistema**:
   ```bash
   python main.py
   ```

2. **Comandos disponibles**:
   - Consultas sobre estado ambiental:
     - `¿Cuál es la temperatura actual?`
     - `¿Qué humedad hay en la habitación principal?`
   - Control de dispositivos IoT:
     - `enciende la luz del comedor`.
     - `apaga la luz del comedor`.
   - Interacción por voz:
     - Reconocimiento y respuesta a comandos hablados.

---

## Funcionalidades avanzadas

1. **Inferencia con modelos de lenguaje**:
   - Respuesta a preguntas utilizando bases de datos vectoriales y modelos locales.

2. **Reconocimiento de voz**:
   - Identificación y discriminación de comandos hablados para diferentes usuarios.

3. **Gestión de energía**:
   - Control de consumo mediante temporizadores y componentes de baja potencia.

---

## Créditos

- **Desarrollador principal**: Cesar (Infootec.net).
- **Asistente**: Lara.

---

## Licencia

Este proyecto está distribuido bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
