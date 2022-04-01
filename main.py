# Public import
from serial.tools import list_ports

import Visualizer
import dobot_extensions

# Personal import
from System import *

VISUALIZE = False


if __name__ == "__main__":
    print("Starting robot")

    available_ports = list_ports.comports()
    print(f"available ports: {[x.device for x in available_ports]}")

    # setup devices correctly
    device1 = dobot_extensions.Dobot(port=available_ports[0].device)
    device2 = dobot_extensions.Dobot(port=available_ports[1].device)

    system = System(device1, device2, device1)

    if VISUALIZE:
        Visualizer.visualize(system.start())
    else:
        system.start()

    device1.close()
    device2.close()
