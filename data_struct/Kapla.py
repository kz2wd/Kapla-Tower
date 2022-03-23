from data_struct.General import *


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
