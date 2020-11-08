# Smart-Screen-Lock-System
## A complex project involving two Arduino Unos, one Arduino Nano and a Raspberry Pi.<br/> Consisting of three modules:
* The RFID Communications Node.
* The Display Node.
* The Locking Node.

## RFID Communications Node
My RFID Reader and Communication node used an MFRC522 contactless RF reader, an NRF24L01+ radio transceiver, and Arduino Nano, an Arduino Uno and two LEDs with resistors, as can be seen below.
![RFID Labelled diagram](https://github.com/SenanS/Smart-Screen-Lock-System/blob/main/Media/Labelled%20RFID.jpg)

## Display Node
My Display node consisted of a Raspberry Pi Model 2B, an NRF24L01+ radio transceiver module, a 13” laptop LCD display and a laptop controller board. 
![Display Labelled diagram](https://github.com/SenanS/Smart-Screen-Lock-System/blob/main/Media/Labelled%20Screen.jpg)

## Locking Node
The Lock and Interior Button node controlled the motor which moved the bolt across the door, as well as the button to lock/ unlock the door from the inside. It consisted of a 3D printed lock mechanism, and Arduino Uno, a capacitive touch sensor, a stepper motor & motor power supply board.
![Locking Labelled diagram](https://github.com/SenanS/Smart-Screen-Lock-System/blob/main/Media/Labelled%20Lock.jpg)
