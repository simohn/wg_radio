#include <Arduino.h>

#include <WiFi.h>
#include <WiFiUdp.h>
#include "credentials.h"

// IP address to send UDP data to.
// it can be ip address of the server or 
// a network broadcast address
// here is broadcast address
const char * udpAddress = "192.168.1.136";
const int udpPort = 44444;

//create UDP instance
WiFiUDP udp;

// Potentiometer is connected to GPIO 34 (Analog ADC1_CH6) 
const int potPin = 34;

// variable for storing the potentiometer value
uint16_t potValue = 0;

void setup() {
  pinMode(potPin, OUTPUT);
  Serial.begin(9600);

  //Connect to the WiFi network
  WiFi.begin(ssid, pwd);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  //This initializes udp and transfer buffer
  udp.begin(udpPort);
}

void loop() {
  // Reading potentiometer value
  potValue = analogRead(potPin);
  Serial.println(potValue);
  delay(100);

  uint8_t volume = (potValue/4095.0)*255.0;

  //data will be sent to server
  uint8_t buffer[50] = "Vol: ";
  buffer[5] = volume;
  buffer[6] = '\0';

  //send hello world to server
  udp.beginPacket(udpAddress, udpPort);
  udp.write(buffer, 50);
  udp.endPacket();
  memset(buffer, 0, 50);
  
  //processing incoming packet, must be called before reading the buffer
  udp.parsePacket();
}