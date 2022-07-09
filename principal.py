"""
Programa que permite el control de un robot que recibe órdenes mediante comunicación Bluetooth

Autores: Álvaro García Ávila y Juan del Pino Mena
Fecha última modificación: 24/05/2022
"""

#Bibliotecas
from machine import Pin, PWM, UART
from funciones_motores import DCMotor

#----------------------------------------------------------------------------------------------------------------

uart = UART(0,9600) #Configuración UART

#Variables
orden = '0'   #ID de la orden a ejecutar
duty = 80     #Duty cycle PWM (80 %) - Rango -> 0-100
freq = 15000  #Frecuencia PWM - Rango -> 0-19200000

#Asignación entradas/salida
led_interno = machine.Pin(25,machine.Pin.OUT) #Led que indica si algún motor está en funcionamiento
motor_1_adelante = Pin(9, Pin.OUT)            #Control del sentido de giro de los motores
motor_1_atras = Pin(8, Pin.OUT)
motor_2_adelante = Pin(7, Pin.OUT) 
motor_2_atras = Pin(6, Pin.OUT)

#PWM para control de los motores
enable1 = machine.PWM(machine.Pin(10)) #PWM motor 1
enable1.freq(freq)
enable2 = machine.PWM(machine.Pin(5))  #PWM motor 2
enable2.freq(freq)

#Inicializa la biblioteca para control de motores 
dc_motor = DCMotor(motor_1_adelante, motor_1_atras, motor_2_adelante, motor_2_atras, enable1, enable2, 0, 65535)

#----------------------------------------------------------------------------------------------------------------

while True: #Bucle principal
    
    #Lectura de ordenes
    if uart.any() > 0:
        orden = uart.readline()
    
        #Repertorio de ordenes
        if "1" in orden: #Stop
            led_interno.value(0)
            dc_motor.motor_apagado()
            
        elif "2" in orden: #Avance hacia adelante
            led_interno.value(1)
            dc_motor.motor_adelante(duty)
            
        elif "3" in orden: #Avance hacia atrás
            led_interno.value(1)
            dc_motor.motor_atras(duty)
            
        elif "4" in orden: #Giro a la izquierda
            led_interno.value(1)
            dc_motor.motor_apagado()
            dc_motor.motor_1_adelante(duty)
            
        elif "5" in orden: #Giro a la derecha
            led_interno.value(1)
            dc_motor.motor_apagado()
            dc_motor.motor_2_adelante(duty)
            
        elif "6" in orden: #Rotación sentido horario
            led_interno.value(1)
            dc_motor.motor_rotacion_horario(duty)

        elif "7" in orden: #Rotación sentido antihorario
            led_interno.value(1)
            dc_motor.motor_rotacion_antihorario(duty)