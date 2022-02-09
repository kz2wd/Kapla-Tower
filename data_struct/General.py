class Position:
    def __init__(self, x: float, y: float, z: float):
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def get_hover(self):
        # 15 mm up
        return Position(self.x, self.y + 15, self.z)

    def clone(self):
        return Position(self.x, self.y, self.z)


class Faces:
    big_face = "big_face"
    medium_face = "medium_face"
    small_face = "small_face"
