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
__version__   = '1.1'


import matplotlib.pyplot as _ppl


class Stairplots():

	def __init__(self, fields, labels, subplots_adjust_args = (.15, .15, .95, .95, .4, .4)):
		"""
		Create triangle of axes plotting each field against each other once
	
		Parameters:
			fields (list): list of strings to be used as data fields
			labels (list): list of strings to be used as axis labels
			subplots_adjust_args (tuple): arguments to pass to `subplots_adjust()`
		"""

		self.fields = [_ for _ in fields]
		self.labels = [_ for _ in labels]

		_ppl.subplots_adjust(*subplots_adjust_args)

		N = len(labels)
		axes = {}

		for k in range(N):
			for j in range(k+1,N):
				axes[(k, j)] = _ppl.subplot(
					N-1, N-1, (N-1)*(j-1) + k + 1,
					sharex = axes[(k,k+1)]  if j > (k+1) else None,
					sharey = axes[(0,j)]  if k > 0 else None,
					)
				if j == (N-1) :
					_ppl.xlabel(labels[k])
				if k == 0 :
					_ppl.ylabel(labels[j])

		self.axes = {(self.fields[i], self.fields[j]): axes[(i, j)] for i, j in axes}

	def plot(self, datadict, *args, **kwargs):
		"""
		Plot data in the proper location of a stairplot
	
		Parameters:
			datadict (dict): a dictionary of the form `{f1: <array-like>, f2: <array-like>}`,
				where `f1` and `f2` are the fields corresponding to each array-like to plot.
				These fields will determine which subplot to use, and whether each field
				should plot along the X or Y axis.
			*args, **kwargs: to be passed on to `plot()`
	
		Returns:
			whatever `plot()` returns
		"""
		i, j = sorted([self.fields.index(_) for _ in datadict])
		fi, fj = self.fields[i], self.fields[j]
		return self.axes[(fi, fj)].plot(datadict[fi], datadict[fj], *args, **kwargs)
