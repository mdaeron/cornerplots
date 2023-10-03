"""
Simple library to create stairplots in `matplotlib`.

Stairplots provide a simple way to visualize multidimensional data,
with each dimension plotted against every other dimension.
"""

__author__    = 'Mathieu Daëron'
__contact__   = 'daeron@lsce.ipsl.fr'
__copyright__ = 'Copyright (c) 2023 Mathieu Daëron'
__license__   = 'MIT License - https://opensource.org/licenses/MIT'
__date__      = '2023-10-03'
__version__   = '1.0'


import matplotlib.pyplot as _ppl


def stairplot_axes(
	labels,
	subplots_adjust_args = (.15, .15, .95, .95, .4, .4),
	):
	"""
	Create triangle of axes plotting each label against each other once
	
	Parameters:
		labels (list): list of strings to be used as x- or y-labels
		subplots_adjust_args (tuple): arguments to pass to `subplots_adjust()`

	Returns:
		output (dict): a dictonary of the created `Axes` instances.
			Each subplot is indexed 2 times, with the following keys returning  the same `Axes` instance:
				- `(i,j)` or `(j,i)`: where `i` and `j` are the indices in `labels` 
				- `(a,b)` or `(b,a)`: where `a` and `b` are the values in `labels` (i.e., `labels[i] = a`)
	"""
	
	N = len(labels)
	axes = {}
	indices = range(N)
	for k in indices[:-1]:
		for j in range(k+1,N):
			axes[(j,k)] = _ppl.subplot(
				N-1, N-1, (N-1)*(j-1) + k + 1,
				sharex = axes[(k+1,k)]  if j > (k+1) else None,
				sharey = axes[(j,0)]  if k > 0 else None,
				)
			axes[(k,j)] = axes[(j,k)]
			if j == (N-1) :
				_ppl.xlabel(labels[k])
			if k == 0 :
				_ppl.ylabel(labels[j])

	_ppl.subplots_adjust(*subplots_adjust_args)

	output = {(u,v): axes[(u,v)] for u,v in axes}
	for u,v in axes:
		output[(labels[u], labels[v])] = axes[(u,v)]
	
	return output


def stairplot(data, axes, *args, **kwargs):
	"""
	Plot data in the proper location of a stairplot
	
	Parameters:
		data (dict): a dictionary of the form `{i: <array-like>, j: <array-like>}`,
			where `i,j` indicate the label (see `stairplot_axes()`) associated with each
			array-like. This will be used to decide which subplot to use, and which data
			should go in the X/Y axis.
		axes (dict): an output of `stairplot_axes()`
		*args, **kwargs: to be passed on to `plot()`
	
	Returns:
		whatever `plot()` returns
	"""
	i,j = sorted([_ for _ in data])
	return axes[(i,j)].plot(data[i], data[j], *args, **kwargs)

