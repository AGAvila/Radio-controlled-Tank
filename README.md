# Radio-controlled-Tank

This repository includes the code and hardware design to create a small tank-type vehicle controlled using a **Raspberry Pi Pico** and comunicated by **Bluetooth 2.0**. The code have been programmed in **MicroPython**.

## Authors

- Álvaro García Ávila
- Juan del Pino Mena 

## Table of Contents
This README containts the next documentantion:

1. What can the vehicle do?
   - What does each .py file do?
2. Components' list
   - Hardware 
   - Vehicle's body parts
3. Electric design
4. References

### 1. What can the vehicle do?

The vehicle can be controlled using a tablet, smartphone or PC via Bluetooth conection. At the moment, it can do the next actions:

- Go forwards/backwards
- Turn left/right
- Rotate clockwise/counter-clockwise

#### What does each .py file do?

- principal.py: It is the main program. This file can be renamed to "main.py" so it will still be working after restarting the Raspberry Pi Pico.
- funciones_motores.py: It contains a library with functions that allow the control of the motors.

### 2. Components' list

#### Hardware

Hardware/electric components needed:

- Raspberry Pi Pico: It will control the vehicle
- HC-06: This module will allow to comunicate with the Raspberri Pi Pico via Bluetooth. The device use as remote must by connected to this module.
- L298N: It allow to suply power to the motors and control them.
- Motors (x2)
- 9V battery: It is used to power the motors
- Powerbank: It is used to power the Raspberri Pi Pico

#### Vehicle's body parts

The different body parts have been made using a 3D printer. The choosen material is PLA. In **4. References** a link can be found to the web where the needed files are.

### 3. Electric design

In this image the electric connections can be consult:

![Montaje Electrico]()
