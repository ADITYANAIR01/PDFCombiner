import os               # draft 3   IMPROVE FUNCTION AND GUI
import subprocess
import sys
from tkinter import Tk, filedialog, Button, Listbox, EXTENDED, messagebox, Label, Scrollbar, RIGHT, Y, BOTH
import time
from tkinter.ttk import Progressbar, Style
import threading

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

class PDFCombinerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Combining Tool by Aditya with ❤️")
        
        # Set window size and position
        window_width = 600
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (window_width / 2)
        y_coordinate = (screen_height / 2) - (window_height / 2)
        root.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")

        # Create a listbox to display selected files with a scrollbar
        self.scrollbar = Scrollbar(root)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        
        self.listbox = Listbox(root, selectmode=EXTENDED, width=50, bg="#ffffff", selectbackground="#b3b3b3", font=("Arial", 12))
        self.listbox.pack(padx=20, pady=20, fill=BOTH)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        # Create buttons with custom style
        button_style = {"font": ("Arial", 12, "bold"), "bg": "#008CBA", "fg": "white", "activebackground": "#004080", "activeforeground": "white", "bd": 0}
        self.select_button = Button(root, text="Select PDFs", command=self.select_files, **button_style)
        self.select_button.pack(pady=5)
        self.combine_button = Button(root, text="Combine PDFs", command=self.combine_selected_pdfs, **button_style)
        self.combine_button.pack(pady=5)

        # Add a label with instructions to hold Ctrl to select multiple PDFs
        self.note_label = Label(root, text="Hold Ctrl to select multiple PDFs", font=("Arial", 10), fg="gray")
        self.note_label.pack(pady=5)

        # Blinking effect for Ctrl message
        self.blink()

        # Progress bar
        self.progress = Progressbar(root, orient='horizontal', mode='determinate', length=400)
        self.progress.pack(pady=10)

    def blink(self):
        current_color = self.note_label.cget("fg")
        new_color = "black" if current_color == "gray" else "gray"
        self.note_label.config(fg=new_color)
        self.root.after(500, self.blink)

    def select_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if not file_paths:
            messagebox.showwarning("Warning", "No PDFs selected.")
        else:
            for file_path in file_paths:
                self.listbox.insert("end", file_path)
            messagebox.showinfo("Info", "PDFs selected. Click the 'Combine Now' button to complete the process.")

    def combine_selected_pdfs(self):
        file_paths = list(self.listbox.get(0, "end"))
        if not file_paths:
            messagebox.showwarning("Warning", "No files selected.")
        else:
            output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title="Choose where to save the combined PDF")
            if output_path:
                threading.Thread(target=self.combine_pdfs, args=(file_paths, output_path)).start()
            else:
                messagebox.showwarning("Warning", "Output path not specified.")

    def combine_pdfs(self, file_paths, output_path):
        pdf_writer = PdfWriter()
        total_files = len(file_paths)

        try:
            for index, file_path in enumerate(file_paths):
                with open(file_path, 'rb') as pdf_file:
                    pdf_reader = PdfReader(pdf_file)
                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)
                self.progress['value'] = ((index + 1) / total_files) * 100
                self.root.update_idletasks()

            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
                messagebox.showinfo("Success", f"Combined PDF saved as {output_path}. Create Unified PDFs in a Snap!")
                self.root.destroy()  # Exit the program after success
        except Exception as e:
            messagebox.showerror("Error", f"Error combining/saving PDF: {e}")

# Main code to create the Tkinter window and run the application
root = Tk()
app = PDFCombinerApp(root)
root.mainloop()
