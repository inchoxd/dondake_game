import serial
import serial.tools.list_ports

import json


class SerialDevice:
    def check_port(self) -> bool:
        if serial.tools.list_ports.comports():
            return True
        else:
            return False


    def get_data(self) -> dict:
        read_serial = serial.Serial('/dev/ttyUSB0', 115200, timeout=3)
        readline_data = read_serial.readline().decode('utf-8')
        data = json.loads(readline_data.replace('\r\n', ''))
        return data


    def send_data(self, data:str) -> None:
        send_serial = serial.Serial('/dev/ttyUSB0', 115200, timeout=3)
        send_serial.write(data.encode('utf-8'))


if __name__ == '__main__':
    SerialDevice().get_data()
