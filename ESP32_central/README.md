# Proyecto OLIMEX ESP32-EVB con ESP-NOW y MicroSD

Este proyecto utiliza una placa **OLIMEX ESP32-EVB** para recibir datos mediante el protocolo **ESP-NOW** y registrar la información en una tarjeta microSD utilizando el sistema de archivos **SD_MMC**. Se soportan diferentes tipos de mensajes, incluyendo datos de temperatura, humedad y detección de eventos.

## Descripción
El programa permite:

1. **Recepción de datos inalámbricos**:
   - Datos de temperatura y humedad.
   - Mensajes genéricos de detección.
2. **Registro de datos en tarjeta microSD**:
   - Los datos recibidos se almacenan con marcas de tiempo.
3. **Gestión de tipos de mensajes**:
   - `SENSOR_DATA`: Incluye temperatura y humedad.
   - `NUMBER_DATA`: Representa eventos específicos como detección de presencia.

## Características
- Recepción de datos inalámbricos utilizando **ESP-NOW**.
- Almacenamiento seguro de datos en una tarjeta microSD.
- Cálculo de tiempo transcurrido desde el inicio del registro.
- Soporte para múltiples tipos de datos.

## Requisitos de Hardware
- Placa **OLIMEX ESP32-EVB**.
- Módulo de tarjeta microSD (compatible con SD_MMC).

## Esquema de Conexión
- **OLIMEX ESP32-EVB**:
  - Utiliza el lector de tarjetas SD integrado en la placa (SD_MMC).

## Instalación y Configuración

1. **Configuración del entorno de desarrollo**:
   - Instalar el IDE de Arduino o **PlatformIO**.
   - Añadir las bibliotecas necesarias:
     - `esp_now` (para comunicación ESP-NOW).
     - `SD_MMC` (para gestionar la tarjeta SD).

2. **Clonar este repositorio**:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   ```

3. **Subir el código**:
   - Conecta la **OLIMEX ESP32-EVB** al ordenador y sube el código desde el entorno de desarrollo.

4. **Configuración de ESP-NOW**:
   - La **OLIMEX ESP32-EVB** debe configurarse como receptora y tener las direcciones MAC de los dispositivos emisores registrados.

## Uso
1. Inserta una tarjeta microSD formateada en el módulo o lector integrado de la **OLIMEX ESP32-EVB**.
2. Alimenta la placa y espera la recepción de datos mediante ESP-NOW.
3. Los datos recibidos se registrarán automáticamente en un archivo llamado `data.txt` en la tarjeta SD.
4. Verifica el contenido del archivo para observar los datos recibidos, incluyendo temperatura, humedad y eventos.

## Formato de los Datos Guardados
Los datos se almacenan en el archivo `data.txt` con la siguiente estructura:

- **SENSOR_DATA**:
  ```
  [HH:MM:SS] sensor exterior, Temperatura: XX.XX °C, Humedad: XX.XX %
  ```

- **NUMBER_DATA**:
  ```
  [HH:MM:SS] Detectado presencia en la entrada
  ```

- **Errores o mensajes desconocidos**:
  ```
  [HH:MM:SS] Tipo de mensaje desconocido
  ```

## Código
El código fuente principal está disponible en este repositorio. Incluye:
- Recepción y procesamiento de datos con ESP-NOW.
- Registro de datos en la tarjeta microSD.
- Manejo de marcas de tiempo.

## Licencia
Este proyecto está bajo la licencia MIT. Puedes usar, modificar y distribuir el código como desees.

---

### Contacto
Si tienes preguntas o necesitas soporte, puedes contactarme a través de [mi página web](https://infootec.net).
