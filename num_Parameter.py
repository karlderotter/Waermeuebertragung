#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 08:44:43 2024

@author: student
"""

import numpy as np
from Parameter import *

#Bestimmen der numerischen Parameter

#Gitterweite in x-Richtung
dx = (xMax - yMin) / (numX - 1)
dy = (yMax - yMin) / (numY - 1)

#Temperaturleitfähigkeit
a = lambal / (rho * cp)

#Berechnung der Anzahl der Zeitschritte
num_Zeitschritte = int((t_end - t0) / dt)

#Darstellen der Anfangsbedingungen
import showInitial