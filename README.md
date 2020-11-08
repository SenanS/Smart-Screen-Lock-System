# Smart-Screen-Lock-System
## A complex project involving two Arduino Unos, one Arduino Nano and a Raspberry Pi.<br/> Consisting of three modules:
* The RFID Communications Node.
* The Display Node.
* The Locking Node.

## [RFID](https://github.com/SenanS/Smart-Screen-Lock-System/tree/main/RFID_reader)  & [Communications](https://github.com/SenanS/Smart-Screen-Lock-System/tree/main/Master_Radio) Node
An Arduino Uno read and authenticated RFID signals. The results were communicated to the Arduino Nano, which used a radio module to send the results to the Raspberry Pi. The second Arduino also controlled LED authentication indicators.
<br/>The hardware used consisted of an MFRC522 contactless RF reader, an NRF24L01+ radio transceiver, and Arduino Nano, an Arduino Uno and two LEDs with resistors, as can be seen below.
![RFID Labelled diagram](https://github.com/SenanS/Smart-Screen-Lock-System/blob/main/Media/Labelled%20RFID.jpg)

## [Display](https://github.com/SenanS/Smart-Screen-Lock-System/blob/main/GUIPi.py) Node
My Raspberry Pi read the incoming radio signal from the RFID Reader node. It then decided to toggle the lock state or not, and sent a signal to the Locking node. Simultaneously it ran and updated an API-powered GUI showing data of interest.
<br/>The hardware consisted of a Raspberry Pi Model 2B, an NRF24L01+ radio transceiver module, a 13” laptop LCD display and a laptop controller board. 
![Display Labelled diagram](https://github.com/SenanS/Smart-Screen-Lock-System/blob/main/Media/Labelled%20Screen.jpg)

## [Locking](https://github.com/SenanS/Smart-Screen-Lock-System/tree/main/Stepper_Motor) Node
The simplest of my 3 nodes. This node consisted of an Arduino Uno attached to a motor power board, a stepper motor and a capacitive touch button. The Arduino would toggle the lock state based on input from the Raspberry Pi and the button attached. Then it would rotate the motor a specific amount to open/close the lock.
<br/>The hardware consisted of a 3D printed lock mechanism, and Arduino Uno, a TTP223 capacitive touch sensor, a stepper motor & motor power supply board.
![Locking Labelled diagram](https://github.com/SenanS/Smart-Screen-Lock-System/blob/main/Media/Labelled%20Lock.jpg)
