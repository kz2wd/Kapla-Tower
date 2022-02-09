import pydobot
from data_struct.Kapla import *
from data_struct.Kapla import RealKapla


class Arm:
    def __init__(self, device: pydobot.Dobot, pos: Position):
        self.device: pydobot.Dobot = device
        self.pos: Position = pos

    def move_kapla(self, kapla: RealKapla, goal_pos: Position):
        self.grab_kapla(kapla)
        self.drop_kapla(kapla, goal_pos)

    def grab_kapla(self, kapla: RealKapla):
        # Todo : Go to pos too (hover pos, then grab pos)

        # . . .

        # Go to hover position
        x, y, z = kapla.position.get_hover()

        # Determine the angle here !
        self.device.move_to(x, y, z, 0)

        # Go to grab position
        x, y, z = kapla.get_grab_position()

        # Determine the angle here !
        self.device.move_to(x, y, z, 0)

        self.device.grip(True)

    def drop_kapla(self, kapla: RealKapla, destination: Position):
        # Go to hover position
        x, y, z = destination.get_hover()
        # Determine the angle here !
        self.device.move_to(x, y, z, 0)

        x, y, z = destination
        # Determine the angle here !
        self.device.move_to(x, y, z, 0)

        self.device.grip(False)


class Conveyor:
    def __init__(self, device, pos: Position):
        self.pos: Position = pos
        self.device = device

    def activate(self):
        pass

    def deactivate(self):
        pass

    def get_drop_pos(self) -> Position:
        return Position(0, 0, 0)

