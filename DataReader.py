import matplotlib.pyplot as plt
import csv
import time
import NeuralToDrone as NTD


# Calcule la moyenne d'une liste
def moyenne(list):
    moy = 0
    for i in list:
        moy += i
    return moy / len(list)


# Calcule la variance d'une liste
def var(list, j):
    var = 0
    moy = moyenne(list)
    for i in list:
        var += (i - moy) ** 2
    return min(var / len(list), 1000000)


# Effectue la mise à jour de la liste en ajoutant à la première place et en supprimant la dernière place
def update(list, value):
    for i in range(len(list)):
        if list[i] == 0:
            list[i] = value
            return
    for i in range(len(list), 2, -1):
        list[i - 1] = list[i - 2]
    list[0] = value

# initialisation
NTD.takeOff()
capteurs = [[], [], [], [], [], [], [], [], [], [], [], [], [], []]
t1 = time.time()
t = time.time()
value = []
varianceCapted = []
executionTime = []

with open('TestMvtsSourire+Contract.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    readerlength = 0
    # Pour chaque lignes d'entrées du csv
    for row in spamreader:
        executionTime += [(time.time() - t1)/0.0078*100]
        if (time.time() - t1) > 0.0078:
            print("Execution time too long")
        time.sleep(0.0078 - (time.time() - t1))
        t1 = time.time()
        readerlength += 1
        # Ligne pour arrêter le code
        if readerlength > 250:
            break
        print(readerlength)
        # Si on a lu les 2 premières lignes du csv
        if readerlength > 2:
            # capteurs stocke la i+3e colonne de row
            for i in range(14):
                capteurs[i] += [float(row[i + 3])]
        # Taille (ici 200) du buffer pour le nombre de valeurs sur lesquelles on calcule la variance
        if len(capteurs[0]) > 200:
            for i in range(14):
                capteurs[i] = capteurs[i][1:len(capteurs[i])]
            # calcule de la variance de la somme des capteurs
            varCapted = var([sum([capteurs[k][j] for k in range(14)]) for j in range(len(capteurs[0]))], 0)
            varianceCapted += [varCapted]
            # classification en 3 valeurs
            if varCapted > 400000:
                value += [1]
            elif varCapted > 20000:
                value += [0.5]
            else:
                value += [0]
            # envoie d'une commande de vol
            NTD.SendCommand(value[-1])
    # envoie d'une commande pour arrêter le vol
    NTD.SendCommand(0, 1)

# affichage des courbes
plt.plot([i for i in range(len(varianceCapted))], varianceCapted)
plt.show()
plt.plot([i for i in range(len(value))], value)
plt.show()
plt.plot([i for i in range(len(executionTime))], executionTime)
plt.show()