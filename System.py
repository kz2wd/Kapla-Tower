import time

from data_struct.General import Position
import dobot_extensions

from logic import KaplaOrganizer


class System:
    # TODO : setup pos here
    shop_pos: Position = Position(180.06, 91.33, -46.74)
    loader_pos: Position = Position(0, 0, 0)
    builder_pos: Position = Position(0, 0, 0)
    conveyor_pos_load: Position = Position(178.29, -36.15, 33.56)
    conveyor_pos_unload: Position = Position(0, 0, 0)
    # Add rotation piece localisation

    def __init__(self, loader: dobot_extensions.Dobot, builder: dobot_extensions.Dobot):
        self.loader: dobot_extensions.Dobot = loader
        self.builder: dobot_extensions.Dobot = builder

        self.loader.set_home(250.0, 0.0, 100.0)
        self.loader.wait_for_cmd(self.loader.home())

    def start(self):

        # Test purpose
        midpoint = Position(186.77, 60.88, 116.95)
        self.loader.speed(10, 10)
        input("Enter to start !")

        while True:
            self.catch(self.loader, System.shop_pos, [midpoint])

            self.drop(self.loader, System.conveyor_pos_load, [midpoint])

            # self.loader.wait_for_cmd(self.loader.home())
            self.loader.wait_for_cmd(self.loader.move_to(*midpoint))

            self.loader.wait_for_cmd(self.loader.conveyor_belt_distance(100, 500, -1, 0))

            if input("Enter to continue, q to quit").lower() == 'q':
                break
        # return
        #
        # for pos, angle, face in KaplaOrganizer.get_sequence():
        #     break

    def catch(self, device: dobot_extensions.Dobot, pos: Position, midpoints: list[Position]):
        self.action(device, pos, True, midpoints)

    def drop(self, device: dobot_extensions.Dobot, pos: Position, midpoints: list[Position]):
        self.action(device, pos, False, midpoints)

    def action(self, device: dobot_extensions.Dobot, pos: Position, suck: bool, midpoints: list[Position]):
        for x, y, z in midpoints:
            device.wait_for_cmd(device.move_to(x, y, z))
        device.wait_for_cmd(device.move_to(*(pos.get_hover())))
        device.wait_for_cmd(device.move_to(*pos))
        device.wait_for_cmd(device.suck(suck))
        time.sleep(.3)
        device.wait_for_cmd(device.move_to(*(pos.get_hover())))
