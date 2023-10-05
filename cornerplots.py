"""
Simple library to create corner plots in `matplotlib`.

Corner plots provide a simple way to visualize multidimensional data,
with each dimension plotted against every other dimension.
"""

__author__    = 'Mathieu Daëron'
__contact__   = 'daeron@lsce.ipsl.fr'
__copyright__ = 'Copyright (c) 2023 Mathieu Daëron'
__license__   = 'MIT License - https://opensource.org/licenses/MIT'
__date__      = '2023-10-05'
__version__   = '1.0'


import matplotlib.pyplot as _ppl


class Cornerplots():

	def __init__(self,
		fields, labels = None, fig = None,
		subplots_adjust = (.12, .12, .95, .95, .4, .4),
		sharexy = True,
		):
		"""
		Create triangle of axes plotting each field against each other once
	
		Parameters:
			fields (list): list of strings to be used as data fields
			labels (list): list of strings to be used as axis labels
			subplots_adjust (tuple): arguments to pass to `subplots_adjust()`
			sharexy (bool): force all X- and Y-axes of the same field to have identical limits
		"""

		self.fields = [_ for _ in fields]
		self.labels = [_ for _ in fields] if labels is None else [_ for _ in labels]
		self.fig = _ppl.gcf() if fig is None else fig
		self.subplots_adjust = subplots_adjust

		_ppl.figure(self.fig)
		_ppl.subplots_adjust(*subplots_adjust)

		N = len(labels)
		axes = {}

		for k in range(N):
			for j in range(k+1,N):
				axes[(k, j)] = _ppl.subplot(
					N-1, N-1, (N-1)*(j-1) + k + 1,
					sharex = axes[(k,k+1)]  if sharexy and j > (k+1) else None,
					sharey = axes[(0,j)]  if sharexy and k > 0 else None,
					)
				if j == (N-1) :
					_ppl.xlabel(labels[k])
				if k == 0 :
					_ppl.ylabel(labels[j])

		self.axes = {(self.fields[i], self.fields[j]): axes[(i, j)] for i, j in axes}
		self.legend_items = []


	def plot(self, datadict, *args, **kwargs):
		"""
		Plot data in the proper location of a cornerplot
	
		Parameters:
			datadict (dict): a dictionary of the form `{f1: <array-like>, f2: <array-like>, ...}`,
				where `f1`, `f2`, ... are fields corresponding to each array-like to plot.
				These fields will determine which subplot to use, and whether each field
				should plot along the X or Y axis.
			*args, **kwargs: to be passed on to `pyplot.plot()`
	
		Returns:
			List of values returned by `pyplot.plot()`
		"""
		indices = sorted([self.fields.index(_) for _ in datadict])
		fields = [self.fields[_] for _ in indices]

		result = []
		for _, fi in enumerate(fields[:-1]):
			for fj in fields[_+1:]:
				result += self.axes[(fi, fj)].plot(datadict[fi], datadict[fj], *args, **kwargs)

		if not result[0].get_label().startswith('_'):
			self.legend_items.append(result[0])

		return result


	def legend(self, *args, **kwargs):
		"""
		Plot combined legend for all cornerplots
	
		Parameters:
			*args, **kwargs: to be passed on to `pyplot.legend()`
	
		Returns:
			Value returned by `pyplot.legend()`
		"""
		return _ppl.legend(
			self.legend_items,
			[_.get_label() for _ in self.legend_items],
			*args,
			**(kwargs | {
				'loc': 'upper right',
				'bbox_to_anchor': self.subplots_adjust[2:4],
				'bbox_transform': self.fig.transFigure,
				'borderaxespad': 0,
				}),
			)