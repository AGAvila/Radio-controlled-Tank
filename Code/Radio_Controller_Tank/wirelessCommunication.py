import network
import time
import urequests
from private_information import *
from umqtt.simple import MQTTClient

offset_id = 0

class wifiCom:
    
    def connet_to_wifi():
        """
        Connect to a Wifi net.
        
        Inputs:
        - None
        Returns:
        - None
        """
        
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)

        # Wait for connect or fail
        max_wait = 10
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
        
        max_wait -= 1
        print('Waiting for connection...')
        time.sleep(1)

        # Handle connection error
        if wlan.status() != 3:
            raise RuntimeError('Network connection failed')
        else:
            print('Connected')
            status = wlan.ifconfig()
            print( 'ip = ' + status[0] )
    
    def send_telegram_message(message: str):
        """
        Sends a message to Telegram.
        
        Inputs:
        - message: String to be sent by the Telegram bot to the user
        Returns:
        - True if there was no error or False the other case around
        """
        
        send_URL = "https://api.telegram.org/bot" + bot_token
        data = {'chat_id': chat_id, 'text': message}
        
        try:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            response = urequests.post(send_URL + '/sendMessage', json=data, headers=headers)
            response.close()
            return True
        except:
            return False
    
    def get_telegram_updates(offset=None):
        """
        Get the last message from the Telegram conversation with the bot.
        
        Inputs:
        - offset: Number of the message to get from the conversation
        Return:
        - Indicated message in JSON format or False case a error happends in the process
        """
        
        get_url = 'https://api.telegram.org/bot' + bot_token + '/getUpdates'
        
        if offset is not None:
            get_url += f'?offset={offset}'
        
        try:
            response = urequests.get(get_url)
            return response.json()
        except:
            return None
    
    def callback(topic, msg):
        """
        Handles received messages from MQTT server. When a message is publish in a topic,
        the message stablish by this method will be printed
        
        Inputs:
        - topic: Topic to subscribe to
        - msg: Message to print
        Return:
        - None
        """
        
        print("Mensaje recibido en el topic {}: {}".format(topic, msg))
    
    def MQTT_broker_connect():
        """
        Connects to MQTT broker
        
        Inputs:
        - None
        Return:
        - Instance of a client connected to MQTT broker
        """
        
        try:
            # Instance of the MQTT client
            mqtt_client = MQTTClient(
                client_id=b"RaspberryPiPico",
                server=MQTT_server_hostname,
                user=MQTT_client_ID,
                password=MQTT_client_password,
                port=0,
                keepalive=7200,
                ssl=True,
                ssl_params={'server_hostname': MQTT_server_hostname})
            # Connect to MQTT broker
            mqtt_client.connect()
            print("Connected to MQTT broker")
            return mqtt_client
        
        except OSError as e:
            print("Error connecting to MQTT broker:", e)
            return None
        
    def MQTT_subscribe(mqtt_client, MQTT_topic: str):
        """
        Subscribe to MQTT topic
        
        Inputs:
        - mqtt_client: Instance of a client connected to MQTT broker
        - topic: Topic to subscribe to
        Returns:
        - None
        """
        
        # Subscribe to topic
        try:
            mqtt_client.subscribe(MQTT_topic)
        except Exception as e:
            print('Error subscribing:', e)
    
    def MQTT_publish(mqtt_client: str, topic: str, message: str):
        """
        Publish in a MQTT topic
        
        Inputs:
        - mqtt_client: Instance of a client connected to MQTT broker
        - topic: Topic to subscribe to
        - message: Message to be publish in the topic
        Returns:
        - None
        """
        
        try:
            mqtt_client.publish(topic, message)
            print("Publish Done")
        except Exception as e:
            print('Error publishing:', e)
    