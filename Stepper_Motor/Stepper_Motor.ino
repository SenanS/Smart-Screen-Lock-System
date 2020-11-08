#include <Stepper.h>

#define openSensor 2

// Define steps per rotation
const int stepsPerRevolution = 2048;
// Create stepper object 
Stepper myStepper = Stepper(stepsPerRevolution, 8, 10, 9, 11);

bool lockState = false;
bool doorState = false;
bool digInt = false;
int timer = 0;

void setup() {
  // Set the speed to 15 rpm
  myStepper.setSpeed(15);
  Serial.begin(9600);
  //Setup interrupt
  pinMode(openSensor, INPUT);
  attachInterrupt(digitalPinToInterrupt(openSensor), digitalInterrupt, RISING);
}

void loop() {

  if (Serial.available() > 0) {
    int incomingByte = Serial.read();
    Serial.println(incomingByte);
    if(incomingByte == 49){
//      Serial.println("received 1");
      change_lock_state();
    }
//    else if (incomingByte == 0 && lockState){
//      change_lock_state();
//    }
  }
  if(timer > 0)
    timer--;

  if(lockState != doorState){
    doorState = lockState;
    if(lockState){
      close_door();
    }
    else{
      if(digInt)
        Serial.write(1);
      open_door();
    }
    digInt= false;
  }
}

void open_door(){
  myStepper.step(1000);
  delay(250);
}

void close_door(){
  myStepper.step(-1000);
  delay(250);
}

void digitalInterrupt(){
  digInt = true;
  change_lock_state();
}

void change_lock_state(){
//  Serial.println(timer);
  if(timer == 0){
    timer = 100;
    lockState = !lockState;
  }
}
