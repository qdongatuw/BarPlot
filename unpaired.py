import os
import matplotlib.pyplot as plt
import matplotlib
import tkinter as tk
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mod_ax import CusAxes, DraggableArtistY
from stats_methods import two_comp, oneway


class FigureWindow(tk.Toplevel):
    def __init__(self, group: list, datas: list, plot_type: str, option: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CusAx = None
        self.groups = group
        self.datas = datas
        self.raw_data = self.datas
        self.__norm_data = None
        self.option = option

        self.is_legend = tk.IntVar()
        self.is_sig_mark = tk.IntVar()
        self.is_norm = tk.IntVar()
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
        ttk.Checkbutton(f, text='Add */ns', variable=self.is_sig_mark, command=self.sig_mark).grid(row=0, column=3)
        ttk.Checkbutton(f, text='Normalize', variable=self.is_norm, command=self.plot).grid(row=0, column=4)
        ttk.Radiobutton(f, text='Open', variable=self.open_closed, value=0, command=self.plot).grid(row=0, column=5)
        ttk.Radiobutton(f, text='Closed', variable=self.open_closed, value=1, command=self.plot).grid(row=0, column=6)

        self.re_text = tk.Text(self, height=5)
        self.re_text.pack(side=tk.TOP, fill=tk.X, expand=1)

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(figure=self.fig, master=self)
        self.canvas.get_tk_widget().pack(expand=1)

        self.stat_result = None
        self.line = None
        self.text = None
        self.drag_line = None
        self.drag_text = None
        self.data_stat = []

        self.get_stat()
        self.stat()
        self.plot(plot_type)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    @property
    def norm_data(self):
        if self.__norm_data is None:
            self.__norm_data = []
            mean = np.mean(self.datas[0])
            for data in self.datas:
                self.__norm_data.append(data / mean * 100)
        return self.__norm_data

    def sig_mark(self):
        if not self.is_sig_mark.get():
            try:
                self.text.remove()
                self.line.remove()
                self.canvas.draw()
                self.line = None
                self.text = None
            except:
                pass
            return
        p = self.stat_result.p
        if p > 0.05:
            mark = 'NSD'
        elif 0.01 < p < 0.05:
            mark = '*'
        elif 0.001 < p < 0.01:
            mark = '**'
        else:
            mark = '***'

        xmin, xmax = self.ax.get_xlim()
        x1 = (0 - xmin)/(xmax - xmin)
        x2 = (1 - xmin)/(xmax - xmin)
        xx = 0.5

        stat = np.asarray(self.data_stat)
        y_bar_max = stat.T[2].max()
        if self.is_raw.get():
            y_bar_max = stat.T[3].max()
        ymin, ymax = self.ax.get_ylim()
        y_line = y_bar_max + 0.02 * (ymax - ymin)
        y_mark = y_line  # + 0.01 * (ymax - ymin)
        if len(self.datas) == 2:
            # line_, = self.ax.plot((x1, x2), (y_line, y_line))
            self.line = self.ax.axhline(y=y_line, xmin=x1, xmax=x2)
            self.text = self.ax.text(x=xx, y=y_mark, s=mark, verticalalignment='bottom', horizontalalignment='center')
            self.drag_text = DraggableArtistY(self.text)
            self.drag_line = DraggableArtistY(self.line)
            # self.CusAx.disconnect()

        self.canvas.draw()

    def stat(self):
        self.re_text.delete('1.0', tk.END)
        if len(self.datas) < 2:
            self.re_text.insert(tk.END, '')
        if len(self.datas) == 2:
            self.stat_result = two_comp(*self.datas)

        else:
            self.stat_result = oneway(*self.datas)
        quantification = '\nMean+/-SEM:\n'
        for s, i in zip(self.groups, self.data_stat):
            quantification += "{name}: {mean:.3f}+/-{sem:.3f}; ".format(name=s, mean=i[0], sem=i[1])

        self.re_text.insert(tk.END, self.stat_result)
        self.re_text.insert(tk.END, quantification)

    def save(self):
        path = self.option['path'] + self.option['sheet'] + 'bar_plot' + '.' + self.option['save_format']
        path_txt = self.option['path'] + self.option['sheet'] + 'note.txt'
        with open(path_txt, 'w') as f:
            f.write(self.re_text.get(index1='0.0', index2=tk.END))
        self.fig.savefig(fname=path)
        os.startfile(path)
        # os.startfile(path_txt)

    def get_stat(self):
        self.data_stat.clear()
        for data in self.datas:
            data_ = np.asarray(data)
            mean = data_.mean()
            std = data_.std()
            sem = std / (len(data_) ** 0.5)
            max_ = data_.max()
            self.data_stat.append([mean, sem, mean+sem, max_])

    def bar_plot(self):
        self.ax.clear()
        index = 0
        if self.is_norm.get():
            self.datas = self.norm_data
        else:
            self.datas = self.raw_data
        self.get_stat()
        self.stat()
        for data in self.datas:
            mean = self.data_stat[index][0]
            sem = self.data_stat[index][1]

            if self.open_closed.get():
                self.ax.bar(index, mean, self.option['bar_width'], yerr=sem, color=self.option['colors'][index],
                            label=self.groups[index],
                            edgecolor=self.option['colors'][index], ecolor=self.option['colors'][index])
            else:
                self.ax.bar(index, mean, self.option['bar_width'], yerr=sem, color='white', label=self.groups[index],
                            edgecolor=self.option['colors'][index], ecolor=self.option['colors'][index])
            if self.is_raw.get():
                x = (np.random.rand(len(data)) - 0.5) * self.option['bar_width'] * 0.8 + index
                self.ax.plot(x, data, '.', color=self.option['colors'][index])
            index += 1
        # self.ax.set_ylim(0, 1.1)
        if self.is_norm.get():
            label = self.option['sheet'] + '(%{s})'.format(s=self.groups[0])
        else:
            label = self.option['sheet']
        self.ax.set_ylabel(label)
        # self.ax.set_ylabel('Y data')

        self.ax.set_xticks(np.arange(0, len(self.groups)))
        self.ax.set_xticklabels(self.groups)
        self.ax.set_xlim(-0.75, len(self.groups)-0.25)
        if self.is_legend.get():
            matplotlib.legend.DraggableLegend(self.ax.legend())
        if self.CusAx is None:
            self.CusAx = CusAxes(self.ax)
        self.canvas.draw()
