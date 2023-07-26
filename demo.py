import tkinter as tk
from tkinter import ttk

def on_edit(event):
    # Get the current item and column
    item = treeview.focus()
    column = treeview.identify_column(event.x)

    # Get the current value of the cell
    current_value = treeview.set(item, column)

    # Create an Entry widget to allow editing
    entry = tk.Entry(treeview, justify='center')
    entry.insert(0, current_value)

    # Place the Entry widget over the cell and set focus
    bbox = treeview.bbox(item, column)
    entry.place(x=bbox[0], y=bbox[1], width=bbox[2]-bbox[0], height=bbox[3]-bbox[1])
    entry.focus()

    # Bind the Entry widget to save the edited value when focus is lost
    entry.bind('<FocusOut>', lambda event: save_edited_value(item, column, entry.get()))

def save_edited_value(item, column, new_value):
    # Save the edited value to the Treeview
    treeview.set(item, column, new_value)

    # Destroy the Entry widget
    entry = treeview.focus_get()
    entry.destroy()

# Sample DataFrame
import pandas as pd
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 22],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
df = pd.DataFrame(data)

root = tk.Tk()
root.title("Editable Treeview")

# Create the Treeview
treeview = ttk.Treeview(root)
treeview.pack(fill='both', expand=True)

# Define column names
columns = df.columns.tolist()

# Insert columns into Treeview
treeview['columns'] = columns
for col in columns:
    treeview.heading(col, text=col)
    treeview.column(col, width=100)

# Insert data rows into Treeview
for _, row in df.iterrows():
    treeview.insert('', 'end', values=row.tolist())

# Bind the <<TreeviewEdit>> event to the on_edit function
treeview.bind('<<TreeviewEdit>>', on_edit)

root.mainloop()
