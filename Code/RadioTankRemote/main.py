import tkinter as tk
from mqtt_communication import *


class RemoteControllerApp:
    def __init__(self, window, topic, start_message):
        self.window = window
        self.topic = topic
        self.start_message = start_message
        self.window.title("RadioTank Remote Controller")

        # Text display
        self.text_display = tk.Label(window, text=start_message, font=('Arial', 10, 'bold'))
        self.text_display.grid(row=2, column=1, columnspan=3, pady=10)

        # MQTT communication
        self.client = mqtt_broker_connect()
        mqtt_subscribe(self.client, topic)
        mqtt_publish(self.client, self.topic, self.start_message)

        # Creation of the buttons
        for i in range(1, 7):
            # Up button
            if i == 1:
                btn_text = '\u02C4'  # Unicode Code
                row_num, col_num = self.get_coordinates(i)
            # Left button
            elif i == 2:
                btn_text = '\u02C2'
                row_num, col_num = self.get_coordinates(i)
            # Down button
            elif i == 3:
                btn_text = '\u02C5'
                row_num, col_num = self.get_coordinates(i)
            # Right button
            elif i == 4:
                btn_text = '\u02C3'
                row_num, col_num = self.get_coordinates(i)
            # Stop button
            elif i == 5:
                btn_text = "Stop"
                row_num, col_num = self.get_coordinates(i)
            # Sensor button
            else:
                btn_text = "Sensor"
                row_num, col_num = self.get_coordinates(i)

            btn = tk.Button(window, text=btn_text, command=lambda num=i: self.used_button(num),
                            font=('Arial', 12, 'bold'))
            btn.grid(row=row_num, column=col_num, padx=10, pady=10)

    def get_coordinates(self, index):
        # Coordinates of the buttons

        # Up button
        if index == 1:
            return 0, 1
        # Left button
        elif index == 2:
            return 1, 0
        # Down button
        elif index == 3:
            return 1, 1
        # Right button
        elif index == 4:
            return 1, 2
        # Stop button
        elif index == 5:
            return 0, 7
        # Sensor button
        else:
            return 0, 8

    def used_button(self, num):
        """
        Returns the number of the used button

        Inputs:
        - num: Number ID of the button used
        Returns:
        - None
        """

        print(f"Used Button {num}")
        message = ""

        if num == 1:
            message = "/go"
        elif num == 2:
            message = "/left"
        elif num == 3:
            message = "/back"
        elif num == 4:
            message = "/right"
        elif num == 5:
            message = "/stop"
        elif num == 6:
            message = "/sensor"
        elif num == 7:
            message = "Order Unknown"
        else:
            self.text_display.config(text="Temperature: " + message + " ºC")

        try:
            mqtt_publish(self.client, self.topic, message)
        except OSError as e:
            print("Error publishing:", e)


if __name__ == "__main__":
    topic = "RadioTank"
    start_message = "Remote Online"

    # Main window
    remote_window = tk.Tk()
    mando = RemoteControllerApp(remote_window, topic, start_message)
    # remote_window.after(1000, )

    # Main loop of the app
    remote_window.mainloop()
