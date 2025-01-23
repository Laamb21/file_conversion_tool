import tkinter as tk
from tkinter import filedialog, messagebox
import os
import logging
from PIL import Image

# Configure logging
logging.basicConfig(
    filename='conversion.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

class FileConversionTool:
    def __init__(self, master):
        self.master = master
        self.master.title("File Conversion Tool")

        # Make the window bigger
        self.master.geometry("800x600")

        # Set a background color for the main window
        self.master.configure(bg="#333333")  # Dark gray for the window

        # Track selected file path
        self.file_path = None

        # Create a container frame to center all elements
        self.container = tk.Frame(self.master, bg="#333333")
        self.container.pack(expand=True, fill='both')

        # GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Define a more legible font
        custom_font = ("Helvetica", 14)

        # Button to browse a file
        self.browse_btn = tk.Button(
            self.container,
            text="Select File",
            command=self.select_file,
            bg="#444444",         # Slightly lighter dark gray
            fg="#FFFFFF",         # White text
            font=custom_font
        )
        self.browse_btn.pack(pady=10, anchor="center")

        # Label to display the selected file
        self.file_label = tk.Label(
            self.container,
            text="No file selected",
            bg="#333333",         # Match container background
            fg="#FFFFFF",
            font=custom_font
        )
        self.file_label.pack(pady=5, anchor="center")

        # Output format label
        self.output_format_label = tk.Label(
            self.container,
            text="Output Format:",
            bg="#333333",
            fg="#FFFFFF",
            font=custom_font
        )
        self.output_format_label.pack(pady=5, anchor="center")

        # Dropdown for output format (images in this example)
        self.available_formats = ["PNG", "JPEG", "GIF", "BMP", "WEBP", "TIFF"]
        self.selected_format = tk.StringVar()
        self.selected_format.set(self.available_formats[0])  # default value

        # OptionMenu
        self.format_dropdown = tk.OptionMenu(self.container, self.selected_format, *self.available_formats)
        self.format_dropdown.config(
            bg="#444444",
            fg="#FFFFFF",
            activebackground="#555555",
            activeforeground="#FFFFFF",
            font=custom_font
        )
        # Style the dropdown menu items
        self.format_dropdown["menu"].config(
            bg="#444444",
            fg="#FFFFFF",
            font=custom_font
        )
        self.format_dropdown.pack(pady=5)

        # Convert button
        self.convert_btn = tk.Button(
            self.container,
            text="Convert",
            command=self.convert_file,
            bg="#444444",
            fg="#FFFFFF",
            font=custom_font
        )
        self.convert_btn.pack(pady=10, anchor="center")

        # Status label
        self.status_label = tk.Label(
            self.container,
            text="",
            bg="#333333",
            fg="#FFFFFF",
            font=custom_font
        )
        self.status_label.pack(pady=5, anchor="center")

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            logging.info(f"Selected file: {file_path}")

    def convert_file(self):
        if not self.file_path:
            messagebox.showwarning("No File Selected", "Please select a file to convert.")
            return

        try:
            # For demonstration, let's assume the file is an image
            with Image.open(self.file_path) as img:
                output_format = self.selected_format.get()
                base_name, _ = os.path.splitext(self.file_path)
                output_file = f"{base_name}_converted.{output_format.lower()}"

                img.save(output_file, output_format)

                success_msg = f"File converted and saved as {output_file}"
                self.status_label.config(text=success_msg, fg="#00FF00")  # Green success text
                logging.info(success_msg)
                messagebox.showinfo("Conversion Successful", success_msg)

        except Exception as e:
            error_msg = f"Conversion failed: {e}"
            self.status_label.config(text=error_msg, fg="#FF0000")  # Red error text
            logging.error(error_msg, exc_info=True)
            messagebox.showerror(
                "Conversion Error",
                f"An error occurred while converting your file:\n\n{e}\n\n"
                "Possible fixes:\n"
                "1. Check if the file is a valid image.\n"
                "2. Make sure you have permission to read/write the file.\n"
                "3. Try a different format."
            )

def main():
    root = tk.Tk()
    app = FileConversionTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
