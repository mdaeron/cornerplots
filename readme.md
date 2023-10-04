# Stairplots

Simple library to create stairplots in `matplotlib`. Stairplots provide a simple way to visualize multidimensional data, with each dimension plotted against every other dimension. The main goal is to let the user specify data and/or model predictions in arbitrary subsets of the multi-dimensional space and let the code take care of where to plot these values. Originally inspired by [corner.py](https://github.com/dfm/corner.py).

For example, you might have one set of (*x*, *y*) data, another set of (*y*, *z*) data, and a model predicting (*x*, *y*, *z*) trajectories. In that case, you could plot everything by simply calling:

```py
data_1 = dict(x = xdata1, y = ydata1)
# xdata1 and ydata1 are two array-likes with identical shapes

data_2 = dict(y = ydata2, z = zdata2)
# ydata2 and zdata2 are two array-likes with identical shapes

model = dict(x = xmodel, y = ymodel, z = zmodel)
# xmodel, ymodel, and zmodel are three array-likes with identical shapes

sp = Stairplots(['x', 'y', 'z'])

sp.plot(data_1, 'ws', mec = 'r')
sp.plot(data_2, 'wo', mec = 'b')
sp.plot(model, 'g-', lw = 2)
```

## Complete example

```py
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
```

Result:

<div align="center">
<img src="stairplots.png">
</div>