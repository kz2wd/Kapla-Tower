class Position:
    def __init__(self, x: float, y: float, z: float):
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def get_hover(self):
        # 50 mm up
        return Position(self.x, self.y + 50, self.z)

    def clone(self):
        return Position(self.x, self.y, self.z)


# Check KaplaManual in resources if you don't understand theses
# active face is the one on the ground / up
class Faces:
    big_face = "big_face"
    medium_face = "medium_face"
    small_face = "small_face"
