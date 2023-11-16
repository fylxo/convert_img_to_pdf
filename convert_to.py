import os
import img2pdf
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def natural_sort_key(s):
    import re
    return [int(c) if c.isdigit() else c.lower() for c in re.split('([0-9]+)', s)]

def convert_images_to_pdf(image_folder, output_pdf):
    image_paths = []
    skipped_files = []  # List of ignored files
    
    for root, dirs, files in os.walk(image_folder):
        for file in files:
            if file.lower().endswith('.jpg'):
                image_paths.append(os.path.join(root, file))
            else:
                skipped_files.append(os.path.join(root, file))  # Add the full file path to the list of ignored files
    
    image_paths.sort(key=natural_sort_key)
    
    if skipped_files:
        skipped_files_message = "The following files were not included in the conversion because they are not in JPG format:\n"
        for file in skipped_files:
            skipped_files_message += file + "\n"
        messagebox.showwarning("Warning", skipped_files_message)
    
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(image_paths))

def select_image_folder():
    folder_path = filedialog.askdirectory()
    image_folder_entry.delete(0, tk.END)
    image_folder_entry.insert(tk.END, folder_path)
    if folder_path:
        image_folder_button.configure(style="Selected.TButton")
    else:
        image_folder_button.configure(style="TButton")

def select_output_pdf():
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    output_pdf_entry.delete(0, tk.END)
    output_pdf_entry.insert(tk.END, output_path)
    if output_path:
        output_pdf_button.configure(style="Selected.TButton")
    else:
        output_pdf_button.configure(style="TButton")

def convert_to_pdf():
    image_folder = image_folder_entry.get()
    output_pdf = output_pdf_entry.get()
    
    if not image_folder:
        messagebox.showerror("Error", "Select an image folder.")
        return
    
    if not output_pdf:
        messagebox.showerror("Error", "Select an output folder for the PDF.")
        return
    
    convert_images_to_pdf(image_folder, output_pdf)
    messagebox.showinfo("Completed", "PDF conversion completed successfully.")
    
    # Remove green color from buttons
    image_folder_button.configure(style="TButton")
    output_pdf_button.configure(style="TButton")

# GUI Creation
window = tk.Tk()
window.title("Image to PDF Converter")
window.geometry("300x200")
window.resizable(False, False)
window.configure(bg="#ffffff")

# Button Style
style = ttk.Style()
style.configure("Selected.TButton", background="#00ff00")  # Green color for the selected button

# Main Frame
main_frame = ttk.Frame(window, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Button for selecting the image folder
image_folder_button = ttk.Button(main_frame, text="Input", command=select_image_folder)
image_folder_button.pack(pady=10)

# Button for selecting the output PDF folder
output_pdf_button = ttk.Button(main_frame, text="Output", command=select_output_pdf)
output_pdf_button.pack(pady=10)

# Conversion button
convert_button = ttk.Button(main_frame, text="Convert to PDF", command=convert_to_pdf)
convert_button.pack(pady=10)

# Entry for the image folder path
image_folder_entry = ttk.Entry(main_frame)
image_folder_entry.pack()

# Entry for the output PDF path
output_pdf_entry = ttk.Entry(main_frame)
output_pdf_entry.pack()

window.mainloop()