# Drone Connexion
from pyardrone import ARDrone

drone = ARDrone()
drone.navdata_ready.wait()
print("initialisation finished")


# fonction à appeler pour faire tourner le drone
# Le premier nombre est pour faire bouger le drone sur l'axe vertical
# Le deuxieme nombre est pour faire tourner le drone sur lui-même clockwise ou counter clockwise
# Le dernier est un boolean à l'état 1 pour arrêter le programme et land le drone sinon ne fait rien
# example:
#   MoveTheDrone([1, ~, 0]) pour faire monter le drone
#   MoveTheDrone([-1, ~, 0]) pour faire descendre le drone
#   MoveTheDrone([~, 1, 0]) pour faire tourner le drone clockwise
#   MoveTheDrone([~, 1, 0]) pour faire tourner le drone counter clockwise
#   MoveTheDrone([~, ~, 1]) pour faire atterir le drone et arrêter le programme
def MoveTheDrone(order):
    # Si order vaut [~, ~, 1] alors on arrête le drone
    if order[3] == 1:
        Land()
        exit(200)

    # Moves the drone
    drone.move(up=(order[0] if order[0] >= 0 else 0),
               down=(order[0] if order[0] < 0 else 0),
               cw=(order[1] if order[1] >= 0 else 0),
               ccw=(order[1] if order[1] < 0 else 0))


# Take Off Function
def TakeOff():
    while not drone.state.fly_mask:
        drone.takeoff()


# Land Function
def Land():
    while drone.state.fly_mask:
        drone.land()
