#include <dht11.h>
#define DHT11PIN 3

dht11 DHT11;

int measurePin = 0; //먼지 센서 A0에 연결
int ledPower = 2;   
int samplingTime = 280;
int deltaTime = 40;
int sleepTime = 9680;
  
float voMeasured = 0;
float calcVoltage = 0;
float dustDensity = 0;



void setup() {
  Serial.begin(9600);
  pinMode(ledPower,OUTPUT);

}

void loop() {
  int chk = DHT11.read(DHT11PIN);

  digitalWrite(ledPower,LOW); 
  delayMicroseconds(samplingTime);
  
  voMeasured = analogRead(measurePin); // 먼지 값 읽어오기
  
  delayMicroseconds(deltaTime);
  digitalWrite(ledPower,HIGH); 
  delayMicroseconds(sleepTime);
  
  // 디지털 신호를 0 - 5 사이로 변환하여 전압 구하기
  calcVoltage = voMeasured * (5.0 / 1024.0);
  
  dustDensity = 0.17 * calcVoltage - 0.1;
  dustDensity = dustDensity*(-1);
  
  Serial.print((float)DHT11.humidity, 2);
  Serial.print(',');
  Serial.print((float)DHT11.temperature, 2);
  Serial.print(',');
  Serial.println(dustDensity); // unit: mg/m3
  
  delay(10000);

}
