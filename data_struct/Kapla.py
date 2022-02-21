from General import *
from System import *


class Kapla:
    # Dimensions in mm
    length: int = 70
    width: int = 24
    depth: int = 20

    def __init__(self, pos: Position, angle: float, face: Faces):
        self.position: Position = pos.clone()
        self.angle: float = angle
        # Face facing the sky
        self.face: Faces = face


# class representing a logic position of a Kapla, used for desired positions
class GoalKapla(Kapla):
    def __init__(self, pos: Position, angle: float, face: Faces):
        super().__init__(pos, angle, face)


# class representing a real Kapla in the robotic system
class RealKapla(Kapla):
    def __init__(self, pos: Position, angle: float, face: Faces):
        super().__init__(pos, angle, face)

    def get_grab_position(self) -> GoalKapla:
        return System.world_watcher.get_real_kapla_pos(self)
