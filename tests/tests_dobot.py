from serial.tools import list_ports
from pydobot import Dobot
import pydobot
import time
import sys


class Position:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r


def pretty_print_pose(pose):
    (x, y, z, r, j1, j2, j3, j4) = pose
    print('(x=%0.2f, y=%0.2f, z=%0.2f r=%0.2f)' % \
          (x, y, z, r))


print('- liste des ports COM:')
ports = list(list_ports.comports())
for p in ports:
    print(p)

print('- connexion au robot ...', end='')
sys.stdout.flush()
port = 'COM3'  # replacez ici COM3 par votre port de communication
device = Dobot(port=port)
print('[ok]')
sys.stdout.flush()

print('- position du robot: ', end='')
sys.stdout.flush()
pose = device.pose()
pretty_print_pose(pose)
print()
print(pose)
position = Position(*pose[:4])

print('- mouvement en Z ... ', end='')
sys.stdout.flush()
device.move_to(position.x, position.y, position.z + 40, position.r, wait=True)
print('[ok]')
# l'usage de wait_for_cmd (ligne suivante) permet d'attendre que la
# commande soit exécutée.  Ca n'est pas obligatoire, sans cela le
# robot lance le déplacement et rend la main au programme
# immédiatement sans attendre que le déplacement effectif soit fini.
print('- mouvement en Y ... ', end='')
sys.stdout.flush()
device.move_to(position.x, position.y + 20, position.z + 40, position.r)
# ici la commande rend la main immédiatement sans attendre la fin du déplacement
device.move_to(position.x, position.y, position.z + 40, position.r, wait=True)
# ici on attend la fin
print('[ok]')
print('- mouvement en X ... ', end='')
sys.stdout.flush()
device.move_to(position.x + 20, position.y, position.z + 40, position.r)
device.move_to(position.x, position.y, position.z + 40, position.r, wait=True)
print('[ok]')
print('- rotation de l\'outil ... ', end='')
sys.stdout.flush()
device.move_to(position.x, position.y, position.z + 40, position.r + 45)
device.move_to(position.x, position.y, position.z + 40, position.r, wait=True)
print('[ok]')


print('- mouvement vertical rectiligne ... ', end='')
device.move_to(150, 0, 40, 0, wait=True)
device.move_to(150, 0, 100, 0, wait=True)
print('[ok]')

pretty_print_pose(device.pose())
print()

print('- test ventouse ... ', end='')
device.suck(True)
time.sleep(1)
device.suck(False)
print('[ok]')

print('- deconnexion')
device.close()
