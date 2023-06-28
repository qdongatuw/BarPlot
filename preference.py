from configparser import ConfigParser
import os
import tkinter as tk
from tkinter import ttk


class Preference(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title('Setting')

        self.is_dark = tk.IntVar()
        self.dpi = tk.StringVar()
        self.format = tk.StringVar()

        self.font_family = tk.StringVar()
        self.font_weight = tk.StringVar()
        self.font_size = tk.StringVar()

        self.line_width = tk.StringVar()

        self.width = tk.StringVar()
        self.height = tk.StringVar()
        self.title_size = tk.StringVar()

        self.axis_lw = tk.StringVar()
        self.axis_label_size = tk.StringVar()
        self.axis_label_weight = tk.StringVar()
        self.axis_xtick_size = tk.StringVar()
        self.axis_ytick_size = tk.StringVar()
        
        self.legend_fontsize = tk.StringVar()
        self.legend_is_frame = tk.IntVar()

        self.capsize = tk.StringVar()

        self.is_same_color = tk.IntVar()
        self.color_1 = tk.StringVar()
        self.color_2 = tk.StringVar()
        self.color_3 = tk.StringVar()
        self.color_4 = tk.StringVar()
        self.color_5 = tk.StringVar()
        self.color_6 = tk.StringVar()
        self.bar_width = tk.StringVar()

        self.file = './setting.ini'
        self.config = ConfigParser()
        self.create_file()
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=1)
        self.frame_bottom = ttk.Frame(self)
        self.frame_bottom.pack(side=tk.BOTTOM, fil=tk.X, ipadx=5, ipady=5)
        ttk.Button(self.frame_bottom, text='OK', command=self.ok).pack(side=tk.RIGHT, padx=5)
        ttk.Button(self.frame_bottom, text='Apply', command=self.write).pack(side=tk.RIGHT, padx=5)
        ttk.Button(self.frame_bottom, text='Reset', command=self.reset).pack(side=tk.RIGHT, padx=5)
        ttk.Button(self.frame_bottom, text='Cancel', command=self.exit).pack(side=tk.RIGHT, padx=5)
        self.general()
        self.stat()

    def reset(self):
        self.is_dark.set(0)
        self.dpi.set('300.0')
        self.format.set('tif')
        self.width.set('3.0')
        self.height.set('3.0')

        self.line_width.set('1.0')
        self.font_family.set('Times New Roman')
        self.font_weight.set('bold')
        self.font_size.set('18')
        self.title_size.set('20')
        self.axis_lw.set('1.0')
        self.axis_label_size.set('12')
        self.axis_label_weight.set('bold')
        self.axis_xtick_size.set('10')
        self.axis_ytick_size.set('10')
        self.legend_fontsize.set('10')
        self.legend_is_frame.set(0)
        self.capsize.set('0')
        self.is_same_color.set(0)
        self.color_1.set('#222222')
        self.color_2.set('#cc6666')
        self.color_3.set('#66cc66')
        self.color_4.set('#6666cc')
        self.color_5.set('#cccc66')
        self.color_6.set('#66cccc')
        self.bar_width.set('80')

    def ok(self):
        self.write()
        self.destroy()

    def exit(self):
        self.destroy()

    def apply(self):
        # self.config.read(self.file)
        self.is_dark.set(int(self.config['Plot']['Dark Mode']))
        self.dpi.set(self.config['Plot']['dpi'])
        self.format.set(self.config['Plot']['format'])
        self.width.set(self.config['Plot']['width'])
        self.height.set(self.config['Plot']['height'])
        self.is_same_color.set(int(self.config['Plot']['same color']))
        self.color_1.set(self.config['Plot']['Color 1'])
        self.color_2.set(self.config['Plot']['Color 2'])
        self.color_3.set(self.config['Plot']['Color 3'])
        self.color_4.set(self.config['Plot']['Color 4'])
        self.color_5.set(self.config['Plot']['Color 5'])
        self.color_6.set(self.config['Plot']['Color 6'])
        self.bar_width.set(self.config['Plot']['bar width'])

        self.line_width.set(self.config['Plot']['line width'])
        self.font_family.set(self.config['Plot']['font family'])
        self.font_weight.set(self.config['Plot']['font weight'])
        self.font_size.set(self.config['Plot']['font size'])
        self.title_size.set(self.config['Plot']['title size'])
        self.axis_lw.set(self.config['Plot']['axis line width'])
        self.axis_label_size.set(self.config['Plot']['axis label size'])
        self.axis_label_weight.set(self.config['Plot']['axis label weight'])
        self.axis_xtick_size.set(self.config['Plot']['xtick size'])
        self.axis_ytick_size.set(self.config['Plot']['ytick size'])
        self.legend_fontsize.set(self.config['Plot']['legend font size'])
        self.legend_is_frame.set(int(self.config['Plot']['legend frame']))
        self.capsize.set(self.config['Plot']['Cap size'])

    def create_file(self):
        if not os.path.exists(self.file):
            self.config.add_section('Plot')
            self.config.add_section('Stat')
            self.reset()
            self.write()
        else:
            self.config.read(self.file)
            self.apply()

    def write(self):
        self.write_plot()
        self.write_stat()

        with open(self.file, 'w') as f:
            self.config.write(f)
        self.master.read_setting()

    def write_plot(self):
        self.config['Plot']['Dark Mode'] = str(self.is_dark.get())
        self.config['Plot']['dpi'] = self.dpi.get()
        self.config['Plot']['format'] = self.format.get()
        self.config['Plot']['width'] = self.width.get()
        self.config['Plot']['height'] = self.height.get()
        self.config['Plot']['same color'] = str(self.is_same_color.get())
        self.config['Plot']['Color 1'] = self.color_1.get()
        self.config['Plot']['Color 2'] = self.color_2.get()
        self.config['Plot']['Color 3'] = self.color_3.get()
        self.config['Plot']['Color 4'] = self.color_4.get()
        self.config['Plot']['Color 5'] = self.color_5.get()
        self.config['Plot']['Color 6'] = self.color_6.get()
        self.config['Plot']['bar width'] = self.bar_width.get()
        self.config['Plot']['line width'] = self.line_width.get()
        self.config['Plot']['font family'] = self.font_family.get()
        self.config['Plot']['font weight'] = self.font_weight.get()
        self.config['Plot']['font size'] = self.font_size.get()
        self.config['Plot']['title size'] = self.title_size.get()
        self.config['Plot']['axis line width'] = self.axis_lw.get()
        self.config['Plot']['axis label size'] = self.axis_label_size.get()
        self.config['Plot']['axis label weight'] = self.axis_label_weight.get()
        self.config['Plot']['xtick size'] = self.axis_xtick_size.get()
        self.config['Plot']['ytick size'] = self.axis_ytick_size.get()
        self.config['Plot']['legend font size'] = self.legend_fontsize.get()
        self.config['Plot']['legend frame'] = str(self.legend_is_frame.get())
        self.config['Plot']['Cap size'] = self.capsize.get()

    def write_stat(self):
        pass

    def general(self):
        def pick_color(event):
            from tkinter.colorchooser import askcolor
            _, color = askcolor()
            if color is None:
                return
            event.widget.config(background=color)
            if event.widget == color_label:
                c_tk = self.color_1
            elif event.widget == color_label_2:
                c_tk = self.color_2
            elif event.widget == color_label_3:
                c_tk = self.color_3
            elif event.widget == color_label_4:
                c_tk = self.color_4
            elif event.widget == color_label_5:
                c_tk = self.color_5
            else:
                c_tk = self.color_6
            c_tk.set(color)

        frame = ttk.Frame(self.notebook, padding=5)
        ttk.Checkbutton(frame, text='Dark Mode', variable=self.is_dark).pack(side=tk.TOP, fill=tk.X)
        f_font = ttk.Labelframe(frame, text='Font', padding=5)
        f_font.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(f_font, text='Font: ').grid(row=0, column=0, sticky=tk.E)
        ttk.Combobox(f_font, textvariable=self.font_family,
                     values=['Times New Roman', 'DejaVu Sans', 'Verdana', 'Arial', 'Comic Sans MS']).\
            grid(row=0, column=1, sticky=tk.EW)
        ttk.Label(f_font, text='Weight: ').grid(row=0, column=2, sticky=tk.E)
        ttk.Combobox(f_font, textvariable=self.font_weight,
                     values=['light', 'normal', 'regular', 'bold', 'heavy', 'extra bold', 'black']). \
            grid(row=0, column=3, sticky=tk.EW)
        ttk.Label(f_font, text='Size: ').grid(row=0, column=4, sticky=tk.E)
        ttk.Combobox(f_font, textvariable=self.font_size, values=list(range(1, 32, 1))). \
            grid(row=0, column=5, sticky=tk.EW)

        f_line = ttk.Labelframe(frame, text='Line', padding=5)
        f_line.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(f_line, text='Line width: ').grid(row=0, column=0, sticky=tk.E)
        ttk.Combobox(f_line, textvariable=self.line_width, values=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0]). \
            grid(row=0, column=1, sticky=tk.EW)

        f_image = ttk.Labelframe(frame, text='Images', padding=5)
        f_image.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(f_image, text='Image resolution (dpi): ').grid(row=0, column=0, sticky=tk.E)
        ttk.Entry(f_image, textvariable=self.dpi).grid(row=0, column=1)
        ttk.Label(f_image, text='Save as: ').grid(row=0, column=2, sticky=tk.E)
        ttk.Combobox(f_image, textvariable=self.format, values=['png', 'tif', 'svg', 'pdf'])\
            .grid(row=0, column=3)

        ttk.Label(f_image, text='Image width (inch): ').grid(row=1, column=0, sticky=tk.E)
        ttk.Entry(f_image, textvariable=self.width).grid(row=1, column=1, sticky=tk.EW)
        ttk.Label(f_image, text='Image height (inch): ').grid(row=1, column=2, sticky=tk.E)
        ttk.Entry(f_image, textvariable=self.height).grid(row=1, column=3, sticky=tk.EW)
        ttk.Label(f_image, text='Title size: ').grid(row=2, column=0, sticky=tk.E)
        ttk.Entry(f_image, textvariable=self.title_size).grid(row=2, column=1, columnspan=3, sticky=tk.EW)

        f_axis = ttk.Labelframe(frame, text='Axis', padding=5)
        f_axis.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(f_axis, text='Axis width: ').grid(row=0, column=0, sticky=tk.E)
        ttk.Combobox(f_axis, textvariable=self.axis_lw, values=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]).\
            grid(row=0, column=1, sticky=tk.EW)
        ttk.Label(f_axis, text='Label size: ').grid(row=0, column=2, sticky=tk.E)
        ttk.Combobox(f_axis, textvariable=self.axis_label_size, values=list(range(1, 24, 1))). \
            grid(row=0, column=3, sticky=tk.EW)
        ttk.Label(f_axis, text='Label weight: ').grid(row=0, column=4, sticky=tk.E)
        ttk.Combobox(f_axis, textvariable=self.axis_label_weight,
                     values=['light', 'normal', 'regular', 'bold', 'heavy', 'extra bold', 'black']). \
            grid(row=0, column=5, sticky=tk.EW)
        ttk.Label(f_axis, text='X tick size: ').grid(row=1, column=0, sticky=tk.E)
        ttk.Combobox(f_axis, textvariable=self.axis_xtick_size,
                     values=list(range(1, 20, 1))). \
            grid(row=1, column=1, sticky=tk.EW)
        ttk.Label(f_axis, text='Y tick size: ').grid(row=1, column=2, sticky=tk.E)
        ttk.Combobox(f_axis, textvariable=self.axis_ytick_size,
                     values=list(range(1, 20, 1))). \
            grid(row=1, column=3, sticky=tk.EW)

        f_legend = ttk.Labelframe(frame, text='Legend', padding=5)
        f_legend.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(f_legend, text='Font size: ').grid(row=0, column=0, sticky=tk.E)
        ttk.Combobox(f_legend, textvariable=self.legend_fontsize,
                     values=list(range(1, 20, 1))). \
            grid(row=0, column=1, sticky=tk.EW)
        ttk.Checkbutton(f_legend, text='Frame', variable=self.legend_is_frame).grid(row=0, column=3, sticky=tk.EW)

        f_plot = ttk.Labelframe(frame, text='Style', padding=5)
        f_plot.pack(side=tk.TOP, fill=tk.X)

        f_bar = ttk.Frame(f_plot)
        f_bar.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(f_bar, text='Bar width (%): ').pack(side=tk.LEFT)
        ttk.Combobox(f_bar, textvariable=self.bar_width, values=list(range(20, 150, 10))).pack(side=tk.LEFT)
        ttk.Checkbutton(f_plot, text='Same color for all group', variable=self.is_same_color).\
            pack(side=tk.TOP, anchor=tk.W)

        f_color = ttk.Frame(f_plot)
        f_color.pack(side=tk.TOP)
        color_label = tk.Label(f_color, width=5, background=self.color_1.get(), relief=tk.SUNKEN)
        color_label.grid(row=0, column=0)
        color_label.bind('<1>', pick_color)

        color_label_2 = tk.Label(f_color, width=5, background=self.color_2.get(), relief=tk.SUNKEN)
        color_label_2.grid(row=0, column=1)
        color_label_2.bind('<1>', pick_color)

        color_label_3 = tk.Label(f_color, width=5, background=self.color_3.get(), relief=tk.SUNKEN)
        color_label_3.grid(row=0, column=2)
        color_label_3.bind('<1>', pick_color)

        color_label_4 = tk.Label(f_color, width=5, background=self.color_4.get(), relief=tk.SUNKEN)
        color_label_4.grid(row=0, column=3)
        color_label_4.bind('<1>', pick_color)

        color_label_5 = tk.Label(f_color, width=5, background=self.color_5.get(), relief=tk.SUNKEN)
        color_label_5.grid(row=0, column=4)
        color_label_5.bind('<1>', pick_color)

        color_label_6 = tk.Label(f_color, width=5, background=self.color_6.get(), relief=tk.SUNKEN)
        color_label_6.grid(row=0, column=5)
        color_label_6.bind('<1>', pick_color)

        f_eb = ttk.Frame(f_plot)
        f_eb.pack(side=tk.TOP, anchor=tk.W)
        ttk.Label(f_eb, text='Cap size of ebar: ').grid(row=0, column=0, sticky=tk.E)
        ttk.Combobox(f_eb, values=list(range(30)), textvariable=self.capsize).grid(row=0, column=1)

        self.notebook.add(frame, text='Plot')

    def stat(self):
        pass


if __name__ == '__main__':
    root = tk.Tk()
    pre = Preference(root)

    # pre.notebook.select(2)
    root.mainloop()
