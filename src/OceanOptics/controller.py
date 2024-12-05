# Communication with device
import pyvisa

V_range = 3.3  # 0 tot 3.3V
resolution = 1024  # stapjes

# Resource manager
rm = pyvisa.ResourceManager("@py")


def list_resources():
    """Lists available resources.

    Returns:
        list: list containing the resources
    """
    rm = pyvisa.ResourceManager("@py")
    ports = rm.list_resources()

    return ports


class ArduinoVISADevice:
    """Class which allows for communication with an arduino."""

    def __init__(self, port):
        """Opens the arduino port.

        Args:
            port (string): port of the arduino
        """
        self.device = rm.open_resource(
            port, read_termination="\r\n", write_termination="\n"
        )

    def get_identification(self):
        """Finds the identification string of the connected device. Disconnects if the device isn't an arduino.

        Returns:
            string: the identification string
        """
        self.identification = self.device.query("*IDN?")

        if self.identification == "Arduino VISA firmware v1.1.0":
            print("Device connected")
        else:
            print("Device not connected")
            exit

        return self.identification

    def set_output_value(self, value):
        """Sets the output value on channel 0.

        Args:
            value (integer): output value on channel 0
        """
        self.device.query(f"OUT:CH0 {value}")

    def get_input_value(self, channel):
        """Measures the analog value on a given channel.

        Args:
            channel (integer): channel on the arduino

        Returns:
            float: analog value on the given channel
        """
        Analog = float(self.device.query(f"MEAS:CH{channel}?"))

        return Analog

    def get_input_voltage(self, channel):
        """Meausres the analog value on a given channel and converts the value to voltage.

        Args:
            channel (integer): channel on the arduino

        Returns:
            float: voltage on the given channel
        """
        Analog = self.get_input_value(channel)

        Voltage = self.A_to_V(Analog)

        return Voltage

    def get_output_value(self):
        """Finds the output value on channel 0 of the arduino.

        Returns:
            float: output value on channel 0
        """
        self.output_value = float(self.device.query("OUT:CH0?"))

        return self.output_value

    def A_to_V(self, A):
        """Converts an analog value A to voltage.

        Args:
            A (float): analog value

        Returns:
            float: voltage
        """
        V = A * (V_range / resolution)

        return V

    def close_device(self):
        """Closes the arduino device."""
        self.device.close()


if __name__ == "__main__":
    print(list_resources())
