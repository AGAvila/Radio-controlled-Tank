from machine import Pin, PWM, UART, Timer
from motorsControl import DCMotor
from wirelessCommunication import wifiCom
import dht
import time

    
def get_temp_and_humidity():
    """
    Read data of temperature and humidity from DHT22.
    
    Inputs:
    - None
    Returns:
    - None
    """
    
    global temperature
    global humidity
    
    try:
        # Sensor communication pin
        sensor = dht.DHT22(Pin(22))
        # Get measures from sensor
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
    except:
        # If DHT22 measures cannot be read
        temperature = "Error"
        humidity = "Error"        

def starting_message():
    """
    Welcome message notifying of the current set of instructions
    """
    
    inst_1 = "Current instruction set:\n/stop\n/go\n/back\n/left\n/right\n/clockwise\n/anticlockwise\n"
    inst_2 = "/temperature\n/humidity\n"
    instructions_set_message = inst_1 + inst_2
    
    wifiCom.send_telegram_message("Radio Robot Online")
    wifiCom.send_telegram_message(instructions_set_message)

def process_order(message: str):
    """
    Does and action depending on the message received from Telegram
    """
    
    if "/stop" in message:
        #uart.write("Stopping\n")
        motor_control_led.value(0)
        dc_motor.all_motors_off()
        wifiCom.send_telegram_message("Stopping")
    # Forward advance
    elif "/go" in message:
        #uart.write("Going forward\n")
        motor_control_led.value(1)
        dc_motor.all_motors_forward()
        wifiCom.send_telegram_message("Going forward!")
    # Backward advance
    elif "/back" in message:
        #uart.write("Going backward\n")
        motor_control_led.value(1)
        dc_motor.motor_backward()
        wifiCom.send_telegram_message("Going backwards!")
    # Turn left
    elif "/left" in message:
        #uart.write("To the left\n")
        motor_control_led.value(1)
        dc_motor.all_motors_off()
        dc_motor.motor_1_forward()
        wifiCom.send_telegram_message("Turning left")
    # Turn right
    elif "/right" in message:
        #uart.write("To the right\n")
        motor_control_led.value(1)
        dc_motor.all_motors_off()
        dc_motor.motor_2_forward()
        wifiCom.send_telegram_message("Turning right")
    # Rotation clockwise
    elif "/clockwise" in message:
        #uart.write("Clockwise\n")
        motor_control_led.value(1)
        dc_motor.motor_rotation_clockwise()
        wifiCom.send_telegram_message("Rotating clockwise")
    # Rotation anticlockwise
    elif "/anticlockwise" in message:
        #uart.write("Anticlockwise\n")
        motor_control_led.value(1)
        dc_motor.motor_rotation_anticlockwise()
        wifiCom.send_telegram_message("Rotating anticlockwise")
    elif "/temperature" in message:
        get_temp_and_humidity()
        wifiCom.send_telegram_message(f"Temperature: {temperature} Cº")
    elif "/humidity" in message:
        get_temp_and_humidity()
        wifiCom.send_telegram_message(f"Humidity: {humidity} %")
    else:
        print("I do not know what do you want from me\n")
        wifiCom.send_telegram_message("I do not know what do you want from me")


if __name__ == "__main__":
    
    # Motors config
    order = "0"     # Order ID
    speed = 80      # Power transfer to the motors (Range -> 0-100) 
    freq = 15000    # PWM frequency (Range -> 0-19200000)
    
    # DHT22 sensors values
    temperature = "0"
    humidity = "0"
    
    # Set the initial offset to None
    offset = None
    
    # UART config (legacy)
    # uart = UART(0, 9600)

    # Input/Output pins assignation
    motor_control_led = Pin(1, Pin.OUT)  # LED to check if one of the motors is on
    motor_1_forward = Pin(9, Pin.OUT)  # Controls the turn direction of the motors
    motor_1_backward = Pin(8, Pin.OUT)
    motor_2_forward = Pin(7, Pin.OUT)
    motor_2_backward = Pin(6, Pin.OUT)

    # PWM for the control of the motors recieved power
    enable_1 = PWM(Pin(10))  # PWM motor 1
    enable_1.freq(freq)
    enable_2 = PWM(Pin(5))  # PWM motor 2
    enable_2.freq(freq)

    # Starting of methods for the control of the motors
    dc_motor = DCMotor(speed, motor_1_forward, motor_1_backward, motor_2_forward, motor_2_backward, enable_1, enable_2,
                       0, 65535)
    
    # Connect to Wifi
    wifiCom.connet_to_wifi()
    
    # Send message to Telegram
    starting_message()
    
    # Internal LED initially OFF
    motor_control_led.value(0)

    # Main loop
    while True:
        
        # Get updates from Telegram
        try:
            updates = wifiCom.get_telegram_updates(offset)

            # Process received messages
            for update in updates.get('result', []):
                message = update.get('message', {}).get('text')
                chat_id = update.get('message', {}).get('chat', {}).get('id')

                if message and chat_id:
                    print(f"Received message '{message}' from chat ID {chat_id}\n")
                    process_order(message)

                # Update the offset to the latest update ID + 1
                offset = update['update_id'] + 1

        except Exception as e:
            print('Error:', e)
            time.sleep(10)
