import wx
import wx.grid
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

class Mywin(wx.Frame):
   
   def __init__(self, parent, title): 
      super(Mywin, self).__init__(parent, title = title, size = (800,600)) 
		
      panel = wx.Panel(self) 
      box = wx.BoxSizer(wx.HORIZONTAL)
      
      self.grid = wx.grid.Grid(panel)
      self.grid.CreateGrid(10,8)
      
      self.figure = Figure(figsize =(5,4))
      self.canvas = FigureCanvas(panel, -1, self.figure)
      
      box.Add(self.grid, 1, flag=wx.EXPAND)
      box.Add(self.canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW)
      
      self.Bind(wx.EVT_DROP_FILES, self.on_drop_files)
      self.SetDropTarget(MyFileDropTarget(self))
      
      panel.SetSizerAndFit(box) 
      self.Centre() 
      self.Show(True)
   
   def on_drop_files(self, event):
      paths = event.GetFiles()
      self.load_data(paths[0])
   
   def load_data(self, file_path):
      if file_path.endswith('.csv'):
         df = pd.read_csv(file_path)
      else:
         df = pd.read_excel(file_path)
      
      self.grid.ClearGrid()
      self.grid.DeleteCols(numCols=self.grid.GetNumberCols())
      self.grid.DeleteRows(numRows=self.grid.GetNumberRows())
      
      self.grid.AppendCols(numCols=len(df.columns))
      self.grid.AppendRows(numRows=len(df.index))
      
      for index, col in enumerate(df.columns):
         self.grid.SetColLabelValue(index, col)
         self.grid.SetColSize(index, 100)
      
      for row in range(len(df.index)):
         for col in range(len(df.columns)):
            self.grid.SetCellValue(row, col, str(df.iat[row, col]))
      
      self.plot_data(df)
   
   def plot_data(self, df):
      self.figure.clear()
      ax = self.figure.add_subplot(111)
      ax.plot(df[df.columns[0]], df[df.columns[1]])  # Adjust as necessary
      self.canvas.draw()

class MyFileDropTarget(wx.FileDropTarget):
   
   def __init__(self, window):
      super(MyFileDropTarget, self).__init__()
      self.window = window
   
   def OnDropFiles(self, x, y, filenames):
      self.window.load_data(filenames[0])
      return True

app = wx.App()
Mywin(None,"Drag-and-Drop File into Grid")
app.MainLoop()
