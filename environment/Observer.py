from data_struct.Kapla import *
from data_struct.General import *
from System import System
from data_struct.Kapla import *
from data_struct.Kapla import RealKapla, GoalKapla


class Observer:
    def __init__(self, cam):
        self.cam = cam

    def check_position(self, kapla: RealKapla):
        # Todo
        pass

    def get_shop_kapla(self) -> RealKapla:
        # Todo
        # Pos to search for near kapla
        # System.shop_pos

        return RealKapla(System.shop_pos, 0, Faces.big_face)

    def get_real_kapla_pos(self, kapla: RealKapla) -> GoalKapla:
        # Todo
        # Find a kapla near the supposed position of the furnished SupposedKapla
        # Do not use SupposedKapla.get_grab_position(), as it call this function

        return GoalKapla(Position(0, 0, 0), 0, Faces.big_face)
