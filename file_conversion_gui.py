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
        self.master.geometry("600x400")

        # Set a background color for the main window
        self.master.configure(bg="#f0f8ff")  # AliceBlue, for example

        # Track selected file path
        self.file_path = None

        # GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Define a custom font. Tkinter will default if Papyrus is not installed.
        # Feel free to try "Jokerman", "Lucida Handwriting", or any other font you prefer.
        custom_font = ("Papyrus", 12)

        # Button to browse a file
        self.browse_btn = tk.Button(
            self.master,
            text="Select File",
            command=self.select_file,
            bg="#7FFFD4",         # Aquamarine button color
            fg="#000000",         # Black text
            font=custom_font
        )
        self.browse_btn.grid(row=0, column=0, padx=10, pady=10)

        # Label to display the selected file
        self.file_label = tk.Label(
            self.master,
            text="No file selected",
            bg="#f0f8ff",         # Match window background
            fg="#000000",
            font=custom_font
        )
        self.file_label.grid(row=0, column=1, padx=10, pady=10)

        # Output format label
        self.output_format_label = tk.Label(
            self.master,
            text="Output Format:",
            bg="#f0f8ff",
            fg="#000000",
            font=custom_font
        )
        self.output_format_label.grid(row=1, column=0, padx=10, pady=10)

        # Dropdown for output format (images in this example)
        self.available_formats = ["PNG", "JPEG", "GIF", "BMP", "WEBP", "TIFF"]
        self.selected_format = tk.StringVar()
        self.selected_format.set(self.available_formats[0])  # default value
        
        # OptionMenu can be tricky to style thoroughly, but we can set some basics:
        self.format_dropdown = tk.OptionMenu(self.master, self.selected_format, *self.available_formats)
        self.format_dropdown.config(
            bg="#7FFFD4",
            fg="#000000",
            activebackground="#98FB98",  # PaleGreen
            font=custom_font
        )
        # The underlying menu can be styled separately:
        self.format_dropdown["menu"].config(
            bg="#7FFFD4",
            fg="#000000",
            font=custom_font
        )
        self.format_dropdown.grid(row=1, column=1, padx=10, pady=10)

        # Convert button
        self.convert_btn = tk.Button(
            self.master,
            text="Convert",
            command=self.convert_file,
            bg="#7FFFD4",
            fg="#000000",
            font=custom_font
        )
        self.convert_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

        # Status label
        self.status_label = tk.Label(
            self.master,
            text="",
            bg="#f0f8ff",
            fg="blue",
            font=custom_font
        )
        self.status_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

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
            # For demonstration, let's assume the file is an image.
            with Image.open(self.file_path) as img:
                output_format = self.selected_format.get()
                base_name, _ = os.path.splitext(self.file_path)
                output_file = f"{base_name}_converted.{output_format.lower()}"

                img.save(output_file, output_format)

                success_msg = f"File converted and saved as {output_file}"
                self.status_label.config(text=success_msg, fg="green")
                logging.info(success_msg)

                messagebox.showinfo("Conversion Successful", success_msg)

        except Exception as e:
            error_msg = f"Conversion failed: {e}"
            self.status_label.config(text=error_msg, fg="red")
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
