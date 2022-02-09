from General import *


class Kapla:
    # Dimensions in mm
    length: int = 70
    width: int = 24
    depth: int = 20

    def __init__(self, pos: Position, angle: float, face: Faces):
        self.position: Position = pos
        self.angle: float = angle
        self.face: Faces = face


class GoalKapla(Kapla):
    def __init__(self, pos: Position, angle: float, face: Faces):
        super().__init__(pos, angle, face)


class RealKapla(Kapla):
    def __init__(self, pos: Position, angle: float, face: Faces):
        super().__init__(pos, angle, face)

    def get_grab_position(self):
        pass

    def get_hover_position(self):
        pass
