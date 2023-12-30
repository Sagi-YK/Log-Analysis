import tkinter as tk
from tkinter import filedialog
import pandas as pd
import os

# Declare search_entry, message_var, and listbox as global variables
search_entry = None
message_var = None
listbox = None

def open_csv():
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not filepath:
        return
    try:
        df = pd.read_csv(filepath, dtype={'column_name': str})
        listbox.delete(0, tk.END)

        # Insert column headings with padding for alignment
        headings = '                   '.join([f"{col:<15}" for col in df.columns])
        listbox.insert(tk.END, headings)

        # Insert data rows with increased spaces, skipping empty columns
        for _, row in df.iterrows():
            non_empty_values = [f"{x:<15}" for x in row if pd.notna(x)]
            row_str = '         '.join(non_empty_values)
            listbox.insert(tk.END, row_str)

        # Reset the message
        message_var.set("")

    except Exception as e:
        # Set an error message
        message_var.set(f"Error reading CSV file: {e}")

def find_text():
    global search_entry, message_var, listbox
    # Reset the message
    message_var.set("")
    search_text = search_entry.get().lower()
    if search_text:
        listbox.selection_clear(0, tk.END)
        items = listbox.get(0, tk.END)
        for i, item in enumerate(items):
            if search_text in item.lower():
                listbox.selection_set(i)
                listbox.see(i)
                break
        else:
            message_var.set(f"Text '{search_text}' not found.")

def find_next():
    global search_entry, message_var, listbox
    # Reset the message
    message_var.set("")
    search_text = search_entry.get().lower()
    if search_text:
        current_selection = listbox.curselection()
        if current_selection:
            current_index = current_selection[0]
            items = listbox.get(current_index + 1, tk.END)
            for i, item in enumerate(items, start=current_index + 1):
                if search_text in item.lower():
                    listbox.selection_clear(0, tk.END)
                    listbox.selection_set(i)
                    listbox.see(i)
                    break
            else:
                message_var.set(f"No more occurrences of '{search_text}'.")
        else:
            message_var.set("No item selected in the listbox.")

def find_previous():
    global search_entry, message_var, listbox
    # Reset the message
    message_var.set("")
    search_text = search_entry.get().lower()
    if search_text:
        current_selection = listbox.curselection()
        if current_selection:
            current_index = current_selection[0]
            items = listbox.get(0, current_index - 1)  # Adjust the range
            for i in reversed(items):
                if search_text in i.lower():
                    listbox.selection_clear(0, tk.END)
                    listbox.selection_set(items.index(i))
                    listbox.see(items.index(i))
                    break
            else:
                message_var.set(f"No previous occurrences of '{search_text}'.")
        else:
            message_var.set("No item selected in the listbox.")

def main():
    global search_entry, message_var, listbox

    # Create the main window
    root = tk.Tk()
    root.title("CSV Viewer")

    # Set the window size
    root.geometry("1200x800")

    # Create a frame to hold the Listbox and scrollbars
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Create a menu
    menu = tk.Menu(root)
    root.config(menu=menu)

    # Add items to the menu
    file_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open File...", command=open_csv)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)

    # Create a label for displaying messages
    message_var = tk.StringVar()
    message_label = tk.Label(frame, textvariable=message_var, fg="red")
    message_label.grid(row=0, column=0, columnspan=2, pady=(10, 5), padx=10, sticky="w")

    # Create an entry for search string
    search_entry = tk.Entry(frame, width=30)  # Set a specific width
    search_entry.grid(row=0, column=2, padx=10, pady=(10, 5), sticky="w")  # Place it to the right of "Search:"
    search_entry_label = tk.Label(frame, text="Search:")
    search_entry_label.grid(row=0, column=1, padx=(0, 5), pady=(10, 5), sticky="e")

    # Create buttons for find, find next, and find previous
    find_button = tk.Button(frame, text="Find", command=find_text)
    find_button.grid(row=0, column=3, padx=(5, 0), pady=5, sticky="ew")

    find_next_button = tk.Button(frame, text="Next", command=find_next)
    find_next_button.grid(row=0, column=4, padx=(5, 0), pady=5, sticky="ew")

    find_previous_button = tk.Button(frame, text="Previous", command=find_previous)
    find_previous_button.grid(row=0, column=5, padx=(5, 0), pady=5, sticky="ew")

    # Create a Listbox to display the CSV content
    listbox = tk.Listbox(frame, justify='left', width=80)  # Adjust the width as needed
    listbox.grid(row=1, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)  # Add padx and pady for left and top margin

    # Create a vertical scrollbar
    v_scrollbar = tk.Scrollbar(frame, command=listbox.yview)
    v_scrollbar.grid(row=1, column=6, sticky="nsew")
    listbox.config(yscrollcommand=v_scrollbar.set)

    # Create a horizontal scrollbar
    h_scrollbar = tk.Scrollbar(frame, command=listbox.xview, orient=tk.HORIZONTAL)
    h_scrollbar.grid(row=2, column=0, columnspan=6, sticky="ew")
    listbox.config(xscrollcommand=h_scrollbar.set)

    # Bind <Return> key to find_text function
    root.bind('<Return>', lambda event=None: find_text())

    # Configure row and column weights
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=0)
    frame.grid_columnconfigure(2, weight=0)
    frame.grid_columnconfigure(3, weight=0)
    frame.grid_columnconfigure(4, weight=0)
    frame.grid_columnconfigure(5, weight=0)
    frame.grid_columnconfigure(6, weight=0)

    # Run the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
