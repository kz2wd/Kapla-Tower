import pydobot
from data_struct.Kapla import *


class Mover:
    def __init__(self, device: pydobot.Dobot):
        self.device: pydobot.Dobot = device

    def move(self, kapla: RealKapla, new_pos: Position):

        # Go to hover position
        x, y, z = kapla.get_hover_position()

        # Determine the angle here !
        self.device.move_to(x, y, z, 0)

        # Go to grab position
        kapla.get_grab_position()

        # grab
        self.device.grip(True)

        # go to hover position

        # go to destination

        # drop
        self.device.grip(False)

