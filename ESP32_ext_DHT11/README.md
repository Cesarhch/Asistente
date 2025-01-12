# Proyecto ESP32 con ESP-NOW, DHT11 y TPL5110

Este proyecto utiliza una placa ESP32 para enviar datos de temperatura y humedad, obtenidos de un sensor **DHT11**, a otro dispositivo mediante el protocolo **ESP-NOW**. Además, se incorpora un temporizador **TPL5110** para optimizar el consumo energético del sistema.

## Descripción
El programa implementa los siguientes componentes:

1. **DHT11**: Sensor de temperatura y humedad.
2. **ESP32**: Microcontrolador que envía los datos de forma inalámbrica usando **ESP-NOW**.
3. **TPL5110**: Temporizador de bajo consumo que controla el encendido y apagado del sistema para maximizar la eficiencia energética.

## Características
- Lectura de temperatura y humedad con el sensor **DHT11**.
- Comunicación inalámbrica utilizando el protocolo **ESP-NOW**.
- Implementación de un temporizador **TPL5110** para minimizar el consumo energético.
- Posibilidad de integrar modo de sueño profundo (**deep sleep**) para optimizar aún más el consumo.

## Requisitos de Hardware
- Placa **ESP32**.
- Sensor **DHT11**.
- Temporizador **TPL5110**.

## Esquema de Conexión
- **DHT11**:
  - Pin de señal conectado al GPIO 33 de la ESP32.
- **TPL5110**:
  - Pin DONE conectado al GPIO 25 de la ESP32.

## Instalación y Configuración

1. **Configuración del entorno de desarrollo**:
   - Instalar el IDE de Arduino o **PlatformIO**.
   - Añadir las bibliotecas necesarias:
     - `DHT` (para el sensor DHT11).
     - `esp_now` (para comunicación ESP-NOW).

2. **Clonar este repositorio**:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   ```

3. **Configuración del código**:
   - Actualizar la dirección MAC del receptor en la línea:
     ```cpp
     uint8_t receiverAddress[] = {0xE0, 0x5A, 0x1B, 0x66, 0x57, 0x38};
     ```
     Sustitúyelo por la dirección MAC del dispositivo receptor.

4. **Subir el código**:
   - Conecta la ESP32 al ordenador y sube el código desde el entorno de desarrollo.

## Uso
1. Alimenta la ESP32 y el sensor DHT11.
2. El sensor lee los datos de temperatura y humedad.
3. Los datos se envían al receptor mediante ESP-NOW.
4. El temporizador TPL5110 apaga el sistema para reducir el consumo energético.
5. Existe la opción de implementar el modo de sueño profundo para ahorrar aún más energía (línea comentada en el código).

## Código
El código fuente principal está disponible en este repositorio. Incluye:
- Inicialización del sensor DHT11.
- Configuración de ESP-NOW.
- Envío periódico de datos al dispositivo receptor.
- Uso del temporizador TPL5110 y configuración para modo de sueño profundo.

## Licencia
Este proyecto está bajo la licencia MIT. Puedes usar, modificar y distribuir el código como desees.

---

### Contacto
Si tienes preguntas o necesitas soporte, puedes contactarme a través de [mi página web](https://infootec.net).
