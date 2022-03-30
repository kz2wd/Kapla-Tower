import time

import pydobot.dobot

from data_struct.General import Position, Faces
import dobot_extensions

from logic import KaplaOrganizer

tempo = 0.2


AUTO = True
DEBUG = True
SPEED = 10
ACCELERATION = 10
TAKE_SPEED = 100
TAKE_ACCELERATION = 100


class System:
    # TODO : setup pos here
    shop_pos: Position = Position(180.06, 91.33, -46.74)
    conveyor_pos_load: Position = Position(178.29, -36.15, 33.56)
    conveyor_pos_unload: Position = Position(189.17, 69.69, 36.42)
    construction_pos: Position = Position(-98.85, -298.12, -71.17)
    flipper_small_face: Position = Position(187.19, -76.02, 2.87)
    flipper_big_face: Position = Position(188.20, -60.77, -8.63)
    # Add rotation piece localisation

    def __init__(self, loader: dobot_extensions.Dobot, builder: dobot_extensions.Dobot, conveyor_handler):
        self.loader: dobot_extensions.Dobot = loader
        self.builder: dobot_extensions.Dobot = builder
        self.conveyor_handler: dobot_extensions.Dobot = conveyor_handler

        # self.loader.set_home(250.0, 0.0, 100.0)
        # self.loader.wait_for_cmd(self.loader.home())

        self.builder.set_home(250.0, 0.0, 100.0)
        self.builder.wait_for_cmd(self.builder.home())

    def start(self):

        # Test purpose

        # self.loader.speed(10, 10)
        self.builder.speed(SPEED, ACCELERATION)
        input("Enter to start !")

        for pos, angle, face in KaplaOrganizer.get_sequence():
            if DEBUG:
                print(f"Next goal : {pos} {angle} {face}")
            # Loading part
            # self.get_kapla_from_shop(face)

            # Travel on conveyor
            # self.conveyor_handler.wait_for_cmd(self.conveyor_handler.conveyor_belt_distance(100, 500, -1, 0))

            # Rotation
            retaking_point = System.conveyor_pos_unload

            if face == Faces.big_face:
                retaking_point = System.flipper_big_face
                self.conveyor_handler.wait_for_cmd(self.conveyor_handler.conveyor_belt_distance(100, 250, -1, 0))
            elif face == Faces.small_face:
                retaking_point = System.flipper_small_face
                self.conveyor_handler.wait_for_cmd(self.conveyor_handler.conveyor_belt_distance(100, 250, -1, 0))

            midpoint = Position(151.28, -160.95, 170.53)
            midpoint2 = Position(185.53, -57.64, 152.09)
            catching_angle = -90
            self.catch(self.builder, retaking_point, [midpoint, midpoint2], catching_angle)

            obj_x, obj_y, obj_z = System.construction_pos
            x, y, z = pos
            obj_x += x
            obj_y += y
            obj_z += z
            self.drop(self.builder, Position(obj_x, obj_y, obj_z), [midpoint], catching_angle + angle)

            if not AUTO:
                if input("Enter to continue, q to quit").lower() == 'q':
                    break
        # return
        #
        # for pos, angle, face in KaplaOrganizer.get_sequence():
        #     break

    def get_kapla_from_shop(self, face: Faces):

        angle = 0
        if face == Faces.small_face:
            angle = 90

        midpoint = Position(186.77, 60.88, 116.95)
        self.catch(self.loader, System.shop_pos, [midpoint])
        self.drop(self.loader, System.conveyor_pos_load, [midpoint], angle)
        self.loader.wait_for_cmd(self.loader.move_to(*midpoint))

    def catch(self, device: dobot_extensions.Dobot, pos: Position, midpoints: list[Position], angle: float = 0):
        self.action(device, pos, True, midpoints, angle)

    def drop(self, device: dobot_extensions.Dobot, pos: Position, midpoints: list[Position], angle: float = 0):
        self.action(device, pos, False, midpoints, angle)

    def action(self, device: dobot_extensions.Dobot, pos: Position, suck: bool, midpoints: list[Position], angle: float = 0):

        for x, y, z in midpoints:
            if DEBUG:
                print("Going to midpoint")
            device.wait_for_cmd(device.move_to(x, y, z, angle))
            if DEBUG:
                print("Midpoint reached")
        time.sleep(tempo)
        if DEBUG:
            print("WANTED ANGLE", angle)

        if DEBUG:
            print("Actual pose :", end="")
            pretty_print_pose(device.get_pose())
        if DEBUG:
            print(f" objective (hover) : {pos.get_hover()}")
        device.wait_for_cmd(device.move_to(*(pos.get_hover()), angle))
        if DEBUG:
            print("Reached : ", end="")
            pretty_print_pose(device.get_pose())
        if not AUTO:
            input("Done ... Continue ?")
            print("\n")
        time.sleep(tempo)

        if DEBUG:
            print("Actual pose :", end="")
        pretty_print_pose(device.get_pose())
        if DEBUG:print(f" objective (real) : {pos}")
        device.speed(TAKE_SPEED, TAKE_ACCELERATION)
        device.wait_for_cmd(device.move_to(*pos, angle, mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
        if DEBUG:
            print("Reached : ", end="")
            pretty_print_pose(device.get_pose())
        if not AUTO:
            input("Done ... Continue ?")
            print("\n")
        time.sleep(tempo)

        if DEBUG:
            print("Actual pose :", end="")
            pretty_print_pose(device.get_pose())
        if DEBUG:print(f" objective (suck) : suck")
        device.wait_for_cmd(device.suck(suck))
        if DEBUG:
            print("Reached : ", end="")
            pretty_print_pose(device.get_pose())
        if not AUTO:
            input("Done ... Continue ?")
            print("\n")
        time.sleep(1)

        if DEBUG:
            print("Actual pose :", end="")
            pretty_print_pose(device.get_pose())
        if DEBUG:print(f" objective (hover) : {pos.get_hover()}")
        device.wait_for_cmd(device.move_to(*(pos.get_hover()), angle, mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
        if DEBUG:
            print("Reached : ", end="")
            pretty_print_pose(device.get_pose())
        if not AUTO:
            input("Done ... Continue ?")
            print("\n")
        time.sleep(tempo)
        device.speed(SPEED, ACCELERATION)


def pretty_print_pose(pose):
    print('(x=%0.2f, y=%0.2f, z=%0.2f r=%0.2f)' % \
          (pose.position.x, pose.position.y, pose.position.z, pose.position.r), end="")
