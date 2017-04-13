#include <ESP8266WiFi.h>

int led = LED_BUILTIN;
String DATA_STRING = "The Quick Brown Fox Jumped Over The Lazy Dog.\n";

const char* ssid = "YOURSSIDHERE";
const char* passwd = "YOURPASSWDHERE";
const char* host_addr = "YOURHOSTADDRHERE";
const int host_port = 8888;

WiFiClient client;

void setup() {
  pinMode(led, OUTPUT);
  pinMode(led, HIGH);
  
  Serial.begin(115200);
  Serial.println();

  // Connect to Wifi AP
  WiFi.begin(ssid, passwd);
  
  Serial.print("Connecting");
  toggleLED();
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  
  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());
  toggleLED();

  // Create TCP connection
  client.setNoDelay(true);
  if (!client.connect(host_addr, host_port)) {
    Serial.println("connection failed");
    digitalWrite(led, HIGH);
    return;
  } else {
    Serial.printf("Connected to server %s:%d\r\n", host_addr, host_port);
  }
}

void loop() {
  // send data to be echoed
  // client.print(DATA_STRING);

  // wait for response until timeout
  unsigned long timeout = millis();
  while (client.available() == 0) {
    if (millis() - timeout > 5000) {
      Serial.println(">>> Client Timeout !");
      delay(0);   // resets watchdog
      return;
    }
  }

  // receive and print data
  while (client.available()) {
    String rx_string = client.readStringUntil('\n');
  }

  delay(0);       // resets watchdog
  toggleLED();
}

void toggleLED() {
  digitalWrite(led, !digitalRead(led));
}

