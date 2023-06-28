import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mod_ax import CusAxes
from stats_methods import oneway, two_comp


class FigureWindow(tk.Toplevel):
    def __init__(self, group: list, datas: list, option:dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CusAx = None
        self.groups = group
        self.datas = datas
        self.option = option

        self.is_legend = tk.IntVar()
        self.is_legend.set(1)
        self.is_raw = tk.IntVar()
        self.is_raw.set(0)
        self.open_closed = tk.IntVar()
        self.open_closed.set(1)
        f = ttk.Frame(self)
        f.pack(side=tk.TOP, fill=tk.X, expand=1)

        tk.Button(f, text='Save', command=self.save).grid(row=0, column=0)
        ttk.Checkbutton(f, text='Show legend', variable=self.is_legend, command=self.plot).grid(row=0, column=1)
        ttk.Checkbutton(f, text='Raw data', variable=self.is_raw, command=self.plot).grid(row=0, column=2)

        ttk.Radiobutton(f, text='Open', variable=self.open_closed, value=0, command=self.plot).grid(row=0, column=3)
        ttk.Radiobutton(f, text='Closed', variable=self.open_closed, value=1, command=self.plot).grid(row=0, column=4)

        self.re_text = tk.Text(self, height=5)
        self.re_text.pack(side=tk.TOP, fill=tk.X, expand=1)

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(figure=self.fig, master=self)
        self.canvas.get_tk_widget().pack(expand=1)
        # self.stat()
        self.plot()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def stat(self):
        if len(self.datas) < 2:
            self.re_text.insert(tk.END, '')
        if len(self.datas) == 2:
            self.re_text.insert(tk.END, two_comp(*self.datas))
        else:
            self.re_text.insert(tk.END, oneway(*self.datas))

    def save(self):
        path = self.option['path'] + self.option['sheet'] + '_histo' + '.' + self.option['save_format']
        path_txt = self.option['path'] + self.option['sheet'] + 'note.txt'
        with open(path_txt, 'w') as f:
            f.write(self.re_text.get(index1='0.0', index2=tk.END))
        self.fig.savefig(fname=path)
        os.startfile(path)
        # os.startfile(path_txt)

    def plot(self):
        self.ax.clear()

        weights = [np.ones_like(arr) / float(len(arr)) for arr in self.datas]
        self.ax.hist(self.datas, bins=50, histtype='bar', density=False, stacked=False, weights=weights,
                     color=self.option['colors'][:len(self.datas)], alpha=0.5, label=self.groups)

        self.ax.set_xlabel(self.option['sheet'])
        self.ax.set_ylabel('Proportion')
        if self.is_legend.get():
            matplotlib.legend.DraggableLegend(self.ax.legend(markerscale=0.2, fontsize='xx-small'))
        if self.CusAx is None:
            self.CusAx = CusAxes(self.ax)
        self.canvas.draw()


if __name__ == '__main__':
    import numpy as np
    f = plt.figure()
    ax3 = f.add_axes([0.2,0.2,0.5,0.5])
    x_multi = [np.random.randn(n) for n in [10000, 5000, 2000]]
    # ax3.hist(x_multi, 50, histtype='bar', color=['r', 'g', 'k'])
    weights = [np.ones_like(arr) / float(len(arr)) for arr in x_multi]
    ax3.hist(x_multi, bins=30, histtype='bar', density=False, stacked=False, weights=weights, color=['r', 'g', 'k'], alpha=0.5)
    ax3.set_title('different sample sizes')
    plt.show()
