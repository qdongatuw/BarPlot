import tkinter as tk
from tkinter import messagebox, filedialog
import os
import itertools
import ttkbootstrap as ttk
import ttkbootstrap.constants as tc
from matplotlib import rc
from configparser import ConfigParser
from load_data import LoadData
from unpaired import FigureWindow


class GUI(ttk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Bar Plot (v 0.1)')
        self.option = dict()
        self.read_setting()

        f = ttk.Frame(self)
        f.pack(expand=1, fill=tk.BOTH)

        self.file_tk = tk.StringVar()
        self.sheet_name = tk.StringVar()
        self.file_tk.set("")
        self.data = None

        f_file = ttk.Labelframe(f, text='Excel File')
        f_file.pack(side=tk.TOP, fill=tk.X, expand=1)

        f_bottom = ttk.Frame(f)
        f_bottom.pack(side=tk.BOTTOM, fill=tk.X, expand=1)
        self.buttons = []
        self.buttons.append(ttk.Button(f_bottom, text='Bar Plot', state='disabled', command=self.bar))
        self.buttons.append(ttk.Button(f_bottom, text='Box Plot', state='disabled', command=self.block))
        self.buttons.append(ttk.Button(f_bottom, text='Violin Plot', state='disabled', command=self.violin))
        self.buttons.append(ttk.Button(f_bottom, text='Paired Plot', state='disabled', command=self.pair))
        self.buttons.append(ttk.Button(f_bottom, text='Cumulative curve', state='disabled', command=self.cumu))
        self.buttons.append(ttk.Button(f_bottom, text='Hitogram', state='disabled', command=self.hist))
        self.buttons.append(ttk.Button(f_bottom, text='Stacked Bar', state='disabled', command=self.stack))
        for i, button in enumerate(self.buttons):
            button.grid(row=0, column=i)
        ttk.Button(f_bottom, text='Setting', command=self.setting).grid(row=0, column=len(self.buttons))

        left_panel = ttk.Frame(f)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, expand=1)
        right_panel = ttk.Labelframe(f, text='Preview')
        right_panel.pack(side=tk.LEFT, fill=tk.Y, expand=1)

        self.cells = [[0, 0, 0]] * 5  # a grid to preview the sheet
        self.cell_data_tk_list = []
        self.const_cells(master=right_panel)

        self.f_sheet = ttk.Labelframe(left_panel, text='Sheets')
        self.f_sheet.pack(side=tk.TOP, fill=tk.X)

        self.f_sheet_ = ttk.Frame(self.f_sheet)
        self.f_sheet_.pack(fill=tk.BOTH, expand=1)

        ttk.Entry(f_file, textvariable=self.file_tk).pack(side=tk.LEFT, fill=tk.X, expand=1)
        ttk.Button(f_file, text='Browse', command=self.open_file).pack(side=tk.LEFT)

        self.protocol("WM_DELETE_WINDOW", self.quit)

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[('MS sheet file', '.xlsx'), ('All files', '*')],
                                          defaultextension='.xlsx')
        if not path:
            return
        if os.path.splitext(path)[1] != '.xlsx':
            messagebox.showerror(title='Error.', message='Please make sure the file is an MS excel file.')
            return
        self.option['path'] = path
        self.f_sheet_.destroy()
        self.f_sheet_ = ttk.Frame(self.f_sheet)
        self.f_sheet_.pack(fill=tk.BOTH, expand=1)
        self.file_tk.set(path)
        self.data = LoadData(filename=path)
        for index, sheet in enumerate(self.data.sheet_names):
            ttk.Radiobutton(self.f_sheet_, text=sheet, variable=self.sheet_name, value=sheet,
                            command=self.update_preview).grid(row=index, sticky=tk.W)
        self.sheet_name.set(self.data.sheet_names[0])
        for button in self.buttons:
            button.config(state='normal')
        self.update_preview()

    def bar(self):
        from bar import FigureWindow
        sheet = self.sheet_name.get()
        self.data.get_groups(sheet_name=sheet)
        groups = self.data.group_name
        if len(groups) > 6:
            messagebox.showerror(title='Error!', message="Too many groups.")
            return
        self.data.load_data(sheet_name=sheet)
        datas = self.data.data_list
        self.option['sheet'] = sheet
        FigureWindow(group=groups, datas=datas, option=self.option)

    def stack(self):
        from stack import FigureWindow
        sheet = self.sheet_name.get()
        self.data.get_groups(sheet_name=sheet)
        groups = self.data.group_name
        if len(groups) > 6:
            messagebox.showerror(title='Error!', message="Too many groups.")
            return
        self.data.load_data(sheet_name=sheet)
        datas = self.data.data_list
        self.option['sheet'] = sheet
        FigureWindow(group=groups, datas=datas, option=self.option)

    def violin(self):
        from violin import FigureWindow
        sheet = self.sheet_name.get()
        self.data.get_groups(sheet_name=sheet)
        groups = self.data.group_name
        if len(groups) > 6:
            messagebox.showerror(title='Error!', message="Too many groups.")
            return
        self.data.load_data(sheet_name=sheet)
        datas = self.data.data_list
        self.option['sheet'] = sheet
        FigureWindow(group=groups, datas=datas, option=self.option)

    def pair(self):
        from figure_pair import FigureWindow
        sheet = self.sheet_name.get()
        self.data.get_groups(sheet_name=sheet)
        groups = self.data.group_name
        if len(groups) != 2:
            messagebox.showerror(title='Error!', message="Must be 2 groups.")
            return
        self.data.load_data(sheet_name=sheet)
        datas = self.data.data_list
        self.option['sheet'] = sheet
        FigureWindow(group=groups, datas=datas, option=self.option)

    def block(self):
        from box import FigureWindow
        sheet = self.sheet_name.get()
        self.data.get_groups(sheet_name=sheet)
        groups = self.data.group_name
        if len(groups) > 6:
            messagebox.showerror(title='Error!', message="Too many groups.")
            return
        self.data.load_data(sheet_name=sheet)
        datas = self.data.data_list
        self.option['sheet'] = sheet
        FigureWindow(group=groups, datas=datas, option=self.option)

    def cumu(self):
        from cumulative import FigureWindow
        sheet = self.sheet_name.get()
        self.data.get_groups(sheet_name=sheet)
        groups = self.data.group_name
        if len(groups) > 6:
            messagebox.showerror(title='Error!', message="Too many groups.")
            return
        self.data.load_data(sheet_name=sheet)
        datas = self.data.data_list
        self.option['sheet'] = sheet
        FigureWindow(group=groups, datas=datas, option=self.option)

    def hist(self):
        from hitograme import FigureWindow
        sheet = self.sheet_name.get()
        self.data.get_groups(sheet_name=sheet)
        groups = self.data.group_name
        if len(groups) > 6:
            messagebox.showerror(title='Error!', message="Too many groups.")
            return
        self.data.load_data(sheet_name=sheet)
        datas = self.data.data_list
        self.option['sheet'] = sheet
        FigureWindow(group=groups, datas=datas, option=self.option)
    
    def unpaired_plot(self):
        sheet = self.sheet_name.get()
        self.data.get_groups(sheet_name=sheet)
        groups = self.data.group_name
        if len(groups) > 6:
            messagebox.showerror(title='Error!', message="Too many groups.")
            return
        self.data.load_data(sheet_name=sheet)
        datas = self.data.data_list
        self.option['sheet'] = sheet
        FigureWindow(group=groups, datas=datas, plot_type='', option=self.option)

    def const_cells(self, master):
        row = len(self.cells)
        column = len(self.cells[0])
        for r, c in itertools.product(range(row), range(column)):
            self.cell_data_tk_list.append(tk.StringVar())
            # self.cell_data_tk_list[-1].set(str(r) + str(c))
            self.cell_data_tk_list[-1].set('0')
            color = '#ccccff' if r % 2 else None
            tk.Label(master, border=1, textvariable=self.cell_data_tk_list[-1], background=color,
                     relief=tk.SUNKEN, width=10, height=1).grid(row=r, column=c)

    def update_preview(self):
        self.data.preview(self.sheet_name.get())
        row = len(self.cells)
        column = len(self.cells[0])
        for r, c in itertools.product(range(row), range(column)):
            try:
                self.cell_data_tk_list[column * r + c].set(round(self.data.preview_data[r][c], 2))
            except IndexError:
                self.cell_data_tk_list[column * r + c].set('')
            except TypeError:
                if self.data.preview_data[r][c] is not None:
                    self.cell_data_tk_list[column * r + c].set(self.data.preview_data[r][c])
                else:
                    self.cell_data_tk_list[column * r + c].set('')

    def read_setting(self):
        facecolor = ['w', '#555555']
        line_text_color = ['k', 'w']
        if os.path.exists('./setting.ini'):
            config = ConfigParser()
            config.read('./setting.ini')
            darkmode = int(config['Plot']['Dark Mode'])
            self.option['same_color'] = int(config['Plot']['same color'])
            self.option['save_format'] = config['Plot']['format']
            self.option['bar_width'] = float(config['Plot']['bar width'])/100
            self.option['color_1'] = config['Plot']['Color 1']
            self.option['color_2'] = config['Plot']['Color 2']
            self.option['color_3'] = config['Plot']['Color 3']
            self.option['color_4'] = config['Plot']['Color 4']
            self.option['color_5'] = config['Plot']['Color 5']
            self.option['color_6'] = config['Plot']['Color 6']
            self.option['colors'] = [self.option['color_1'], self.option['color_2'],
                                     self.option['color_3'], self.option['color_4'],
                                     self.option['color_5'], self.option['color_6']]

            self.option['capsize'] = int(config['Plot']['Cap size'])
            rc('lines', linewidth=float(config['Plot']['line width']), color=line_text_color[darkmode])
            rc('font', family=config['Plot']['font family'], weight=config['Plot']['font weight'],
               size=config['Plot']['font size'])
            rc('axes', linewidth=float(config['Plot']['axis line width']),
               labelsize=float(config['Plot']['axis label size']),
               labelweight=config['Plot']['axis label weight'], titlesize=float(config['Plot']['title size']),
               titleweight='bold', edgecolor=line_text_color[darkmode], labelcolor=line_text_color[darkmode],
               facecolor=facecolor[darkmode]) # , markersize=1.0)
            rc('axes.spines', right=False, top=False)
            rc('legend', framealpha=0.5, fontsize=float(config['Plot']['legend font size']),
               frameon=int(config['Plot']['legend frame']))
            rc('xtick', top=False, labeltop=False, labelsize=float(config['Plot']['xtick size']),
               color=line_text_color[darkmode])
            rc('ytick', right=False, labelright=False, labelsize=float(config['Plot']['ytick size']),
               color=line_text_color[darkmode])
            rc('text', color=line_text_color[darkmode])
            rc('figure', dpi=float(config['Plot']['dpi']), figsize=(float(config['Plot']['width']),
                                                                    float(config['Plot']['height'])),
               facecolor=facecolor[darkmode])
            # rc('figure.subplot', left=0.3, right=0.9, bottom=0.3, top=0.9, wspace=0.2, hspace=0.2)
            rc('figure.subplot', left=0.3, right=0.9, bottom=0.5, top=0.9, wspace=0.2, hspace=0.2)
            rc('errorbar', capsize=float(config['Plot']['Cap size']))
            rc('savefig', transparent=True, dpi=float(config['Plot']['dpi']))
        else:
            is_default = messagebox.askyesno(title='Initialization?', message='Setting file not found. '
                                                                              'click Yes to customize the setting. '
                                                                              'Click No to use the default setting')
            if is_default:
                self.setting()
            else:
                self.option['same_color'] = 0
                self.option['save_format'] = 'tif'
                self.option['color_1'] = '#222222'
                self.option['color_2'] = '#cc6666'
                self.option['color_3'] = '#66cc66'
                self.option['color_4'] = '#6666cc'
                self.option['color_5'] = '#cccc66'
                self.option['color_6'] = '#66cccc'
                self.option['colors'] = [self.option['color_1'], self.option['color_2'],
                                         self.option['color_3'], self.option['color_4'],
                                         self.option['color_5'], self.option['color_6']
                                         ]
                self.option['bar_width'] = 0.8
                self.option['capsize'] = 0

                darkmode = 0

                rc('lines', linewidth=0.8, color=line_text_color[darkmode])
                rc('font', family='Times New Roman', weight='bold', size=14)
                rc('axes', linewidth=1, labelsize=14, labelweight='bold', titlesize=18,
                   titleweight='bold', edgecolor=line_text_color[darkmode], labelcolor=line_text_color[darkmode],
                   facecolor=facecolor[darkmode], markersize=1.0)
                rc('axes.spines', right=False, top=False)
                rc('legend', framealpha=0.5, fontsize=10, frameon=False)
                rc('xtick', top=False, labeltop=False, labelsize=10, color=line_text_color[darkmode])
                rc('ytick', right=False, labelright=False, labelsize=10, color=line_text_color[darkmode])
                rc('text', color=line_text_color[darkmode])
                rc('figure', dpi=300, figsize=(5, 4), facecolor=facecolor[darkmode])
                rc('figure.subplot', left=0.3, right=0.9, bottom=0.3, top=0.9, wspace=0.2, hspace=0.2)
                rc('errorbar', capsize=0)
                rc('savefig', transparent=True, dpi=300)

    def setting(self):
        from preference import Preference
        Preference(master=self)


if __name__ == '__main__':
    # plt.rcParams['axes.linewidth'] = 5
    APP = GUI()
    APP.mainloop()
