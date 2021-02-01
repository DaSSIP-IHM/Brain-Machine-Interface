import NeuralNetwork as N
import DroneFlyer as D


def takeOff():
    D.TakeOff()


def SendCommand(command, stop=0):
    # Si le drone doit se déplacer (évite de désactiver le mode stationnaire du drone alors qu'il doit bouger
    if command != 0:
        output = [command, 0, stop]
        # Partie à changer dans le futur, marche pour le moment dans cette configuration
        if command == 0.5:
            output[0] = 1
        elif command == 1:
            output[0] = -1
        # appel du drone
        D.MoveTheDrone(output)
