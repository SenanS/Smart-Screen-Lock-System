#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#define blueLED 6
#define redLED 3
RF24 radio(7, 8); 

int val = 0;
int lightTime = 500;
const uint64_t pipe = 0xF0F0F0F0E1LL;

void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.setChannel(0x76) ;
  radio.openWritingPipe(pipe);
  radio.setPALevel(RF24_PA_MAX);
  radio.enableDynamicPayloads() ;
  radio.powerUp() ;
  radio.stopListening();

  pinMode(blueLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  resetLEDs();
}

void loop() {
  if (Serial.available()) {
    val = Serial.read();
//    Serial.print("ACK : ");
//    Serial.println(val);
  }
  resetLEDs();
  switch(val){
    case 2 :
      digitalWrite(redLED, HIGH);
      sendValueAndWait(val);
      break;
    case 1 :
      digitalWrite(blueLED, HIGH);
      sendValueAndWait(val);      
      break;
    case 3 :
      digitalWrite(blueLED, HIGH);
      sendValueAndWait(val);
      break;
    default :
      break;
  }
  val = -1;
}

void resetLEDs(){
  digitalWrite(blueLED, LOW);
  digitalWrite(redLED, LOW);
}

void sendValueAndWait(int value){
  if(!radio.write(&value, sizeof(value))){
    digitalWrite(blueLED, HIGH);
    delay(50);
    digitalWrite(blueLED, LOW);
    delay(50);
    digitalWrite(blueLED, HIGH);
    delay(50);
    digitalWrite(blueLED, LOW);
    delay(50);
    digitalWrite(blueLED, HIGH);
    delay(50);
    digitalWrite(blueLED, LOW);
    delay(50);
    digitalWrite(blueLED, HIGH);
    delay(50);
    digitalWrite(blueLED, LOW);
    delay(50);
    digitalWrite(blueLED, HIGH);
    delay(50);
    digitalWrite(blueLED, LOW);
    delay(50);
  }
  else{
    delay(lightTime);
  }
}
