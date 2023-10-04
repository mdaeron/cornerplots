#! /usr/bin/env python3

### GENERATE SOME RANDOM DATA ###

from numpy.random import default_rng
from numpy import cov, zeros, eye

labels = ['aaa', 'bbb', 'ccc', 'ddd']
fields = labels
N = len(labels)
Ndata = 1000

rng = default_rng(1)

seed_data = rng.multivariate_normal(
	mean = zeros((N,)),
	cov = eye(N),
	size = 3,
	)
C = cov(seed_data.T)

data = rng.multivariate_normal(
	mean = [1, 2, 4, 8],
	cov = C,
	size = Ndata,
	)

data = {f: data[:,k] for k,f in enumerate(fields)}
meandata = {_: data[_].mean() for _ in data}

### CREATE THE STAIRPLOTS ###

from stairplots import *
import matplotlib.pyplot as ppl

ppl.figure(figsize = (6,6))
sp = Stairplots(fields, labels)

sp.plot(data, 'r+', alpha = 0.05)
sp.plot(meandata, 'ws', mec = 'k', mew = 1, ms = 8)

ppl.savefig('stairplots.png')
