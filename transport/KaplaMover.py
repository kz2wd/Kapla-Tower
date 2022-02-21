import pydobot
from data_struct.Kapla import *
from data_struct.Kapla import RealKapla


# Class representing a robot Arm
class Arm:
    def __init__(self, device: pydobot.Dobot, pos: Position):
        self.device: pydobot.Dobot = device
        self.pos: Position = pos

    def move_kapla(self, kapla: RealKapla, goal_pos: GoalKapla):
        self.grab_kapla(kapla)
        self.drop_kapla(goal_pos)

    def grab_kapla(self, kapla: RealKapla):
        # Go to hover position
        objective = kapla.get_grab_position()
        x, y, z = objective.position.get_hover()

        self.device.move_to(x, y, z, objective.angle)

        # Go to grab position
        x, y, z = objective.position

        self.device.move_to(x, y, z, objective.angle)

        # grab
        self.device.grip(True)

    def drop_kapla(self, destination: GoalKapla):
        # Go to hover position
        x, y, z = destination.position.get_hover()
        self.device.move_to(x, y, z, destination.angle)

        # Go to release position
        x, y, z = destination.position
        self.device.move_to(x, y, z, destination.angle)

        # release
        self.device.grip(False)


# Class representing the conveyor
class Conveyor:
    def __init__(self, device, pos: Position):
        self.pos: Position = pos
        self.device = device

    def activate(self):
        pass

    def deactivate(self):
        pass

    def get_drop_pos(self) -> GoalKapla:
        # Todo
        return GoalKapla(Position(0, 0, 0), 0, Faces.big_face)

