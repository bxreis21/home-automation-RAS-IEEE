#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>

// WiFi
const char* ssid     = "Wokwi-GUEST";
const char* password = "";

// URLs da API
const char* API_BASE = "https://bxreis21.pythonanywhere.com/device/";

// ==== SALA ====
int leds_sala[]    = {5, 15, 2};
int buttons_sala[] = {21, 22, 23};
const int led_ids[]    = {6,7,4};
const int button_ids[] = {1,2,3};

// ==== JARDIM ====
int led_irrigacao = 18;
int pot_umidade   = 32;
int pot_temp      = 33;
const int led_irrigacao_id = 9;
const int pot_umidade_id   = 10;
const int pot_temp_id      = 11;

// LEDs de erro
int led_erro_get  = 12;
int led_erro_post = 13;

WiFiClientSecure client;

void setup() {
  Serial.begin(115200);
  connectWiFi();
  setupPins();
}

void loop() {
  // Sala
  updateButtons();
  updateLEDs();

  // Jardim
  updateIrrigation();

  delay(1000); // 1s entre loops
}

// =================== FUNÇÕES ===================

void connectWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado!");
  client.setInsecure();
}

void setupPins() {
  for (int pin : leds_sala) pinMode(pin, OUTPUT);
  pinMode(led_irrigacao, OUTPUT);
  pinMode(led_erro_get, OUTPUT);
  pinMode(led_erro_post, OUTPUT);
  digitalWrite(led_erro_get, LOW);
  digitalWrite(led_erro_post, LOW);

  for (int pin : buttons_sala) pinMode(pin, INPUT_PULLUP);
  pinMode(pot_umidade, INPUT);
  pinMode(pot_temp, INPUT);
}

// ==== SALA ====
void updateButtons() {
  for (int i = 0; i < 3; i++) {
    int state = digitalRead(buttons_sala[i]) == LOW ? 1 : 0;
    if (!postDeviceState(button_ids[i], state)) digitalWrite(led_erro_post, HIGH);
    else digitalWrite(led_erro_post, LOW);
  }
}

void updateLEDs() {
  for (int i = 0; i < 4; i++) {
    int state = getDeviceState(led_ids[i]);
    if (state == -1) digitalWrite(led_erro_get, HIGH);
    else {
      digitalWrite(led_erro_get, LOW);
      digitalWrite(leds_sala[i], state);
    }
  }
}

void updateIrrigation() {
  int umidade = map(analogRead(pot_umidade), 0, 4095, 0, 10);
  int temp    = map(analogRead(pot_temp), 0, 4095, 0, 10);

  if (!postDeviceState(pot_umidade_id, umidade)) digitalWrite(led_erro_post, HIGH);
  if (!postDeviceState(pot_temp_id, temp)) digitalWrite(led_erro_post, HIGH);

  if (umidade == -1 || temp == -1) {
    digitalWrite(led_erro_get, HIGH);
    return;
  } else digitalWrite(led_erro_get, LOW);

  bool irrigLevel = fuzzyIrrigation(umidade, temp);
  digitalWrite(led_irrigacao, irrigLevel);
  postDeviceState(led_irrigacao_id, irrigLevel);
}

// ==== FUZZY ====
bool fuzzyIrrigation(int umidade, int temp) {
  bool ligar = false;
  // regras simples: liga irrigação apenas se uma das condições for atendida
  if ((umidade <= 4 && temp >= 5) ||   // baixa umidade e alta temperatura
      (umidade <= 4 && temp <= 4) ||   // baixa umidade e baixa temperatura
      (umidade >= 5 && umidade <=7 && temp >=8)) // umidade média e temperatura alta
    ligar = true;
}

// ==== HTTP ====
int getDeviceState(const int device_id) {
  if (WiFi.status() != WL_CONNECTED) return -1;

  HTTPClient http;
  String url = String(API_BASE) + device_id + "/read/";
  http.begin(client, url);
  int code = http.GET();
  int state = -1;

  if (code == 200) {
    String payload = http.getString();
    DynamicJsonDocument doc(256);
    deserializeJson(doc, payload);
    if (String(doc["type"]) == "digital") state = doc["value"];
    else state = doc["value"];
  }
  http.end();
  return state;
}

bool postDeviceState(const int device_id, int value) {
  if (WiFi.status() != WL_CONNECTED) return false;

  HTTPClient http;
  String url = String(API_BASE) + device_id + "/write/";
  http.begin(client, url);
  http.addHeader("Content-Type", "application/json");

  DynamicJsonDocument doc(128);
  doc["value"] = value;
  String json;
  serializeJson(doc, json);

  int code = http.POST(json);
  http.end();

  return (code == 200);
}
