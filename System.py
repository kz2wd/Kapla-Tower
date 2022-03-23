import time

from data_struct.General import Position, Faces
import dobot_extensions

from logic import KaplaOrganizer


class System:
    # TODO : setup pos here
    shop_pos: Position = Position(180.06, 91.33, -46.74)
    loader_pos: Position = Position(0, 0, 0)
    builder_pos: Position = Position(0, 0, 0)
    conveyor_pos_load: Position = Position(178.29, -36.15, 33.56)
    conveyor_pos_unload: Position = Position(189.17, 69.69, 36.42)
    construction_pos: Position = Position(-8.00, -266.30, -49.64)
    # Add rotation piece localisation

    def __init__(self, loader: dobot_extensions.Dobot, builder: dobot_extensions.Dobot):
        self.loader: dobot_extensions.Dobot = loader
        self.builder: dobot_extensions.Dobot = builder

        # self.loader.set_home(250.0, 0.0, 100.0)
        # self.loader.wait_for_cmd(self.loader.home())

        self.builder.set_home(250.0, 0.0, 100.0)
        self.builder.wait_for_cmd(self.builder.home())

    def start(self):

        # Test purpose

        # self.loader.speed(10, 10)
        self.builder.speed(10, 10)
        input("Enter to start !")

        for pos, angle, face in KaplaOrganizer.get_sequence():
            print(f"Next goal : {pos} {angle} {face}")
            # Loading part
            # self.get_kapla_from_shop()
            # self.loader.wait_for_cmd(self.loader.conveyor_belt_distance(100, 500, -1, 0))

            midpoint = Position(151.28, -160.95, 150.53)
            self.catch(self.builder, System.conveyor_pos_unload, [midpoint])

            obj_x, obj_y, obj_z = System.construction_pos.clone()
            x, y, z = pos
            obj_x += x
            obj_y += y
            obj_z += z
            self.drop(self.builder, Position(obj_x, obj_y, obj_z), [midpoint], angle)

            if input("Enter to continue, q to quit").lower() == 'q':
                break
        # return
        #
        # for pos, angle, face in KaplaOrganizer.get_sequence():
        #     break

    def get_kapla_from_shop(self):
        midpoint = Position(186.77, 60.88, 116.95)
        self.catch(self.loader, System.shop_pos, [midpoint])
        self.drop(self.loader, System.conveyor_pos_load, [midpoint])
        self.loader.wait_for_cmd(self.loader.move_to(*midpoint))

    def catch(self, device: dobot_extensions.Dobot, pos: Position, midpoints: list[Position], angle: float = 0):
        self.action(device, pos, True, midpoints, angle)

    def drop(self, device: dobot_extensions.Dobot, pos: Position, midpoints: list[Position], angle: float = 0):
        self.action(device, pos, False, midpoints, angle)

    def action(self, device: dobot_extensions.Dobot, pos: Position, suck: bool, midpoints: list[Position], angle: float = 0):
        for x, y, z in midpoints:
            device.wait_for_cmd(device.move_to(x, y, z))
        device.wait_for_cmd(device.move_to(*(pos.get_hover())))
        device.wait_for_cmd(device.move_to(*pos, angle))
        device.wait_for_cmd(device.suck(suck))
        time.sleep(1)
        device.wait_for_cmd(device.move_to(*(pos.get_hover())))
