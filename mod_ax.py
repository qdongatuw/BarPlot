import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt


font_name = ['Times New Roman',
             'DejaVu Sans',
             'Verdana',
             'Arial',
             'Comic Sans MS']


class CusAxes:
    def __init__(self, axes: plt.Axes):
        self.axes = axes
        self.xticks = self.axes.get_xticks()
        self.yticks = self.axes.get_yticks()
        self.cid = None
        self.connect()

    def connect(self):
        def onclick(event):
            if not event.dblclick:
                return
            if event.inaxes:
                return
            index = 0   # notebook tab_id
            if event.y < self.axes.bbox.y0 and event.x > self.axes.bbox.x0:
                index = 1
            elif event.x < self.axes.bbox.x0 and event.y > self.axes.bbox.y0:
                index = 2
            elif event.x > self.axes.bbox.x0 and event.y > self.axes.bbox.y0:
                index = 0
            self.setting(index)
        self.cid = self.axes.figure.canvas.mpl_connect('button_press_event', onclick)

    def setting(self, tab_id):
        setting = SetDialog(self.axes)
        setting.n.select(tab_id)

    def disconnect(self):
        if not self.cid:
            return
        self.axes.figure.canvas.mpl_disconnect(self.cid)


class SetDialog(tk.Toplevel):
    def __init__(self, axes: plt.Axes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.axes = axes
        self.title('Config axis')
        f_bottom = ttk.Frame(self, padding=5)
        f_bottom.pack(side=tk.BOTTOM, fill=tk.X)
        ttk.Button(f_bottom, text='Apply', command=self.apply_setting).grid(row=0, column=0)
        ttk.Button(f_bottom, text='OK', command=self.ok).grid(row=0, column=1)
        self.n = ttk.Notebook(self)
        self.n.pack(fill=tk.BOTH, expand=1)
        frame_title = ttk.Frame(self.n, padding=5)
        self.n.add(frame_title, text='Title')
        frame_x = ttk.Frame(self.n, padding=5)
        self.n.add(frame_x, text='Axis X')
        frame_y = ttk.Frame(self.n, padding=5)
        self.n.add(frame_y, text='Axis Y')

        self.axes_title_tk = tk.StringVar()
        self.axes_title_tk.set(self.axes.get_title())

        self.axes_title_size_tk = tk.StringVar()
        self.axes_title_size_tk.set(self.axes.title.get_size())
        self.axes_title_font_tk = tk.StringVar()
        self.axes_title_font_tk.set(self.axes.title.get_fontfamily())
        self.axes_title_color_tk = tk.StringVar()
        self.axes_title_color_tk.set(self.axes.title.get_color())
        self.x_label_tk = tk.StringVar()
        self.x_label_tk.set(self.axes.get_xlabel())
        self.x_tick_size_tk = tk.StringVar()
        self.x_tick_size_tk.set('12')
        self.x_tick_rotation_tk = tk.StringVar()
        self.x_tick_rotation_tk.set('30')
        self.y_label_tk = tk.StringVar()
        self.y_label_tk.set(self.axes.get_ylabel())
        self.y_tick_size_tk = tk.StringVar()
        self.y_tick_size_tk.set('12')
        self.x_min_tk = tk.StringVar()
        self.x_max_tk = tk.StringVar()
        self.y_min_tk = tk.StringVar()
        self.y_max_tk = tk.StringVar()
        self.x_min_tk.set(str(self.axes.get_xlim()[0]))
        self.x_max_tk.set(str(self.axes.get_xlim()[1]))
        self.y_min_tk.set(str(self.axes.get_ylim()[0]))
        self.y_max_tk.set(str(self.axes.get_ylim()[1]))

        self.frame_title(frame_title)
        self.x_title(frame_x)
        self.y_title(frame_y)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def frame_title(self, master=None):
        lf1 = ttk.LabelFrame(master, text='Title')
        lf1.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(lf1, text='Title: ').grid(row=0, column=0)
        ttk.Entry(lf1, textvariable=self.axes_title_tk).grid(row=0, column=1)
        ttk.Label(lf1, text='Size: ').grid(row=1, column=0)
        ttk.Combobox(lf1, textvariable=self.axes_title_size_tk, values=[5, 6, 7, 8, 9, 10, 11, 12, 14,
                                                                        16, 18, 20, 24, 28, 36]).grid(row=1, column=1)
        ttk.Label(lf1, text='Font: ').grid(row=2, column=0)
        ttk.Combobox(lf1, textvariable=self.axes_title_font_tk, values=font_name).grid(row=2, column=1)

    def x_title(self, master=None):
        lf1 = ttk.LabelFrame(master, text='X Title')
        lf1.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(lf1, text='X Title: ').grid(row=0, column=0)
        ttk.Entry(lf1, textvariable=self.x_label_tk).grid(row=0, column=1)

        ttk.Label(lf1, text='Ticks Size: ').grid(row=1, column=0)
        ttk.Combobox(lf1, textvariable=self.x_tick_size_tk, values=[5, 6, 7, 8, 9, 10, 11, 12, 14,
                                                                     16, 18, 20, 24, 28, 36]).grid(row=1, column=1)
        ttk.Label(lf1, text='Ticks Rotation: ').grid(row=2, column=0)
        ttk.Combobox(lf1, textvariable=self.x_tick_rotation_tk, values=[0, 30, 45, 60, 90]).grid(row=2, column=1)

        lf2 = ttk.LabelFrame(master, text='X Range')
        lf2.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(lf2, text='Min: ').grid(row=0, column=0)
        ttk.Entry(lf2, textvariable=self.x_min_tk).grid(row=0, column=1)
        ttk.Label(lf2, text='Max: ').grid(row=1, column=0)
        ttk.Entry(lf2, textvariable=self.x_max_tk).grid(row=1, column=1)

    def y_title(self, master=None):
        lf1 = ttk.LabelFrame(master, text='Y Title')
        lf1.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(lf1, text='Y Title: ').grid(row=0, column=0)
        ttk.Entry(lf1, textvariable=self.y_label_tk).grid(row=0, column=1)
        lf2 = ttk.LabelFrame(master, text='Y Range')
        lf2.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(lf2, text='Min: ').grid(row=0, column=0)
        ttk.Entry(lf2, textvariable=self.y_min_tk).grid(row=0, column=1)
        ttk.Label(lf2, text='Max: ').grid(row=1, column=0)
        ttk.Entry(lf2, textvariable=self.y_max_tk).grid(row=1, column=1)

    def apply_setting(self):
        self.axes.set_title(self.axes_title_tk.get())
        self.axes.title.set_size(self.axes_title_size_tk.get())
        self.axes.title.set_fontname(self.axes_title_font_tk.get())

        self.axes.set_xlabel(self.x_label_tk.get())
        self.axes.set_xlim(float(self.x_min_tk.get()), float(self.x_max_tk.get()))
        rotation = float(self.x_tick_rotation_tk.get())
        alignment = 'center'
        if rotation != 0:
            alignment = 'right'
        # self.axes.tick_params(axis='x', labelsize=self.x_tick_size_tk.get(), labelrotation=rotation)
        self.axes.set_xticklabels(self.axes.get_xticklabels(), horizontalalignment=alignment, size=self.x_tick_size_tk.get(), rotation=rotation)
        self.axes.set_ylabel(self.y_label_tk.get())
        self.axes.set_ylim(float(self.y_min_tk.get()), float(self.y_max_tk.get()))
        self.axes.figure.canvas.draw()

    def ok(self):
        self.apply_setting()
        self.destroy()


class DraggableArtist:
    def __init__(self, artist):#plt.Artist):
        self.artist = artist
        self.canvas = self.artist.figure.canvas

        self.press = None
        self.connect()

    def connect(self):
        # '''connect to all the events we need'''
        self.cidpress = self.canvas.mpl_connect('button_press_event', self.on_press)

    def on_press(self, event):
        if event.inaxes != self.artist.axes:
            return
        # 'on button press we will see if the mouse is over us and store some data'
        contains, attrd = self.artist.contains(event)
        if not contains:
            return

        if isinstance(self.artist, plt.Line2D):
            self.xy0 = self.artist.get_xydata()
        self.press = event.xdata, event.ydata
        self.cidrelease = self.artist.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.artist.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_motion(self, event):
        # 'on motion we will move the rect if the mouse is over us'
        if self.press is None:
            return
        if event.inaxes != self.artist.axes:
            return
        xpress, ypress = self.press
        if isinstance(self.artist, plt.Line2D):
            dx = event.xdata - xpress
            dy = event.ydata - ypress
            x = self.xy0.T[0] + dx
            y = self.xy0.T[1] + dy
            self.artist.set_data(x, y)
        elif isinstance(self.artist, plt.Text):
            self.artist.set_position((event.xdata, event.ydata))
        self.canvas.draw()

    def on_release(self, event):
        # 'on release we reset the press data'
        self.press = None
        self.canvas.draw()

    def disconnect(self):
        # 'disconnect all the stored connection ids'
        self.canvas.mpl_disconnect(self.cidpress)
        self.canvas.mpl_disconnect(self.cidrelease)
        self.canvas.mpl_disconnect(self.cidmotion)

    def remove(self):
        del self


class DraggableArtistY(DraggableArtist):
    def __init__(self, line: plt.Line2D, callback=None):
        super().__init__(line)
        self.callback = callback

    def on_motion(self, event):
        # 'on motion we will move the rect if the mouse is over us'
        if self.press is None:
            return
        if event.inaxes != self.artist.axes:
            return
        _, ypress = self.press
        if isinstance(self.artist, plt.Line2D):
            dy = event.ydata - ypress
            y = self.xy0.T[1] + dy
            self.artist.set_ydata(y)
        elif isinstance(self.artist, plt.Text):
            self.artist.set_y(event.ydata)
        self.canvas.draw()

    def on_release(self, event):
        self.press = None
        self.canvas.draw()
        if self.callback:
            self.callback(self.artist.get_ydata()[0])


if __name__ == '__main__':
    f, ax = plt.subplots()
    CusAxes(ax)
    ll, = ax.plot((1,2,3,4,5), (1,2,3,4,5))

    l = ax.axhline(1)
    t = ax.text(ax.get_xlim()[1], ax.get_ylim()[1], 'test')

    t.set_picker(True)
    plt.show()

