from machine import Pin, PWM, UART, Timer
from motorsControl import DCMotor
from wirelessCommunication import *
import dht
import time
from private_information import *
from sensors_control import *       


def interruption_handler(timer):
    """
    Time interruption handler. Sends via  MQTT the data acquiered by the DHT22.
    """
    
    try:
        temperature, humidity = get_temp_and_humidity()
        MQTT_publish(mqtt_client, topic, f"Temperature: {temperature} C, Humidity: {humidity}")
    except:
        print("Could not read DHT22 sensor")


def starting_message_telegram():
    """
    Welcome message in Telegram notifying of the current set of instructions.
    """
    
    inst_1 = "Current instruction set:\n/stop\n/go\n/back\n/left\n/right\n/clockwise\n/anticlockwise\n"
    inst_2 = "/temperature\n/humidity\n"
    instructions_set_message = inst_1 + inst_2
    
    send_telegram_message("Radio Robot Online")
    send_telegram_message(instructions_set_message)


def process_order_telegram(message: str):
    """
    Does and action depending on the message received and inform of the action taken via Telegram.
    """
    
    if "pass" in message:
        pass
    elif "/stop" in message:
        #uart.write("Stopping\n")
        motor_control_led.value(0)
        dc_motor.all_motors_off()
        send_telegram_message("Stopping")
    # Forward advance
    elif "/go" in message:
        #uart.write("Going forward\n")
        motor_control_led.value(1)
        dc_motor.all_motors_forward()
        send_telegram_message("Going forward!")
    # Backward advance
    elif "/back" in message:
        #uart.write("Going backward\n")
        motor_control_led.value(1)
        dc_motor.motor_backward()
        send_telegram_message("Going backwards!")
    # Turn left
    elif "/left" in message:
        #uart.write("To the left\n")
        motor_control_led.value(1)
        dc_motor.all_motors_off()
        dc_motor.motor_1_forward()
        send_telegram_message("Turning left")
    # Turn right
    elif "/right" in message:
        #uart.write("To the right\n")
        motor_control_led.value(1)
        dc_motor.all_motors_off()
        dc_motor.motor_2_forward()
        send_telegram_message("Turning right")
    # Rotation clockwise
    elif "/clockwise" in message:
        #uart.write("Clockwise\n")
        motor_control_led.value(1)
        dc_motor.motor_rotation_clockwise()
        send_telegram_message("Rotating clockwise")
    # Rotation anticlockwise
    elif "/anticlockwise" in message:
        #uart.write("Anticlockwise\n")
        motor_control_led.value(1)
        dc_motor.motor_rotation_anticlockwise()
        send_telegram_message("Rotating anticlockwise")
    elif "/temperature" in message:
        temperature, humidity = get_temp_and_humidity()
        send_telegram_message(f"Temperature: {temperature} Cº")
    elif "/humidity" in message:
        temperature, humidity = get_temp_and_humidity()
        send_telegram_message(f"Humidity: {humidity} %")
    else:
        print("I do not know what do you want from me\n")
        send_telegram_message("I do not know what do you want from me")
        
    message = "pass"


def process_order_mqtt(message: str, client, topic):
    """
    Does and action depending on the message received and inform of the action taken via Telegram.
    """
    
    if "pass" in message:
        pass
    elif "/stop" in message:
        motor_control_led.value(0)
        dc_motor.all_motors_off()
        # MQTT_publish(client, topic, "Stopping")
    # Forward advance
    elif "/go" in message:
        motor_control_led.value(1)
        dc_motor.all_motors_forward()
    # Backward advance
    elif "/back" in message:
        #uart.write("Going backward\n")
        motor_control_led.value(1)
        dc_motor.motor_backward()
        # MQTT_publish(client, topic, "Going backwards!")
    # Turn left
    elif "/left" in message:
        motor_control_led.value(1)
        dc_motor.all_motors_off()
        dc_motor.motor_1_forward()
        # MQTT_publish(client, topic, "Turning left")
    # Turn right
    elif "/right" in message:
        motor_control_led.value(1)
        dc_motor.all_motors_off()
        dc_motor.motor_2_forward()
        # MQTT_publish(client, topic, "Turning right")
    # Rotation clockwise
    elif "/clockwise" in message:
        motor_control_led.value(1)
        dc_motor.motor_rotation_clockwise()
        # MQTT_publish(client, topic, "Rotating clockwise")
    # Rotation anticlockwise
    elif "/anticlockwise" in message:
        motor_control_led.value(1)
        dc_motor.motor_rotation_anticlockwise()
        MQTT_publish(client, topic, "Rotating anticlockwise")
    elif "/temperature" in message:
        get_temp_and_humidity()
        MQTT_publish(client, topic, f"Temperature: {temperature} Cº")
    elif "/humidity" in message:
        get_temp_and_humidity()
        MQTT_publish(client, topic, f"Humidity: {humidity} %")
    else:
        pass
        
    message = "pass"

    
if __name__ == "__main__":
    
    # Motors configuration
    order = "0"     # Order ID
    speed = 80      # Power transfer to the motors (Range -> 70-100) 
    freq = 15000    # PWM frequency (Range -> 0-19200000)
    
    # DHT22 sensors values
    temperature = "0"
    humidity = "0"
    
    # Set the initial Telegram offset to None
    offset = None
    
    # MQTT info
    topic = "RadioTank"
    message_to_publish = "RadioTank Online"
    
    # Ultrasound sensor
    distance = 0
    
    # UART config (legacy)
    # uart = UART(0, 9600)
    
    # Input/Output pins assignation
    motor_control_led = Pin(0, Pin.OUT)  # LED to check if one of the motors is on
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
    
    # Internal LED initially OFF
    motor_control_led.value(0)
    
    # Connect to Wifi
    connet_to_wifi()
    
    # Send startind message to Telegram
    starting_message_telegram()

    # Connect to MQTT broker
    mqtt_client = MQTT_broker_connect()
    mqtt_client.set_callback(callback) # Stablish wich method will be called when there is available data
    
    # Subscribe to MQTT topic
    MQTT_subscribe(mqtt_client, topic)
    MQTT_publish(mqtt_client, topic, message_to_publish)
    
    # Configure Timer interrupts
    period = 10000  # 10 seconds
    soft_timer = Timer(mode=Timer.PERIODIC, period=period, callback=interruption_handler)
    
    # Main loop
    while True:
        
        # Check ultrasound sensor
        distance = measure_distance()
        print(distance)
        
        # Get updates from Telegram
        try:
            updates = get_telegram_updates(offset)

            # Process received messages
            for update in updates.get('result', []):
                message = update.get('message', {}).get('text')
                chat_id = update.get('message', {}).get('chat', {}).get('id')

                if message and chat_id:
                    print(f"Received message '{message}' from chat ID {chat_id}\n")
                    process_order_telegram(message)

                # Update the offset to the latest update ID + 1
                offset = update['update_id'] + 1

        except Exception as e:
            print('Telegram Error:', e)
            
        # Get MQTT messages
        try:
            mqtt_client.check_msg()
            order = get_mqtt_message()
            
            # If it the chasis is far from an obstacle
            if distance > 30:
                order = order[0]
            # If the chasis is close to an obstacle
            else:
                order = "/stop"
                
            process_order_mqtt(order, mqtt_client, topic)
            
            #process_order_telegram_mqtt(read_mqtt_message)
        except Exception as e:
            mqtt_client.disconnect()
            print('MQTT Error:', e)

        