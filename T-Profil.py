import numpy as np
import matplotlib.pyplot as plt

#Abmessen des Querschnitts
xMin = 0 #m
xMax = 0.1 #m
yMin = 0 #m
yMax = 0.1 #m

#Temperaturleitfähigkeit Stahl
a = 4 * 10 ** (-6) #m2/s

#Definition des Rechengitters
numX = 47 #Anzahl der Einteilungen in x-Richtung
numY = 47 #Anzahl der Einteilungen in y-Richtung

if numX != numY or ((numX - 2) % 3 != 0 or (numY - 2) % 3 != 0):
    print("Rechengitter nicht in 3x3 teilbar")
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
t_end = 120 #s

#Definieren der Anfangsbedingungen
T_t0 = np.zeros((numX,numY))

#Alle Kanten und Inzies sind super schlecht definiert, wenn ich mehr Zeit habe, machen ichd as nochmal

#Definieren der Randpunkte des T-Profils
KanteX = int(( numX - 2) * 2 / 3 + 1)
KanteY_West = int((numY - 2) / 3 + 1)
KanteY_East = int((numY - 2) * 2 / 3 + 1)

#Definieren des T-Profils
T_t0[1      : KanteX     , KanteY_West     : KanteY_East   ] = T_A
T_t0[KanteX : numX - 1   , 1               : numY - 1       ] = T_A


#Behandluch der Randbedigungen bzw. Dirichelt und Neumann Bedingugen
def Randbedingung (T_t0R:np.array, numXR:int, numYR:int, KanteXR:int, KanteY_EastR:int, KanteY_WestR:int):
    #Neumann Bedingung am obereb Rand
    T_t0R[-1                  , 1               : numY - 1       ] = T0

    #Dirichelt Bedingung an allen anderen Ränder
    T_t0R[KanteXR : numXR - 1 , 1] = T_t0R[KanteXR : numXR - 1 , 0]
    T_t0R[KanteXR, 1 : KanteY_WestR - 1] = T_t0R[KanteXR - 1, 1 : KanteY_WestR - 1]
    T_t0R[1 : KanteXR - 1, KanteY_WestR] = T_t0R[1 : KanteXR - 1, KanteY_WestR - 1]
    T_t0R[1 , KanteY_WestR : KanteY_EastR] = T_t0R[0 , KanteY_WestR : KanteY_EastR]
    T_t0R[1 : KanteXR - 1, KanteY_EastR] = T_t0R[1 : KanteXR - 1, KanteY_EastR + 1]
    T_t0R[KanteXR, KanteY_EastR + 1 : numYR - 1] = T_t0R[KanteXR - 1 , KanteY_EastR + 1 : numYR - 1]
    T_t0R[KanteXR : numXR - 1 , numYR - 1] = T_t0R[KanteXR : numXR - 1 , numYR]

    #Eckpunkte
    T_t0R[KanteXR - 1 , KanteY_WestR - 1] = T_t0R[KanteXR , KanteY_WestR]
    T_t0R[KanteXR - 1 , KanteY_EastR] = T_t0R[KanteXR , KanteY_EastR - 1]

Randbedingung(T_t0, numX, numY, KanteX, KanteY_East, KanteY_West)

'''
fig, axis = plt.subplots()
pcm = axis.pcolormesh(T_t0, cmap=plt.cm.jet, vmin=0, vmax=100)
plt.colorbar(pcm, ax=axis)
plt.show()
'''

#Initialisieren des Rechengebietes für die Zeitschritte n und n+1
T_n = np.copy(T_t0)
T_np1 = np.copy(T_t0)

#Gitterweite in x-Richtung
dx = (xMax - yMin) / (numX - 1)
dy = (yMax - yMin) / (numY - 1)

#Berechnung der Anzahl der Zeitschritte
num_Zeitschritte = int((t_end - t0) / dt)

#Darstellen der Anfangsbedingungen

#x, y = np.meshgrid(np.arange(xMax,xMin-dx,-dx),np.arange(yMax,yMin-dy,-dy))

#Numerische Fehler reduzieren indem 0 explizit zugeordnet wird
#x[:,-1] = 0
#y[-1,:] = 0

#Maske für T-Profil
mask = np.zeros((numX, numY), dtype=bool)
mask[1:KanteX, KanteY_West:KanteY_East] = True
mask[KanteX:numX-1, 1:numY-1] = True

#Visualisierung

fig, axis = plt.subplots()
pcm = axis.pcolormesh(T_n, cmap=plt.cm.jet, vmin=0, vmax=100)
plt.colorbar(pcm, ax=axis)
masked_T = np.ma.masked_array(T_n, ~mask)

#Zeitschleife
for t in range(0,num_Zeitschritte):
    
    #Durchlaufen aller Punkte in y-Richtung
    for j in range(1, numY-1):
        
        #gleichzeitig Durchlaufen aller Punkte in x-Richtung
        for i in range(1, numX-1):
            if i >= KanteX and i <= numX - 2:
                T_np1[i,j] = T_n[i,j] + dt * a * ((T_n[i+1,j] - 2 * T_n[i,j] + T_n[i-1,j]) / (dx * dx) + (T_n[i,j+1] - 2 * T_n[i,j] + T_n[i,j-1]) / (dy * dy))
            else:
                if (j >= KanteY_West and j <= KanteY_East - 1):
                    T_np1[i,j] = T_n[i,j] + dt * a * ((T_n[i+1,j] - 2 * T_n[i,j] + T_n[i-1,j]) / (dx * dx) + (T_n[i,j+1] - 2 * T_n[i,j] + T_n[i,j-1]) / (dy * dy))

    #Berechnung der neune Randbedingungen
    Randbedingung(T_np1, numX, numY, KanteX, KanteY_East, KanteY_West) 

    #Kopieren der Lösung für den Zeitschritt n+1 als Startbedingung 
    #für den neuen Zeitschritt
    T_n[:,:] = T_np1[:,:]

    #Gesonderte Behandlung der Dirichelt-Randbedingung
    #T_n[-1,:] = T0

    #Gesonderte Behandlung der Neumann-Randbedingung
    #T_n[:,1] = T_np1[:,2]
    #T_n[:,-2] = T_np1[:,-3]
    #T_n[1,:] = T_np1[2,:]

    #mittlere Temperatur
    mittelTemperatur = np.mean(T_n[1 : KanteX , KanteY_West : KanteY_East]) * 2 / 5 + np.mean(T_n[1 : KanteX , KanteY_West : KanteY_East]) * 3 / 5
    print("Die mittlere Temperatur zum Zeitpunkt t = " 
          + str(round(t*dt,2)) + " s beträgt " + str(mittelTemperatur) + "°C")
    

    #Diagramm Update    
    if t % 20 == 0:
        masked_T = np.ma.masked_array(T_n, ~mask)
        pcm.set_array(masked_T.ravel())
        axis.set_title(f"t = {round(t * dt,2)} s")
        plt.pause(dt * 20)

plt.show()
