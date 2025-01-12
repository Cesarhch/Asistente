# Proyecto ESP32 con ESP-NOW y Sensor PIR

Este proyecto utiliza una placa ESP32 para detectar movimiento mediante un sensor **HC-SR501 PIR** y enviar un mensaje al receptor utilizando el protocolo **ESP-NOW**.

## Descripción
El programa implementa los siguientes componentes:

1. **HC-SR501 PIR**: Sensor de movimiento que detecta cambios en el nivel infrarrojo.
2. **ESP32**: Microcontrolador que envía los datos de forma inalámbrica usando **ESP-NOW**.

## Características
- Detección de movimiento con el sensor PIR.
- Comunicación inalámbrica utilizando el protocolo **ESP-NOW**.
- Envío de un mensaje con un identificador y un número cuando se detecta movimiento.

## Requisitos de Hardware
- Placa **ESP32**.
- Sensor de movimiento **HC-SR501 PIR**.

## Esquema de Conexión
- **HC-SR501 PIR**:
  - Pin de señal conectado al GPIO 25 de la ESP32.

## Instalación y Configuración

1. **Configuración del entorno de desarrollo**:
   - Instalar el IDE de Arduino o **PlatformIO**.
   - Añadir las bibliotecas necesarias:
     - `esp_now` (para comunicación ESP-NOW).

2. **Clonar este repositorio**:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   ```

3. **Configuración del código**:
   - Actualizar la dirección MAC del receptor en la línea:
     ```cpp
     uint8_t receiverAddress[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
     ```
     Sustitúyelo por la dirección MAC del dispositivo receptor.

4. **Subir el código**:
   - Conecta la ESP32 al ordenador y sube el código desde el entorno de desarrollo.

## Uso
1. Alimenta la ESP32 y conecta el sensor PIR.
2. Cuando el sensor PIR detecte movimiento:
   - Enviará un mensaje con el identificador `NUMBER_DATA` y el valor `11` al dispositivo receptor.
3. Se implementa un retardo de 10 segundos entre detecciones para evitar múltiples envíos consecutivos.

## Código
El código fuente principal está disponible en este repositorio. Incluye:
- Inicialización del sensor PIR.
- Configuración de ESP-NOW.
- Envío de datos al dispositivo receptor cuando se detecta movimiento.

## Licencia
Este proyecto está bajo la licencia MIT. Puedes usar, modificar y distribuir el código como desees.

---

### Contacto
Si tienes preguntas o necesitas soporte, puedes contactarme a través de [mi página web](https://infootec.net).
