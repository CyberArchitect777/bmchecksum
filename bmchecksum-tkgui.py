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

def browse_directory(entry):
        directory = filedialog.askdirectory()
        if directory:
            entry.delete(0, tk.END)
            entry.insert(0, directory)

def main():
    """
    The first function run upon program start to create the main application window
    """

    # Create the main application window

    main_window = tk.Tk()
    main_window.title("BMChecksum version 0.2.0")
    main_window.geometry("800x400")  # Set the window size

    # Output display section

    output_display = scrolledtext.ScrolledText(main_window, height=12, wrap=tk.WORD)
    output_display.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

    # Interface controls section with a documentation label, a row with directory entry and a buttons panel

    controls_frame = tk.Frame(main_window)
    controls_frame.pack(fill=tk.X, padx=10, pady=5)
    doc_display = tk.Label(controls_frame, text="Welcome to BMChecksum. Please select the required directory and then the calculate, verify or upgrade buttons to start.")
    doc_display.pack(fill=tk.X, padx=10, pady=5)
    directory_frame = tk.Frame(controls_frame)
    directory_frame.pack(fill=tk.X, padx=10, pady=5, expand=True)
    # Ensure the middle element stretches to take up more of the available space
    directory_frame.grid_columnconfigure(0, weight=1)
    directory_frame.grid_columnconfigure(1, weight=3)
    directory_frame.grid_columnconfigure(2, weight=1)
    tk.Label(directory_frame, text="Directory:").grid(row=0, column=0, padx=5, pady=5)
    tk.Entry(directory_frame).grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
    tk.Button(directory_frame, text="Browse", command=lambda: browse_directory(directory_frame)).grid(row=0, column=2, padx=5, pady=5)
    button_frame = tk.Frame(controls_frame)
    button_frame.pack(fill=tk.X, padx=10, pady=5, expand=True)
    # Set the button panel to have even weights for all grid rows and columns
    for number in range(3):
        button_frame.grid_rowconfigure(number, weight=1)
    for number in range(2):
        button_frame.grid_columnconfigure(number, weight=1)
    tk.Button(button_frame, width=35, text="Calculate All Checksums").grid(row=0, column=0, padx=5, pady=5)
    tk.Button(button_frame, width=35, text="Calculate MD5 Checksums").grid(row=0, column=1, padx=5, pady=5)
    tk.Button(button_frame, width=35, text="Calculate SHA-1 Checksums").grid(row=1, column=0, padx=5, pady=5)
    tk.Button(button_frame, width=35, text="Verify Checksums").grid(row=1, column=1, padx=5, pady=5)
    tk.Button(button_frame, width=35, text="Verify Checksums In All Direct Subfolders").grid(row=2, column=0, padx=5, pady=5)
    tk.Button(button_frame, width=35, text="Upgrade Legacy Checksums").grid(row=2, column=1, padx=5, pady=5)

    # Start the Tkinter event loop
    
    main_window.mainloop()

if __name__ == "__main__":
    
    """
    Runs the main function if this code is being run directly.
    """
    
    main()
