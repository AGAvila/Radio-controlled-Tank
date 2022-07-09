"""
Biblioteca que define la clase DCMotor, la cual incluye funciones para el control de
giro y parada de dos motores mediante el driver L298N.

Autores: Álvaro García Ávila y Juan del Pino Mena
Fecha última modificación: 24/05/2022
"""

import machine

class DCMotor:
    
    def __init__(self, pin1, pin2, pin3, pin4, enable_pin1, enable_pin2, min_duty=0, max_duty=65535): #Inicialización variables
        #Pines control lado 1
        self.pin1 = pin1 
        self.pin2 = pin2
        #Pines control lado 2
        self.pin3 = pin3 
        self.pin4 = pin4
        
        self.enable_pin1 = enable_pin1
        self.enable_pin2 = enable_pin2
        self.min_duty = min_duty #Duty cycle mínimo
        self.max_duty = max_duty #Duty cycle máximo

    def motor_adelante(self,speed): #Los motores hacen avanzar
        self.speed = speed
        self.enable_pin1.duty_u16(self.duty_cycle(self.speed))
        self.enable_pin2.duty_u16(self.duty_cycle(self.speed))
        self.pin1.value(1)
        self.pin2.value(0) 
        self.pin3.value(0)
        self.pin4.value(1)
        
    def motor_atras(self,speed): #Los motores hacen retroceder
        self.speed = speed
        self.enable_pin1.duty_u16(self.duty_cycle(self.speed))
        self.enable_pin2.duty_u16(self.duty_cycle(self.speed))
        self.pin1.value(0)
        self.pin2.value(1)
        self.pin3.value(1)
        self.pin4.value(0)
        
    def motor_apagado(self): #Todos los motores apagados
        self.enable_pin1.duty_u16(0)
        self.enable_pin2.duty_u16(0)
        self.pin1.value(0)
        self.pin2.value(0)
        self.pin3.value(0)
        self.pin4.value(0)
        
    def motor_1_adelante(self,speed): #Se enciende el motor 1 - No se modifica el esta del motor 2
        self.speed = speed
        self.enable_pin1.duty_u16(self.duty_cycle(self.speed))
        self.enable_pin2.duty_u16(0)
        self.pin1.value(1)
        self.pin2.value(0)
        
    def motor_2_adelante(self,speed): #Se enciende el motor 2 - No se modifica el esta del motor 1
        self.speed = speed
        self.enable_pin1.duty_u16(0)
        self.enable_pin2.duty_u16(self.duty_cycle(self.speed))
        self.pin3.value(0)
        self.pin4.value(1)
        
    def motor_rotacion_horario(self,speed): #Se enciende el motor 1 girando hacia atrás y el motor 2 girando hacia adelante
        self.speed = speed
        self.enable_pin1.duty_u16(self.duty_cycle(self.speed))
        self.enable_pin2.duty_u16(self.duty_cycle(self.speed))
        self.pin1.value(0)
        self.pin2.value(1)
        self.pin3.value(0)
        self.pin4.value(1)
    
    def motor_rotacion_antihorario(self,speed): #Se enciende el motor 2 girando hacia atrás y el motor 1 girando hacia adelante
        self.speed = speed
        self.enable_pin1.duty_u16(self.duty_cycle(self.speed))
        self.enable_pin2.duty_u16(self.duty_cycle(self.speed))
        self.pin1.value(1)
        self.pin2.value(0)
        self.pin3.value(1)
        self.pin4.value(0)
        
    def duty_cycle(self,speed): #Cálculo del duty cicle
       if self.speed <= 0 or self.speed > 100:
            duty_cycle = 0
       else:
        duty_cycle = int(self.min_duty + (self.max_duty - self.min_duty)*((self.speed-1)/(100-1)))
        return duty_cycle

