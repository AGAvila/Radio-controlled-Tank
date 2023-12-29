from machine import Pin, PWM, UART
from motorsControl import DCMotor

order = "0"     # Order ID
speed = 80      # Range -> 0-100 (%)
freq = 15000    # PWM frequency - Rango -> 0-19200000

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
dc_motor = DCMotor(speed, motor_1_forward, motor_1_backward, motor_2_forward, motor_2_backward, enable1, enable2,
                   0, 65535)

motor_control_led.value(0)

# Main loop
while True:

    if uart.any() > 0:

        order = uart.readline()

        # Stop
        if "1" in order:
            uart.write("Stopping\n")
            motor_control_led.value(0)
            dc_motor.all_motors_off()
        # Forward advance
        elif "2" in order:
            uart.write("Going forward\n")
            motor_control_led.value(1)
            dc_motor.all_motors_forward()
        # Backward advance
        elif "3" in order:
            uart.write("Going backward\n")
            motor_control_led.value(1)
            dc_motor.motor_backward()
        # Turn left
        elif "4" in order:
            uart.write("To the left\n")
            motor_control_led.value(1)
            dc_motor.all_motors_off()
            dc_motor.motor_1_forward()
        # Turn right
        elif "5" in order:
            uart.write("To the right\n")
            motor_control_led.value(1)
            dc_motor.all_motors_off()
            dc_motor.motor_2_forward()
        # Rotation clockwise
        elif "6" in order:
            uart.write("Clockwise\n")
            motor_control_led.value(1)
            dc_motor.motor_rotation_clockwise()
        # Rotation anticlockwise
        elif "7" in order:
            uart.write("Anticlockwise\n")
            motor_control_led.value(1)
            dc_motor.motor_rotation_anticlockwise()
