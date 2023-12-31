import network
import time
import urequests

class wifiCom:
    
    def connet_to_wifi(ssid: str, password: str):
        """
        Connect to a Wifi net.
        
        Inputs:
        - ssid: ID of the net
        - password: Password of the net
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
    
    def send_telegram_message(bot_token: str, chat_id: str, message: str):
        """
        Sends a message to Telegram.
        
        Inputs:
        - token: Bot token
        - chat_id: Chat ID of the conversation with the bot
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
    
