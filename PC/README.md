# Proyecto: Sistema Operativo con IA y Electrónica

Este repositorio contiene múltiples scripts y archivos relacionados con el desarrollo de un sistema operativo orientado a la interacción con inteligencia artificial y hardware electrónico, basado en Linux y dispositivos IoT.

## Contenido del Repositorio

### Documentación y Esquemas

- **ESP32yTPL5110.pdf**: Descripción detallada de un circuito para medir temperatura y humedad con un sensor DHT11 y una ESP32. Incluye detalles del diseño eléctrico, componentes utilizados y conexiones. El circuito utiliza una tarjeta TPL5110 para bajo consumo y se alimenta con paneles solares y supercondensadores【20†source】.

### Código Fuente

- **main.py**: Script principal que inicializa la aplicación. Controla la interfaz gráfica y la grabación de audio mediante hilos【21†source】.

- **agentmanager.py**: Gestiona las consultas dirigidas a diferentes agentes, seleccionando entre un modelo local o técnico según el contexto del usuario【22†source】.

- **agentelocal.py**: Configura y ejecuta un modelo de lenguaje local utilizando LangChain y Phi-3【23†source】.

- **agentetecnico.py**: Configura y ejecuta un modelo técnico local. También incluye una funcionalidad para contar archivos en directorios específicos【31†source】.

- **reconocimiento.py**: Implementa el reconocimiento de voz utilizando el modelo Vosk. Permite la interacción mediante comandos hablados y la conexión con otros módulos del sistema【24†source】.

- **terminartodo.py**: Maneja el cierre completo del sistema, incluyendo la terminación de procesos y la limpieza de bases de datos【25†source】.

- **contexto.py**: Define el contexto global de la aplicación, incluyendo variables compartidas entre módulos【26†source】.

- **hardware.py**: Proporciona funcionalidades para interactuar con el hardware, como encender/apagar luces y ejecutar modelos remotos o locales【27†source】.

- **funciones.py**: Contiene utilidades como limpieza de texto y guardado de información en archivos【28†source】.

- **interfaz.py**: Implementa la interfaz gráfica con Tkinter, permitiendo la entrada y procesamiento de texto【30†source】.

- **voz.py**: Convierte texto a voz utilizando gTTS y maneja la reproducción de audio en segundo plano【32†source】.

### Archivos de Configuración y Datos

- **datoscasa2.txt**: Archivo de texto que almacena información personalizada sobre el usuario y el asistente【29†source】.

- **tecnico.txt**: Archivo utilizado por el modelo técnico, que contiene datos específicos del entorno y proyectos del usuario【33†source】.

- **managment.txt**: Archivo utilizado por el modelo de gestión, que incluye información como correos y citas del usuario【34†source】.

## Cómo Empezar

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   ```

2. Asegúrate de tener instaladas las dependencias necesarias, como `vosk`, `gTTS`, y `LangChain`.

3. Ejecuta el script principal:
   ```bash
   python main.py
   ```

## Requisitos

- Python 3.8 o superior
- Librerías:
  - `vosk`
  - `pyaudio`
  - `LangChain`
  - `gTTS`

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.
