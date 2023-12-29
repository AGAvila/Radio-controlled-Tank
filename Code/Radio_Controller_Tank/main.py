from machine import Pin, PWM, UART
from funciones_motores import DCMotor

order = '0'  # Order ID
duty = 60  # PWM duty cycle - Range -> 0-100 (%)
freq = 15000  # PWM frequency - Rango -> 0-19200000

# UART config
uart = UART(0, 9600)

# Input/Output pins assignation
motor_control_led = Pin(25, Pin.OUT)  # LED to check if one of the motors is on
motor_1_forward = Pin(9, Pin.OUT)  # Controls the turn direction of the motors
motor_1_backward = Pin(8, Pin.OUT)
motor_2_forward = Pin(7, Pin.OUT)
motor_2_backward = Pin(6, Pin.OUT)

# PWM for the control of the motor feeding
enable1 = PWM(Pin(10))  # PWM motor 1
enable1.freq(freq)
enable2 = PWM(Pin(5))  # PWM motor 2
enable2.freq(freq)

# Starting of methods for the control of the motors
dc_motor = DCMotor(motor_1_forward, motor_1_backward, motor_2_forward, motor_2_backward, enable1, enable2,
                   0, 65535)

# Main loop
while True:

    if uart.any() > 0:
        order = uart.readline()
        # Stop
        if "1" in order:
            motor_control_led.value(0)
            dc_motor.motor_apagado()
        # Forward advance
        elif "2" in order:
            motor_control_led.value(1)
            dc_motor.motor_adelante(duty)
        # Backward advance
        elif "3" in order:
            motor_control_led.value(1)
            dc_motor.motor_atras(duty)
        # Turn left
        elif "4" in order:
            motor_control_led.value(1)
            dc_motor.motor_apagado()
            dc_motor.motor_1_adelante(duty)
        # Turn right
        elif "5" in order:
            motor_control_led.value(1)
            dc_motor.motor_apagado()
            dc_motor.motor_2_adelante(duty)
        # Rotation clockwise
        elif "6" in order:
            motor_control_led.value(1)
            dc_motor.motor_rotacion_horario(duty)
        # Rotation anticlockwise
        elif "7" in order:
            motor_control_led.value(1)
            dc_motor.motor_rotacion_antihorario(duty)
