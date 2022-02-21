from data_struct.Kapla import RealKapla
from transport.KaplaMover import *
from environment.Observer import *


class System:
    # TODO : setup pos here
    shop_pos: Position = Position(0, 0, 0)
    loader_pos: Position = Position(0, 0, 0)
    builder_pos: Position = Position(0, 0, 0)
    conveyor_pos: Position = Position(0, 0, 0)
    world_watcher: Observer = None

    def __init__(self, loader: pydobot.Dobot, builder: pydobot.Dobot, conveyor, cam):
        self.loader: Arm = Arm(loader, System.loader_pos)
        self.builder: Arm = Arm(builder, System.builder_pos)
        self.conveyor: Conveyor = Conveyor(conveyor, System.conveyor_pos)
        System.world_watcher = Observer(cam)

    def start(self):

        # Todo : Get Kapla sequence using KaplaOrganizer
        # Todo : For each Kapla in the sequence : request a new kapla,

        pass

    def request_new_kapla(self) -> RealKapla:
        kapla: RealKapla = System.world_watcher.get_shop_kapla()

        self.loader.move_kapla(kapla, self.conveyor.get_drop_pos())

        return kapla
