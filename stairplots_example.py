#! /usr/bin/env python3

import numpy as np
from stairplots import *
import matplotlib.pyplot as ppl


t = np.linspace(0, 1)
model = dict(
    w = 3 * t + 1,
    x = 5 * t,
    y = 8 * t**.5,
    z = 3 * t**1.5,
    )

red_data = dict(
    w = np.array([1, 2, 3, 4]),
    x = np.array([0, 2, 4, 5]),
    y = np.array([1, 4, 6, 8]),
    )

blue_data = dict(
    x = np.array([1, 2, 5]),
    y = np.array([3, 5, 7]),
    z = np.array([0, 1, 3]),
    )


fig = ppl.figure(figsize = (5,5))

sp = Stairplots(
    fields = ['w', 'x', 'y', 'z'],
    labels = ['W-value', 'X-value', 'Y-value', 'Z-value'],
    )

sp.plot(model,     'k-', lw = 1, dashes = (6,2,2,2), label = 'model')
sp.plot(red_data,  'ws', mec = 'r', mew = 1, ms = 5, label = 'red data')
sp.plot(blue_data, 'wD', mec = 'b', mew = 1, ms = 5, label = 'blue data')

sp.legend()

ppl.savefig('stairplots.png')
