import NeuralNetwork as N
import DroneFlyer as D

D.TakeOff()

normalizedStatus = [0, 0, 0]

# While not Landing
while normalizedStatus[2] == 0:
    statusNN = N.getPrediction()
    # Add Exit Option on the third component of normalizedStatus
    normalizedStatus = [1 if statusNN[0] > 0.5 else 0, 1 if statusNN[1] > 0.5 else 0, 0]
    D.MoveTheDrone(normalizedStatus)
