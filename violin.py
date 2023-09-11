import os
import matplotlib.pyplot as plt
import matplotlib
import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mod_ax import CusAxes
from stats_methods import two_comp, oneway


class FigureWindow(tk.Toplevel):
    def __init__(self, group: list, datas: list, option: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CusAx = None
        self.groups = group
        self.datas = datas
        self.option = option

        self.is_legend = tk.IntVar()
        self.is_legend.set(0)
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
        self.stat()
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
        path = self.option['path'] + self.option['sheet'] + 'violin_plot' + '.' + self.option['save_format']
        path_txt = self.option['path'] + self.option['sheet'] + 'note.txt'
        with open(path_txt, 'w') as f:
            f.write(self.re_text.get(index1='0.0', index2=tk.END))
        self.fig.savefig(fname=path)
        # os.startfile(path)
        # os.startfile(path_txt)

    def plot(self):
        self.ax.clear()

        p = self.ax.violinplot(self.datas, showextrema=False)
        for index, data in enumerate(self.datas):

            if self.open_closed.get():
                p['bodies'][index].set_facecolor(self.option['colors'][index])
                p['bodies'][index].set_edgecolor(self.option['colors'][index])
            else:
                p['bodies'][index].set_facecolor('white')
                p['bodies'][index].set_edgecolor(self.option['colors'][index])
            if self.is_raw.get():
                x = (np.random.rand(len(data)) - 0.5) * self.option['bar_width'] * 0.8 + index+1
                self.ax.plot(x, data, '.', markersize=0.5, color=self.option['colors'][index])

        # self.ax.set_ylim(0, 1.1)
        self.ax.set_ylabel('${' + self.option['sheet'] + '}$')
        # self.ax.set_ylabel('Y data')

        self.ax.set_xticks(np.arange(1, len(self.groups)+1))
        self.ax.set_xticklabels(self.groups)
        self.ax.set_xlim(0.5, len(self.groups)+0.5)
        if self.is_legend.get():
            matplotlib.legend.DraggableLegend(self.ax.legend())
        if self.CusAx is None:
            self.CusAx = CusAxes(self.ax)
        self.canvas.draw()
