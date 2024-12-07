#include <esp_now.h>
#include <WiFi.h>

// Declaración del tipo de mensaje
enum MessageType {
  SENSOR_DATA = 0,
  NUMBER_DATA = 1 // Identificador para mensajes de tipo número
};

// Estructura para el mensaje con identificador
typedef struct {
  MessageType type;  // Identificador del tipo de mensaje
  int number;        // Número a enviar
} NumberMessage;

NumberMessage message;

// Dirección MAC de la ESP32 receptora (cambiar según la dirección real)
uint8_t receiverAddress[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF}; 

// Pin del sensor HC-SR501
const int pirPin = 25;  // Cambia según la conexión

// Callback para notificar estado de envío
void onSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("Paquete enviado con estado: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Éxito" : "Fallido");
}

void setup() {
  Serial.begin(9600);

  // Configurar el pin del PIR
  pinMode(pirPin, INPUT);

  // Inicializar Wi-Fi en modo estación
  WiFi.mode(WIFI_STA);

  // Inicializar ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error al inicializar ESP-NOW");
    while (true);  // Detener ejecución si hay un fallo crítico
  }
  esp_now_register_send_cb(onSent);

  // Añadir el receptor
  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, receiverAddress, 6);
  peerInfo.channel = 0;  // Usar canal por defecto
  peerInfo.encrypt = false;

  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Error al añadir el receptor.");
    while (true);  // Detener ejecución si hay un fallo crítico
  }

  Serial.println("ESP-NOW inicializado y receptor añadido.");
}

void loop() {
  // Leer el estado del PIR
  int currentState = digitalRead(pirPin);

  if (currentState == HIGH) {
    // Preparar el mensaje
    message.type = NUMBER_DATA;  // Tipo del mensaje
    message.number = 11;         // Valor del número a enviar

    // Enviar mensaje
    esp_now_send(receiverAddress, (uint8_t *)&message, sizeof(message));
    //Serial.println("Número 11 enviado.");
    delay(10000);  // Esperar antes de enviar nuevamente
  }

  delay(2000);  // Pequeño retardo para evitar rebotes
}
