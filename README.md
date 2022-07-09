# Radio-controlled-Tank

This repository includes the code and hardware design to create a small tank-type vehicle controlled using a **Raspberry Pi Pico** by using **Bluetooth 2.0**. The code is written on **MicroPython**.

## Authors

- [Álvaro García Ávila](https://github.com/AGAvila)
- [Juan del Pino Mena](https://github.com/dpmj) 

## Table of Contents
This README containts the following documentantion:

1. What can the vehicle do?
   - What does each .py file do?
2. Components' list
   - Hardware 
   - Vehicle's body parts
3. Electric design
4. References

### 1. What can the vehicle do?

The vehicle can be controlled using a tablet, smartphone or PC via Bluetooth. At the moment, it can do the only the following actions:

- Go forwards or backwards
- Turn left or right
- Rotate clockwise or counter-clockwise

#### What does each .py file do?

- principal.py: It is the main program. This file can be renamed to "main.py" so it will still be working after restarting the Raspberry Pi Pico.
- funciones_motores.py: It contains a library with functions that allow the control of the motors.

### 2. Components' list

#### Hardware

Electronic components needed:

- Raspberry Pi Pico: It will control the vehicle
- HC-06 module: This module will allow to comunicate with the Raspberri Pi Pico via Bluetooth. The device use as remote must by connected to this module.
- L298N module: It supplies power to the motors according to control signals from the Raspberry Pi Pico.
- Two standard, brushed DC Motors.
- A standard 5 V USB powerbank: It is used to power the Raspberri Pi Pico via the USB
- A 9 V battery: It is used to power the motors, since they needed a higher voltage. A more elegant solution can be used, such as another, higher voltage battery or an additional DC/DC step-up (boost) converter to 9 to 12 volts.

#### Vehicle's body parts

The different body parts have been manufactured using a 3D printer. The chosen material is PLA. In reference **[1]** a link can be found to the thing (in thingiverse) where the .STL files are from.

### 3. Electric design

The electric connections are detailed in the figure below.

![Montaje Electrico](https://raw.githubusercontent.com/AGAvila/Radio-controlled-Tank/main/Electric_Design.png)

### 4. References

[1] https://www.thingiverse.com/thing:972768
