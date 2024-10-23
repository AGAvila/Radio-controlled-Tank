# Radio-controlled-Tank

This repository contains the code and hardware design for creating a small tank-like vehicle controlled via Wi-Fi using a **Raspberry Pi Pico**. The control can be done through either Telegram or MQTT. The code is written in MicroPython. 
If the vehicle is controlled through Telegram, a chat created with BotFather is used, where commands can be sent, and feedback from the device is received. If MQTT is used for control, a Python application is provided, which implements the 
necessary commands. For this case, the HiveMQ service is also utilized.
 
## Table of Contents
This README containts the following documentantion:

1. What can the vehicle do?
2. Components' list
   - Hardware 
   - Vehicle's body parts
3. References

### 1. What can the vehicle do?

The vehicle can be controlled using a tablet, smartphone or PC via Bluetooth. At the moment, it can do the only the following actions:

- Go forwards or backwards
- Turn left or right
- Rotate clockwise or counter-clockwise
- Stop if it detects a frontal colision
- Comunicate via Telegram or MQTT. In the latter case, the HiveMQ service is used.
- Acquire humidity and temperature values

### 2. Components' list

#### Hardware

Electronic components needed:

- Raspberry Pi Pico W: It will control the vehicle and enable the Wifi communication.
- L298N module: It supplies power to the motors according to control signals from the Raspberry Pi Pico.
- Two standard, brushed DC Motors.
- A standard 5 V USB powerbank: It is used to power the Raspberri Pi Pico via the USB
- A 9 V battery: It is used to power the motors, since they needed a higher voltage. A more elegant solution can be used, such as another, higher voltage battery or an additional DC/DC step-up (boost) converter to 9 to 12 volts.
- DHT22: Temperature and humidity sensor.
- HC-SR04: Ultrasonic sensor to measure distances.

#### Vehicle's body parts

The different body parts have been manufactured using a 3D printer. The chosen material is PLA. In reference **[1]** a link can be found to the thing (in thingiverse) where the .STL files are from.

### 3. References

[1] https://www.thingiverse.com/thing:972768
