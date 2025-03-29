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

    output_display = scrolledtext.ScrolledText(main_window, height=4, wrap=tk.WORD)
    output_display.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

    # Directory input section

    directory_frame = tk.Frame(main_window)
    directory_frame.pack(fill=tk.X, padx=10, pady=15)
    tk.Label(directory_frame, text="Directory:").pack(side=tk.LEFT, padx=5)
    directory_entry = tk.Entry(directory_frame)
    directory_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    browse_button = tk.Button(directory_frame, text="Browse", command=lambda: browse_directory(directory_entry))
    browse_button.pack(side=tk.RIGHT, padx=5)

    # Button section in a grid

    button_frame = tk.Frame(main_window)
    button_frame.pack(fill=tk.BOTH, padx=10, pady=15, expand=True)
    tk.Button(button_frame, text="Calculate All Checksums").grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)
    tk.Button(button_frame, text="Calculate MD5 Checksums").grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
    tk.Button(button_frame, text="Calculate SHA-1 Checksums").grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)
    tk.Button(button_frame, text="Verify Checksums").grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
    tk.Button(button_frame, text="Verify Checksums In All Direct Subfolders").grid(row=2, column=0, padx=5, pady=5, sticky=tk.EW)
    tk.Button(button_frame, text="Upgrade Legacy Checksums").grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

    # Start the Tkinter event loop
    
    main_window.mainloop()

if __name__ == "__main__":
    
    """
    Runs the main function if this code is being run directly.
    """
    
    main()
