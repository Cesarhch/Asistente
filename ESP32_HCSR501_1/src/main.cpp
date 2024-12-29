#include <esp_now.h>
#include <WiFi.h>
#include "DHT.h"

// Configuración del sensor DHT
#define DHTPIN 33
#define DHTTYPE DHT11
#define TPL 25
DHT dht(DHTPIN, DHTTYPE);

// Dirección MAC de la ESP32 receptora
uint8_t receiverAddress[] = {0xE0, 0x5A, 0x1B, 0x66, 0x57, 0x38};

// Declaración del tipo de mensaje
enum MessageType {
  SENSOR_DATA
};

// Estructura para el mensaje con identificador
typedef struct {
  MessageType type;
  float temperature;
  float humidity;
} SensorMessage;

SensorMessage dataToSend;

// Callback para notificar estado de envío
void onSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("Estado del envío: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Éxito" : "Fallido");
}

void setup() {
  Serial.begin(9600);
  pinMode(TPL, OUTPUT);
  digitalWrite(TPL, LOW);
  // Inicializar el sensor DHT
  dht.begin();
  Serial.println("Sensor DHT inicializado.");

  // Inicializar Wi-Fi en modo estación
  WiFi.mode(WIFI_STA);

  // Inicializar ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error al inicializar ESP-NOW");
    return;
  }
  esp_now_register_send_cb(onSent);

  // Añadir el receptor
  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, receiverAddress, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Error al añadir el receptor.");
    return;
  }

  Serial.println("ESP-NOW inicializado y receptor añadido.");
}

void loop() {
  // Leer datos del sensor DHT
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  // Comprobar si la lectura es válida
  if (isnan(temp) || isnan(hum)) {
    Serial.println("Error al leer el sensor DHT");
    delay(2000);
    return;
  }

  // Preparar datos para enviar
  dataToSend.type = SENSOR_DATA;
  dataToSend.temperature = temp;
  dataToSend.humidity = hum;
  delay(1000);
  // Enviar datos
  esp_now_send(receiverAddress, (uint8_t *)&dataToSend, sizeof(dataToSend));

  // Retardo antes de enviar nuevamente
  delay(1000);
  digitalWrite(TPL, HIGH);
  delay(1000);
  esp_deep_sleep_start();
}
