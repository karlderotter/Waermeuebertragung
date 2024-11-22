# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 13:55:33 2023

@author: xk4236
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


from Parameter import *
from num_Parameter import *
from Initialisierung import *
from showInitial import *
from showData import update_plot

#Zeitschleife
for t in range(0,num_Zeitschritte):
    
    #Durchlaufen aller Punkte in y-Richtung
    for j in range(1, numY-1):
        
        #gleichzeitig Durchlaufen aller Punkte in x-Richtung
        for i in range(1, numX-1):
            
            T_np1[i,j] = T_n[i,j] + (dt / (rho * cp)) * lambal * ((T_n[i+1,j] - 2 * T_n[i,j] + T_n[i-1,j]) / (dx * dx) + (T_n[i,j+1] - 2 * T_n[i,j] + T_n[i,j-1]) / (dy * dy))
            
            
            
    
    #Kopieren der Lösung für den Zeitschritt n+1 als Startbedingung 
    #für den neuen Zeitschritt
    T_n[:,:] = T_np1[:,:]
    
    #Gesonderte Behandlung der Neumann-Randbedingung am unteren Rand
    T_n[-1,:] = T_np1[-2,:]
    
    #aktualisiere Plot
    update_plot(T_n, round(t*dt,2))
    
    #mittlere Temperatur
    mittelTemperatur = np.mean(T_np1)
    print("Die mittlere Temperatur zum Zeitpunkt t = " 
          + str(round(t*dt,2)) + " s beträgt " + str(mittelTemperatur) + "°C")
    