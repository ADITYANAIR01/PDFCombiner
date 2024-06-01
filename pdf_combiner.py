import os               # draft 2 IMPROVED GUI
import subprocess
import sys
from tkinter import Tk, filedialog, Button, Listbox, EXTENDED, messagebox, Label
import time

# Function to install packages
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install required packages
required_packages = ["PyPDF2", "fpdf"]
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install_package(package)

from PyPDF2 import PdfWriter, PdfReader

# Function to combine PDFs
def combine_pdfs(file_paths, output_path):
    pdf_writer = PdfWriter()
    
    for file_path in file_paths:
        try:
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
        except Exception as e:
            print(f"Error combining {file_path}: {e}")
    
    try:
        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)
            messagebox.showinfo("Success", f"Combined PDF saved as {output_path}. Create Unified PDFs in a Snap!")
            root.destroy()  # Exit the program after success
    except Exception as e:
        print(f"Error saving combined PDF: {e}")

# Function to select files
def select_files():
    """Opens a file dialog to select PDF files and adds them to the listbox."""
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if not file_paths:
        messagebox.showwarning("Warning", "No PDFs selected.")
    else:
        for file_path in file_paths:
            listbox.insert("end", file_path)
        messagebox.showinfo("Info", "PDFs selected. Click the 'Combine Now' button to complete the process.")

# Function to combine selected PDFs
def combine_selected_pdfs():
    """Combines selected PDFs into a single PDF."""
    file_paths = list(listbox.get(0, "end"))
    if not file_paths:
        messagebox.showwarning("Warning", "No files selected.")
    else:
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], 
                                                    title="Choose where to save the combined PDF")
        if output_path:
            combine_pdfs(file_paths, output_path)
        else:
            messagebox.showwarning("Warning", "Output path not specified.")

# Create the main application window
root = Tk()
root.title("PDF Combining Tool by Aditya with ❤️")

# Set window size and position
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
root.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")

# Create a listbox to display selected files
listbox = Listbox(root, selectmode=EXTENDED, width=50, bg="#ffffff", selectbackground="#b3b3b3", font=("Arial", 12))
listbox.pack(padx=20, pady=20)

# Create buttons with custom style
button_style = {"font": ("Arial", 12, "bold"), "bg": "#008CBA", "fg": "white", "activebackground": "#004080", "activeforeground": "white", "bd": 0}
select_button = Button(root, text="Select PDFs", command=select_files, **button_style)
select_button.pack(pady=5)
combine_button = Button(root, text="Combine PDFs", command=combine_selected_pdfs, **button_style)
combine_button.pack(pady=5)

# Add a label with instructions to hold Ctrl to select multiple PDFs
note_label = Label(root, text="Hold Ctrl to select multiple PDFs", font=("Arial", 10), fg="gray")
note_label.pack(pady=5)

# Blinking effect for Ctrl message
def blink():
    note_label.config(fg="black")
    root.update()
    time.sleep(0.5)
    note_label.config(fg="gray")
    root.update()
    time.sleep(0.5)

while True:
    blink()

root.mainloop()
 