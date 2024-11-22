#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 08:18:34 2024

@author: student
"""
#Abmessen des Querschnitts
xMin = 0 #m
xMax = 0.1 #m
yMin = 0 #m
yMax = 0.1 #m

#Stoffeigenschaften von Eisen
rho = 7874 #kg/m3
cp = 449 #J/(kg*K)
lambal = 80 #W/(m*K)

#Definition des Rechengitters
numX = 101 #Anzahl der Einteilungen in x-Richtung
numY = 101 #Anzahl der Einteilungen in y-Richtung

#Definition der Anfangsbedingung
T0 = 1000 #°C

#Definition der Anfangsbedingung
T_A = 100 #°C

#Definition der Zeitschrittweite
dt = 0.01 #s

#Definition des Startzeitpunktes
t0 = 0 #s

#Definition des Endzeitpunktes
t_end = 30 #s