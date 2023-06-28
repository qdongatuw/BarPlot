import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import cumfreq


class CumAx:
    def __init__(self, ax: plt.Axes, data, legend: str=None, num_bin: int=50, color: str='k'):
        self.ax = ax
        self.data = data
        self.legend = legend
        self.num_bin = num_bin
        self.color = color
        self.__plot()
        
    def __plot(self):
        re = cumfreq(self.data, numbins=self.num_bin)
        y = re.cumcount / re.cumcount.max()
        x = np.arange(re.lowerlimit, re.lowerlimit + self.num_bin * re.binsize, re.binsize)

        min_size = min(len(y), len(x))
        y = y[:min_size]
        x = x[:min_size]

        self.ax.plot(x, y, color=self.color, label=self.legend)

    def __plot_hist(self):
        weights = np.ones_like(arr) / float(len(arr))
        self.ax.hist(arr, bins=self.num_bin, density=False, stacked=True, weights=weights, color=self.color, alpha=0.7)


if __name__ == '__main__':
    arr = np.random.randn(100)
    f = plt.figure(figsize=(2, 2))
    ax_ = f.add_axes([0.2, 0.2, 0.7, 0.7])
    CumAx(ax=ax_, data=arr)
    plt.show()
