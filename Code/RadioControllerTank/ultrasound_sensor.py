"""Methods to control the HC-SR04 ultrasonic sensor"""

from machine import Pin, time_pulse_us
import time, utime

def measure_distance():
    """
    Read the distance in cm to a surface using the ultrasound sensor HC-SR04
    """
    
    
    # Ultrasound pins
    trigger_pin = Pin(15, Pin.OUT) # Broche GP15 de la Pico
    echo_pin = Pin(14, Pin.IN)  # Broche GP14 de la Pico
    
    # Trigger pulse
    trigger_pin.value(0)
    time.sleep_us(2)
    trigger_pin.value(1)
    time.sleep_us(10)
    trigger_pin.value(0)

    # Measure pulse duration
    duration = time_pulse_us(echo_pin, 1, 30000)  # 30ms timeout for safety
    if duration > 0:
        # Speed of sound is approximately 340 meters per second (29 microseconds per centimeter)
        # Divide by 2 to get one-way distance
        distance_cm = (duration / 2) / 29.1
        return distance_cm
    else:
        # If no echo received, return a large value to indicate an error
        return float('inf')
    