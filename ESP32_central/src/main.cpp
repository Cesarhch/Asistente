#include <esp_now.h>
#include <WiFi.h>
#include <SD_MMC.h>

// Declaración de tipos de mensajes
enum MessageType {
  SENSOR_DATA,  // Para temperatura y humedad
  NUMBER_DATA   // Para otros números
};

// Estructuras de datos específicas para cada tipo
typedef struct {
  float temperature;
  float humidity;
} SensorData;

typedef struct {
  int number;
} NumberData;

// Estructura genérica para recibir datos
typedef struct {
  MessageType type;  // Identificador del tipo de mensaje
  union {
    SensorData sensorData;
    NumberData numberData;
  } payload;  // Datos específicos según el tipo
} GenericMessage;

GenericMessage receivedMessage;

// Variable para el tiempo de inicio
unsigned long startTime;

void onReceive(const uint8_t *mac, const uint8_t *incomingData, int len) {
  // Copiar datos en la estructura
  memcpy(&receivedMessage, incomingData, len);

  // Calcular tiempo transcurrido
  unsigned long elapsedMillis = millis() - startTime;
  unsigned long elapsedSeconds = elapsedMillis / 1000;
  unsigned int hours = elapsedSeconds / 3600;
  unsigned int minutes = (elapsedSeconds % 3600) / 60;
  unsigned int seconds = elapsedSeconds % 60;

  // Formatear tiempo transcurrido
  char elapsedTimeStr[20];
  snprintf(elapsedTimeStr, sizeof(elapsedTimeStr), "%02u:%02u:%02u", hours, minutes, seconds);

  // Abrir archivo para guardar los datos
  File dataFile = SD_MMC.open("/data.txt", FILE_APPEND);
  if (!dataFile) {
    Serial.println("Error al abrir el archivo en la tarjeta SD.");
    return;
  }

  // Procesar y guardar los datos según el tipo de mensaje
  switch (receivedMessage.type) {
    case SENSOR_DATA:
      Serial.println("Datos de sensor recibidos:");
      Serial.print("Temperatura: ");
      Serial.print(receivedMessage.payload.sensorData.temperature);
      Serial.println(" °C");
      Serial.print("Humedad: ");
      Serial.print(receivedMessage.payload.sensorData.humidity);
      Serial.println(" %");

      // Guardar en la microSD
      dataFile.printf("[%s] sensor exterior, Temperatura: %.2f °C, Humedad: %.2f %%\n",
                      elapsedTimeStr,
                      receivedMessage.payload.sensorData.temperature,
                      receivedMessage.payload.sensorData.humidity);
      break;

    case NUMBER_DATA:
      // Siempre imprimir "Detectado presencia en la entrada"
      Serial.println("Detectado presencia en la entrada");
      dataFile.printf("[%s] Detectado presencia en la entrada\n", elapsedTimeStr);
      break;

    default:
      Serial.println("Tipo de mensaje desconocido.");
      dataFile.printf("[%s] Tipo de mensaje desconocido\n", elapsedTimeStr);
      break;
  }

  // Cerrar el archivo
  dataFile.close();
  Serial.println("Datos guardados en la tarjeta SD.");
}

void setup() {
  Serial.begin(9600);

  // Inicializar Wi-Fi en modo estación
  WiFi.mode(WIFI_STA);
  Serial.println("Wi-Fi inicializado en modo estación");

  // Inicializar ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error al inicializar ESP-NOW");
    return;
  }

  // Registrar callback para recibir datos
  esp_now_register_recv_cb(onReceive);

  // Inicializar la tarjeta microSD
  if (!SD_MMC.begin()) {
    Serial.println("Error al inicializar la tarjeta SD.");
    return;
  }
  Serial.println("Tarjeta SD inicializada correctamente.");

  // Configurar tiempo inicial
  startTime = millis();
  const char* startDate = "2024-11-30 09:00:00"; // Fecha de inicio predefinida

  // Abrir el archivo (sin importar si existe) y escribir el inicio del registro
  File dataFile = SD_MMC.open("/data.txt", FILE_APPEND);
  if (dataFile) {
    dataFile.printf("Inicio del registro: %s\n", startDate);
    dataFile.close();
    Serial.println("Inicio del registro guardado en la tarjeta SD.");
  } else {
    Serial.println("Error al escribir el inicio del registro en la tarjeta SD.");
  }

  Serial.println("ESP-NOW inicializado y esperando datos...");
}

void loop() {
  // No hay lógica adicional, los datos se manejan en el callback
}
