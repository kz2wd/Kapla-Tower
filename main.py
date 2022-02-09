# Public import
import pydobot
from serial.tools import list_ports

# Personal import
from System import *


if __name__ == "__main__":
    print("Starting robot")

    available_ports = list_ports.comports()
    print(f"available ports: {[x.device for x in available_ports]}")

    # TODO : setup devices correctly
    device1 = pydobot.Dobot(port=available_ports[0].device, verbose=True)
    device2 = pydobot.Dobot(port=available_ports[1].device, verbose=True)
    device3 = pydobot.Dobot(port=available_ports[2].device, verbose=True)
    cam = 0

    system = System(device1, device2, device3, cam)
    system.start()

    device1.close()
    device2.close()
    device3.close()
