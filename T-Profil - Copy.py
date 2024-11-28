#Teile von Code basieren auf die Übung Numerische Strömungssimulation für VT und CIW im WS24/25 von Professor Nirschl

import numpy as np
import matplotlib.pyplot as plt
import time

#Querschnitt
xMin = 0 #m
xMax = 0.1 #m
yMin = 0 #m
yMax = 0.1 #m

#Eingabe des Rechengitters
print("nxn Gitter n=")
Gitter = int(input())
if (Gitter - 2) % 3 != 0:
    print("Rechengitter nicht in 3x3 teilbar")
    exit()
numX = Gitter
numY = Gitter

#Eingabe des Materials
print("Temperaturleitfähigkeit von: \n 1. Kupfer\n 2. Stahl\n 3. Styropor")
TempLeitF = int(input())
match TempLeitF:
    case 1:
        a = 115 * 10 ** (-6) #m2/s Temperaturleitfähigkeit Kupfer
        Name = "Kupfer"
    case 2:
        a = 4 * 10 ** (-6) #m2/s Temperaturleitfähigkeit Stahl
        Name = "Stahl"
    case 3:
        a = 0.4 * 10 ** (-6) #m2/s Temperaturleitfähigkeit Styropor
        Name = "Styropor"
    case _:
        exit()

#Definition der Anfangsbedingung
T0 = 100. #°C

#Definition der Anfangsbedingung
T_A = 20. #°C

#Definition der Zeitschrittweite
dt = 0.01 #s

#Definition des Startzeitpunktes
t0 = 0 #s

#Definition des Endzeitpunktes
t_end = 1 #s

#Definieren der Anfangsbedingungen
T_t0 = np.zeros((numX, numY))

#Alle Kanten und Inzies sind super schlecht definiert, wenn ich mehr Zeit habe, machen ich das anders

#Definieren der Randpunkte des T-Profils
KanteX = int(( numX - 2) * 2 / 3 + 1)
KanteY_West = int((numY - 2) / 3 + 1)
KanteY_East = int((numY - 2) * 2 / 3 + 1)
MitteY = int((numY - 2) / 2) + 2
MitteXSued = int((numX - 2) / 3) + 2
MitteXNord = int ((numX - 2) * 5 / 6) + 2
RandAbstand = int((numX - 2) / 10)

#Definieren des T-Profils
T_t0[1      : KanteX   , KanteY_West : KanteY_East] = T_A
T_t0[KanteX : numX - 1 , 1           : numY - 1   ] = T_A

#Behandlung der Randbedigungen bzw. Dirichelt und Neumann Bedingugen
def Randbedingung (T_t0R:np.array, numXR:int, numYR:int, KanteXR:int, KanteY_EastR:int, KanteY_WestR:int):
    #Neumann Bedingung am obereb Rand
    T_t0R[-1 , 1 : numY - 1] = T0

    #Neumann Bedingung an allen anderen Rändern
    T_t0R[KanteXR : numXR - 1 , 0] = T_t0R[KanteXR : numXR - 1 , 1]
    T_t0R[KanteXR - 1, 1 : KanteY_WestR - 1] = T_t0R[KanteXR, 1 : KanteY_WestR - 1]
    T_t0R[1 : KanteXR - 1, KanteY_WestR - 1 ] = T_t0R[1 : KanteXR - 1, KanteY_WestR]
    T_t0R[0 , KanteY_WestR : KanteY_EastR] = T_t0R[1 , KanteY_WestR : KanteY_EastR]
    T_t0R[1 : KanteXR - 1, KanteY_EastR] = T_t0R[1 : KanteXR - 1, KanteY_EastR - 1]
    T_t0R[KanteXR - 1, KanteY_EastR + 1 : numYR - 1] = T_t0R[KanteXR , KanteY_EastR + 1 : numYR - 1]
    T_t0R[KanteXR : numXR - 1 , numYR - 1] = T_t0R[KanteXR : numXR - 1 , numYR - 2]

    #Neumann Bedingung Eckpunkte
    T_t0R[KanteXR - 1 , KanteY_WestR - 1] = T_t0R[KanteXR , KanteY_WestR]
    T_t0R[KanteXR - 1 , KanteY_EastR] = T_t0R[KanteXR , KanteY_EastR - 1]

Randbedingung(T_t0, numX, numY, KanteX, KanteY_East, KanteY_West)

#Initialisieren des Diagramms
fig, axis = plt.subplots()
pcm = axis.pcolormesh(T_t0, cmap=plt.cm.jet, vmin=0, vmax=100)
plt.colorbar(pcm, ax=axis)
plt.show()

#Initialisieren des Rechengebietes für die Zeitschritte n und n+1
T_n = np.copy(T_t0)
T_np1 = np.copy(T_t0)

