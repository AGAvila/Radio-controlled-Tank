class DCMotor:

    def __init__(self, speed, pin1, pin2, pin3, pin4, enable_pin1, enable_pin2, min_duty=0, max_duty=65535):
        # Pines control side 1
        self.pin1 = pin1
        self.pin2 = pin2
        # Pines control side 2
        self.pin3 = pin3
        self.pin4 = pin4

        self.enable_pin1 = enable_pin1
        self.enable_pin2 = enable_pin2
        self.min_duty = min_duty
        self.max_duty = max_duty

        self.speed = speed

    def duty_cycle(self):
        """
        Calculation of the duty cycle from the percentage of speed.

        Returns:
        - None
        """

        if self.speed <= 0 or self.speed > 100:
            duty_cycle = 0
        else:
            duty_cycle = int(self.min_duty + (self.max_duty - self.min_duty) * ((self.speed - 1) / (100 - 1)))

        return duty_cycle

    def all_motors_off(self):
        """
        Turn OFF all motors.

        Returns:
        - None
        """

        self.enable_pin1.duty_u16(0)
        self.enable_pin2.duty_u16(0)
        self.pin1.value(0)
        self.pin2.value(0)
        self.pin3.value(0)
        self.pin4.value(0)

    def all_motors_forward(self):
        """
        Turn ON all motors and make the chassis go forwards.

        Returns:
        - None
        """

        self.enable_pin1.duty_u16(self.duty_cycle())
        self.enable_pin2.duty_u16(self.duty_cycle())
        self.pin1.value(1)
        self.pin2.value(0)
        self.pin3.value(0)
        self.pin4.value(1)

    def motor_backward(self):
        """
        Turn ON all motors and make the chassis go backwards.

        Returns:
        - None
        """

        self.enable_pin1.duty_u16(self.duty_cycle())
        self.enable_pin2.duty_u16(self.duty_cycle())
        self.pin1.value(0)
        self.pin2.value(1)
        self.pin3.value(1)
        self.pin4.value(0)

    def motor_1_forward(self):
        """
        Turn ON motor 1. No change is made to the state of motor 2.

        Returns:
        - None
        """

        self.enable_pin1.duty_u16(self.duty_cycle())
        self.enable_pin2.duty_u16(0)
        self.pin1.value(1)
        self.pin2.value(0)

    def motor_2_forward(self):
        """
        Turn ON motor 2. No change is made to the state of motor 1.

        Returns:
        - None
        """

        self.enable_pin1.duty_u16(0)
        self.enable_pin2.duty_u16(self.duty_cycle())
        self.pin3.value(0)
        self.pin4.value(1)

    def motor_rotation_clockwise(self):
        """
        Turn ON motor 1 rotating backwards and motor 2 rotating forwards.

        Returns:
        - None
        """

        self.enable_pin1.duty_u16(self.duty_cycle())
        self.enable_pin2.duty_u16(self.duty_cycle())
        self.pin1.value(0)
        self.pin2.value(1)
        self.pin3.value(0)
        self.pin4.value(1)

    def motor_rotation_anticlockwise(self):
        """
        Turn ON motor 1 rotating forwards and motor 2 rotating backwards.

        Returns:
        - None
        """

        self.enable_pin1.duty_u16(self.duty_cycle())
        self.enable_pin2.duty_u16(self.duty_cycle())
        self.pin1.value(1)
        self.pin2.value(0)
        self.pin3.value(1)
        self.pin4.value(0)
