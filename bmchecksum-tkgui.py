"""
BMChecksum: A file hashing program to store and later verify the checksums of files
Copyright (C) 2025 Barrie Millar

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import core as bmc
import tkinter as tk
from tkinter import filedialog, scrolledtext

def browse_directory(directory_textbox):
    """
    Opens a file dialog to select a directory and updates the directory_textbox with the selected path.
    :param directory_textbox: The Entry widget to update with the selected directory path
    """
    
    checksum_directory = filedialog.askdirectory(title="Select Directory")
    if checksum_directory:
        directory_textbox.delete(0, tk.END)
        directory_textbox.insert(0, checksum_directory)


def enclosed_output_display(output_display):
    """
    This function passes in the output_display variable to ensure any 
    internal functions can access it. It has been done to avoid global
    variable use
    :param output_display: The scrolled text widget to display output
    """

    def update_output_display(message):
        """
        Updates the output display with the given message.
        :param message: The message to display in the output area
        """
        output_display.insert(tk.END, message + "\n")
        output_display.update_idletasks()  # Force the UI to update immediately

    return update_output_display

def main():
    """
    The first function run upon program start to create the main application window
    """

    # Create the main application window

    main_window = tk.Tk()
    main_window.title("BMChecksum version 0.2.0")
    main_window.geometry("725x480")

    # Setting main interface row and column weights to 1

    for row in range(4):
        main_window.grid_rowconfigure(row, weight=1)
    main_window.grid_columnconfigure(0, weight=1)

    # Output display section
    
    output_display = scrolledtext.ScrolledText(main_window, wrap=tk.WORD)
    output_display.grid(row=0, column=0, rowspan=4, padx=5, pady=5, sticky=tk.NSEW)
    
    # Interface controls section with a documentation label, a row with directory entry and a buttons panel

    # Set label to wrap as needed based on window size.
    doc_display = tk.Label(main_window, text="Welcome to BMChecksum. Please select the required directory and then the calculate, verify or upgrade buttons to start.", wraplength=main_window.winfo_width() - 20, justify="center")
    main_window.bind("<Configure>", lambda event: doc_display.config(wraplength=event.width - 20))
    doc_display.grid(row=4, column=0, padx=5, pady=5, sticky=tk.EW)    

    # Directory selection panel

    directory_frame = tk.Frame(main_window)
    directory_frame.grid(row=5, column=0, padx=5, pady=5, sticky=tk.EW)
    tk.Label(directory_frame, text="Directory:").pack(side=tk.LEFT, padx=5, pady=5)
    directory_textbox = tk.Entry(directory_frame)
    tk.Button(directory_frame, text="Browse", command=lambda: browse_directory(directory_textbox)).pack(side=tk.RIGHT, padx=5, pady=5)
    directory_textbox.pack(padx=5, pady=5, fill=tk.X, expand=True)

    # Button panel

    button_frame = tk.Frame(main_window)
    button_frame.grid(row=6, column=0, rowspan=3, padx=5, pady=5, sticky=tk.NSEW)
    for cell in range(3):
        button_frame.grid_rowconfigure(cell, weight=1)
        if cell < 2:
            button_frame.grid_columnconfigure(cell, weight=1)
    # Button width set to 35 pixels minimum
    tk.Button(button_frame, width=35, text="Calculate All Checksums", command=lambda: bmc.start_checksum_process(directory_textbox.get(), 0, enclosed_output_display(output_display))).grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)
    tk.Button(button_frame, width=35, text="Calculate MD5 Checksums").grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
    tk.Button(button_frame, width=35, text="Calculate SHA-1 Checksums").grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)
    tk.Button(button_frame, width=35, text="Verify Checksums").grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
    tk.Button(button_frame, width=35, text="Verify Checksums In All Direct Subfolders").grid(row=2, column=0, padx=5, pady=5, sticky=tk.EW)
    tk.Button(button_frame, width=35, text="Upgrade Legacy Checksums").grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

    # Start the Tkinter event loop
    
    main_window.mainloop()

if __name__ == "__main__":
    
    """
    Runs the main function if this code is being run directly.
    """
    
    main()
