import random
import math


# Create a node
# It is initialized with:
#   a matrixWeights as a list of 0.
#   a nodeListReference as a list of all the parent nodes
class Nodes:
    def __init__(self, matrixWeights, nodeListReference):
        if len(matrixWeights) != len(nodeListReference):
            print("error during initialisation of a node : line 2 in NeuralNetwork.py" +
                  "length of matrixWeights and nodeListReference does not match" +
                  "Should be equal")
            exit(100)
        self.matrixWeights = matrixWeights
        self.nodeRefs = nodeListReference
        self.value = 0
        self.poids = 0

    # Evaluate a Node with the values from its parents
    def evaluateNode(self):
        for i in range(len(self.nodeRefs)):
            self.value += self.nodeRefs[i].value * self.matrixWeights[i]
        self.value += self.poids

    # Set the value for this node
    def setValue(self, value):
        self.value = value

    # Set The value of the matrixWeights for this node
    def setMatrix(self, matrixWeights, poids):
        self.matrixWeights = matrixWeights
        self.poids = poids

    def getMatrix(self):
        return [self.matrixWeights, self.poids]

    def __len__(self):
        return 1

    def __str__(self):
        return self.value.__str__()


# Create a neural network depending on the parameters at the input
# numberInputs is for the number of inputs you want to send to the neural network
# numberOutputs is for the number of inputs you want from the neural network
# numberLayer is for the number of layer inside the neural network, it excludes the two layers of input and output
#   numberLayer = 1 will end in a neural network with one layer for the input, one layer hidden, one for the output
# listNodesNumberPerLayer must be a list of nodes number per layer
# Example : myNetwork = NeuralNetwork(3, 1, 2, [3, 4])
#   will produce a neural Network with, 3 inputs, 1 output and 2 hidden layers with 3 then 4 nodes
class NeuralNetwork:
    def __init__(self, numberInputs, numberOutputs, numberLayer, listNodesNumberPerLayer):
        # lself.nodesTree is for the node tree it holds in memory the architecture of the neural network with one element for one layer
        self.nodesTree = [[]]
        for i in range(numberInputs):
            self.nodesTree[0] += [Nodes([], [])]
        for j in range(numberLayer):
            self.nodesTree += [[]]
            for i in range(listNodesNumberPerLayer[j]):
                print(self.nodesTree[-(j + 2)])
                self.nodesTree[j + 1] += [Nodes([0] * len(self.nodesTree[-(j + 2)]), self.nodesTree[-(j + 2)])]
        self.nodesTree += [[]]
        for i in range(numberOutputs):
            self.nodesTree[-1] += [Nodes([0] * len(self.nodesTree[-(j + 2)]), self.nodesTree[-(j + 2)])]

    # Print the values of the nodes at the current status of the Neural Network
    def __str__(self):
        phrase = ""
        for i in range(len(self.nodesTree)):
            for j in range(len(self.nodesTree[i])):
                phrase += self.nodesTree[i][j].__str__()
                phrase += " "
            print(phrase)
            phrase = ""
        return ""

    # Train this neural network with some input Data
    def trainWithData(self, TrainingData):
        dico = {}
        dicoCounter = 0
        for dataTrain in TrainingData:
            for i in range(len(self.nodesTree[0])):
                self.nodesTree[0][i].setValue(dataTrain[0][i])
            while NeuralNetworkHasError(dataTrain, self):
                # if dataTrain == [[0, 0, 1], [1]]:
                #    print(self)
                for neuralLayer in self.nodesTree[1:]:
                    for neural in neuralLayer:
                        neural.setValue(0)
                for neuralLayer in self.nodesTree[1:]:
                    for neural in neuralLayer:
                        neural.setMatrix(generateNewRandomMatrix(len(neural.matrixWeights)), random.randint(-1, 1))
                        neural.evaluateNode()
            print(self)
            for neuralLayer in self.nodesTree[1:]:
                for neural in neuralLayer:
                    dicoCounter += 1
                    dico[dicoCounter] = neural.getMatrix()
            print(dico)
        print(dico)

    # Get the prediction from an input with this neural network
    def getPrediction(self, input):
        for i in range(len(self.nodesTree[0])):
            self.nodesTree[0][i].setValue(input[i])

        for i in range(1, len(self.nodesTree)):
            for j in range(len(self.nodesTree[i])):
                self.nodesTree[i][j].evaluateNode()

        return [self.nodesTree[-1][i].value for i in range(len(self.nodesTree[-1]))]


# Check if the NeuralNetwork is not predicting correctly for the current data
def NeuralNetworkHasError(donnees, network):
    if len(donnees[0]) == 2:
        # print("l106: "+donnees.__str__())
        for i in donnees:
            # print("l108: "+i.__str__())
            if areAnyOutputsDifferent(abs(network.getPrediction(i[0]) - i[1])):
                return True
    else:
        # print("l112: "+donnees.__str__())
        # print("l113: "+donnees[0][1].__str__())
        if areAnyOutputsDifferent(
                [abs(network.getPrediction(donnees[0])[i] - donnees[1][i]) for i in range(len(donnees[1]))]):
            return True
    return False


# generate a new Matrix weights from random numbers of the lengths in the input
def generateNewRandomMatrix(longueur):
    return [random.randint(-2, 2) for i in range(longueur)]


# Check if all the outputs of the Neural Network are correct
def areAnyOutputsDifferent(liste):
    for i in liste:
        if i > 0.5:
            return True
    return False


# Get the prediction with the Neural Network with the inputs with the EEG headset from the NeuralToDrone script
def getPrediction():
    # change by return myNetwork.getPrediction(DataDuCasque)
    return myNetwork.getPrediction(data[0][0])


data = [
    [[1, 1, 1], [0]],
    [[1, 1, 0], [1]],
    [[1, 0, 1], [1]],
    [[1, 0, 0], [0]],
    [[0, 1, 1], [0]],
    [[0, 1, 0], [1]],
    [[0, 0, 0], [0]],
    [[0, 0, 1], [1]]
]

myNetwork = NeuralNetwork(3, 1, 1, [3, 3])

myNetwork.trainWithData(data)

print("test finished")
