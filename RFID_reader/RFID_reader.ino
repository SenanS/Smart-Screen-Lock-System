//White card  - C6431F39
//BF card     - FDF43BB6
//Fob         - 2E4D9063
 
#include <SPI.h>
#include <MFRC522.h>
 
#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);  
 
void setup() 
{
  Serial.begin(9600);
  SPI.begin();      
  mfrc522.PCD_Init(); 
}
void loop() 
{
  // Poll for RFID tags
  if ( ! mfrc522.PICC_IsNewCardPresent()){
    return;
  }
  if ( ! mfrc522.PICC_ReadCardSerial()){
    return;
  }

  //Print ID in hex
  String content= "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++){
//     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
//     Serial.print(mfrc522.uid.uidByte[i], HEX);
     mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ";
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  content.toUpperCase();

  //Check in whitelist
  if (content.substring(1) == "C6 43 1F 39"){
//    Serial.println("Authorized access, Welcome card 1.");
    Serial.write(1);
    delay(2500);
  }
  else   if (content.substring(1) == "FD F4 3B B6"){
//    Serial.println("Authorized access, Welcome card 2.");
    Serial.write(2);
    delay(2500);
  }
  else   if (content.substring(1) == "2E 4D 90 63"){
//    Serial.println("Authorized access, Welcome key-chain.");
    Serial.write(3);
    delay(2500);
  } 
  else{
    Serial.write(0);
    delay(2500);
  }
}
