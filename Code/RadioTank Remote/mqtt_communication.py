import paho.mqtt.client as paho
from paho import mqtt

from private_information import *

message = ""  # Stored the MQTT message read from the topic


def mqtt_broker_connect():
    """
    Connects to MQTT broker

    Inputs:
    - None
    Return:
    - Instance of a client connected to MQTT broker
    """

    port = 8883

    try:
        client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
        client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        client.username_pw_set(MQTT_client_ID, MQTT_client_password)
        client.connect(MQTT_server_hostname, port=port)
        return client

    except OSError as e:
        print("Error connecting to MQTT broker:", e)
        return None


def mqtt_subscribe(client, topic: str):
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
        client.on_message = on_message
        client.subscribe(topic, qos=1)
    except Exception as e:
        print('Error subscribing:', e)


def mqtt_publish(client, topic: str, message: str):
    """
    Publish in a MQTT topic

    Inputs:
    - mqtt_client: Instance of a client connected to MQTT broker
    - topic: Topic to subscribe to
    - message: Message to be published in the topic
    Returns:
    - None
    """

    try:
        client.publish(topic, payload=message, qos=1)
        print("Publish Done")
    except Exception as e:
        print('Error publishing:', e)


def on_message(client, userdata, msg):
    """

    """

    print(f"Mensaje recibido en el tema '{msg.topic}': {msg.payload.decode()}")
    return msg.payload.decode()
