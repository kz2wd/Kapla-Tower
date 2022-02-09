import pydobot
from serial.tools import list_ports

if __name__ == "__main__":
    print("Starting robot")

    available_ports = list_ports.comports()
    print(f"available ports: {[x.device for x in available_ports]}")
    port = available_ports[0].device
    device = pydobot.Dobot(port=port, verbose=True)
    device.close()

    