#Gitterweite in x-Richtung
dx = (xMax - yMin) / (numX - 1)
dy = (yMax - yMin) / (numY - 1)

#Berechnung der Anzahl der Zeitschritte
num_Zeitschritte = int((t_end - t0) / dt)

#Maske für T-Profil
mask = np.zeros((numX, numY), dtype=bool)
mask[1:KanteX, KanteY_West:KanteY_East] = True
mask[KanteX:numX-1, 1:numY-1] = True

#Visualisierung des T-Profils mit Maske
fig, axis = plt.subplots()
pcm = axis.pcolormesh(T_n, cmap=plt.cm.jet, vmin=0, vmax=100)
plt.colorbar(pcm, ax=axis)
masked_T = np.ma.masked_array(T_n, ~mask)

#Anfang der Zeitmessung
start_time = time.time()

#Zeitschleife
for t in range(0,num_Zeitschritte):
    
    #Durchlaufen aller Punkte in y-Richtung
    for j in range(1, numY-1):
        
        # Durchlaufen aller Punkte in x-Richtung
        for i in range(1, numX-1):
            if i >= KanteX and i <= numX - 2:
                T_np1[i,j] = T_n[i,j] + dt * a * ((T_n[i+1,j] - 2 * T_n[i,j] + T_n[i-1,j]) / (dx * dx) + (T_n[i,j+1] - 2 * T_n[i,j] + T_n[i,j-1]) / (dy * dy))
            else:
                if (j >= KanteY_West and j <= KanteY_East - 1):
                    T_np1[i,j] = T_n[i,j] + dt * a * ((T_n[i+1,j] - 2 * T_n[i,j] + T_n[i-1,j]) / (dx * dx) + (T_n[i,j+1] - 2 * T_n[i,j] + T_n[i,j-1]) / (dy * dy))

    #Berechnung der neunen Randbedingungen
    Randbedingung(T_np1, numX, numY, KanteX, KanteY_East, KanteY_West) 

    #Kopieren der Lösung für den Zeitschritt n+1 als Startbedingung für den neuen Zeitschritt
    T_n[:,:] = T_np1[:,:]

    #Mittlere Temperatur
    mittelTemperatur = np.mean(T_n[1 : KanteX , KanteY_West : KanteY_East]) * 2 / 5 + np.mean(T_n[KanteX : numX - 1   , 1 : numY - 1]) * 3 / 5
    print(f"{t}")
    
    #Diagramm Update
    masked_T = np.ma.masked_array(T_n, ~mask)
    pcm.set_array(masked_T.ravel())
    axis.set_title(f"T-Profil aus {Name} mit Querschnitt {round(xMax * yMax * 5 / 9, 4)} m2, \nt = {round(t * dt, 2)} s, Mittlere Temperatur T = {str(round(mittelTemperatur, 2))} °C")

    #Diagramm Update    
    if t % 20 == 0:
        masked_T = np.ma.masked_array(T_n, ~mask)
        pcm.set_array(masked_T.ravel())
        #Labels sehr schlecht geschrieben
        axis.set_title(f"T-Profil aus {Name} mit Querschnitt {round(xMax * yMax * 5 / 9, 4)} m2, \nt = {round(t * dt, 2)} s, Mittlere Temperatur T = {str(round(mittelTemperatur, 2))} °C")
        text1 = plt.text(MitteY, KanteX, round(T_n[KanteX, MitteY], 2), ha="center", va="center", color="black", fontweight='bold')
        text2 = plt.text(MitteY, MitteXSued, round(T_n[MitteXSued, MitteY], 2), ha="center", va="center", color="black", fontweight='bold')
        text3 = plt.text(MitteY, numX - RandAbstand, round(T_n[numX - RandAbstand, MitteY], 2), ha="center", va="center", color="black", fontweight='bold')
        text4 = plt.text(MitteY, RandAbstand, round(T_n[RandAbstand, MitteY], 2), ha="center", va="center", color="black", fontweight='bold')
        text5 = plt.text(1, MitteXNord, round(T_n[MitteXNord, 1], 2), ha="center", va="center", color="black", fontweight='bold') #NICHT DYNAMISCH
        text6 = plt.text(45, MitteXNord, round(T_n[MitteXNord, 45], 2), ha="center", va="center", color="black", fontweight='bold') #NICHT DYNAMISCH
        plt.pause(dt * 20)

        text1.remove()
        text2.remove()
        text3.remove()
        text4.remove()
        text5.remove()
        text6.remove()
plt.show()

#Ende der Zeitmessung
print("Berechungsdauer --- %s Sekunden ---" % (time.time() - start_time))