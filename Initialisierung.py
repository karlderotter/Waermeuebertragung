#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 08:28:31 2024

@author: student
"""

import numpy as np
from Parameter import *  #Was genau importiert das?
#Initialisierung des Rechengebietes

#Definieren der Anfangsbedingungen
T_t0 = T0 * np.ones((numX,numY))    #Notation?

#Inkludieren der Randbedingung
T_t0[:,0] = T_A
T_t0[:,-1] = T_A
T_t0[0,:] = T_A
T_t0[-1,:] = T0

#Initialisieren des Rechengebietes für die Zeitschritte n und n+1
T_n = np.copy(T_t0)
T_np1 = np.copy(T_t0)
