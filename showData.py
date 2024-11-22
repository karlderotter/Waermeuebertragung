# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 13:49:08 2023

@author: xk4236
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython import get_ipython

from Parameter import *
from num_Parameter import *
from Initialisierung import *
from showInitial import * 
'''
    pcm.set_array(u)
    axis.set_title("Distribution at t: {:.3f} [s].".format(counter))
    plt.pause(0.01)
'''
#Ab hier

#Funktion zum updaten des Initialen Plots. Benötigt als Variablen das neue T-Feld und die Zeit
def update_plot(T_n, t, pic=picture, fig=figure, ax=ax):
    pic.set_data(T_n)
    ax.set_title("t = " + str(t) + " s")
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.show()