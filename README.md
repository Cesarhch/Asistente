# Asistente con ESP32 y Python

Este proyecto combina el uso de dispositivos ESP32 y scripts en Python para crear un sistema integrado que recolecta datos de sensores, los procesa y almacena, proporcionando además interacción y visualización en una computadora personal.

## Estructura del Proyecto

El proyecto está organizado en varios módulos independientes, cada uno con un propósito específico:

### Directorios Principales

- **ESP32_HCSR501_1/**
  - **Descripción:** Módulo que interactúa con el sensor HCSR501 para detección de movimiento.
  - **Contenido:**
    - `src/main.cpp`: Código fuente del módulo.
    - `platformio.ini`: Archivo de configuración de PlatformIO.

- **ESP32_central/**
  - **Descripción:** Módulo central que utiliza una tarjeta Olimex ESP32-EVB para recibir datos de otros dispositivos ESP32 mediante ESP-NOW, procesarlos y almacenarlos en una tarjeta SD.
  - **Contenido:**
    - `src/main.cpp`: Código fuente del módulo.
    - `platformio.ini`: Archivo de configuración de PlatformIO.

- **ESP32_ext_DHT11/**
  - **Descripción:** Módulo que recolecta datos de temperatura y humedad utilizando el sensor DHT11 y los envía al módulo central.
  - **Contenido:**
    - `src/main.cpp`: Código fuente del módulo.
    - `platformio.ini`: Archivo de configuración de PlatformIO.

- **PC/**
  - **Descripción:** Scripts en Python para procesar, analizar o visualizar los datos recolectados por los ESP32.
  - **Contenido:**
    - `src/main.py`: Script principal.
    - `requirements.txt`: Dependencias necesarias para ejecutar el script en Python.

## Requisitos

### Hardware
- Mínimo 2 dispositivos ESP32 (incluyendo una Olimex ESP32-EVB para la central).
- Sensores compatibles (HCSR501, DHT11).
- Tarjeta SD y módulo de lectura/escritura para ESP32.
- Computadora personal con Python 3.x instalado.

### Software
- [PlatformIO](https://platformio.org/) para programar los ESP32.
- Python 3.x y las dependencias listadas en `requirements.txt`.

## Instalación y Configuración

### Configurar los ESP32
1. Clona este repositorio:
   ```bash
   git clone https://github.com/Cesarhch/Asistente.git
   ```

2. Configura cada módulo ESP32:
   - Abre el código correspondiente en PlatformIO.
   - Ajusta los parámetros necesarios (p. ej., pines de sensores, configuración de WiFi o ESP-NOW).
   - Sube el código al ESP32 mediante USB.

3. Conecta los sensores y verifica el funcionamiento.

### Configurar la Computadora Personal
1. Instala las dependencias de Python:
   ```bash
   pip install -r PC/requirements.txt
   ```

2. Ejecuta el script principal:
   ```bash
   python PC/src/main.py
   ```

## Uso

1. **Inicia los módulos ESP32:**
   - Asegúrte de que los dispositivos estén encendidos y correctamente configurados.

2. **Recolecta y almacena datos:**
   - Los módulos ESP32 recolectarán datos de los sensores y los enviarán al módulo central.
   - El módulo central almacenará los datos en una tarjeta SD.

3. **Procesa los datos en la PC:**
   - Ejecuta los scripts en Python para analizar o visualizar la información almacenada.

## Notas Adicionales

- **Depuración:** Utiliza `Serial Monitor` en PlatformIO para depurar los ESP32.
- **Seguridad:** Considera implementar autenticación o cifrado para proteger la comunicación entre módulos.

## Contribución

Si deseas contribuir a este proyecto, realiza un *fork* del repositorio, realiza tus cambios y envía un *pull request*. Toda ayuda es bienvenida.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---

Desarrollado por [Cesarhch](https://github.com/Cesarhch).

