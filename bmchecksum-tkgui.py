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
import os

def browse_directory(directory_textbox):
    """
    Opens a file dialog to select a directory and updates the directory_textbox with the selected path.
    :param directory_textbox: The Entry widget to update with the selected directory path
    """
    
    checksum_directory = filedialog.askdirectory(title="Select Directory")
    if checksum_directory:
        if os.name == 'nt':  # Check if the operating system is Windows
            checksum_directory = checksum_directory.replace("/", "\\")  # Ensure Windows standard paths
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

def validate_directory(directory_textbox, buttons):
    """
    Validates the directory path in the directory_textbox and enables/disables buttons accordingly.
    :param directory_textbox: The Entry widget containing the directory path
    :param buttons: A list of button widgets to enable/disable
    """
    directory = directory_textbox.get()
    if os.path.isdir(directory):  # Check if the path is a valid directory
        disable_interface_buttons(buttons, False)  # Enable buttons
    else:
        disable_interface_buttons(buttons, True)  # Disable buttons

def disable_interface_buttons(buttons, state):
    """
    Sets whether the passed buttons are disabled or not
    :param buttons: A list of button widgets to enable/disable
    :param state: True for disabled
    """
    for button in buttons:
        if state == True:
            button.config(state=tk.DISABLED)  # Set button state
        else:
            button.config(state=tk.NORMAL)

def main():
    """
    The first function run upon program start to create the main application window using Tkinter
    """

    # Create the main application window

    main_window = tk.Tk()
    main_window.title("BMChecksum version 0.2.0")
    main_window.geometry("725x480")

    # Add PNG image as an application icon
    
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "assets" + os.sep + "images" + os.sep + "mainicon.png")
        main_window.iconphoto(False, tk.PhotoImage(file=icon_path))
    except Exception as e:
        print(f"Error loading icon: {e}")

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
    # Button list for later access. Width set to 35 pixels minimum
    buttons = [
    tk.Button(button_frame, width=35, text="Calculate All Checksums", command=lambda: (output_display.delete(1.0, tk.END), bmc.start_checksum_process(directory_textbox.get(), 0, enclosed_output_display(output_display)))),
    tk.Button(button_frame, width=35, text="Calculate MD5 Checksums", command=lambda: (output_display.delete(1.0, tk.END), bmc.start_checksum_process(directory_textbox.get(), 1, enclosed_output_display(output_display)))),
    tk.Button(button_frame, width=35, text="Calculate SHA-1 Checksums", command=lambda: (output_display.delete(1.0, tk.END), bmc.start_checksum_process(directory_textbox.get(), 2, enclosed_output_display(output_display)))),
    tk.Button(button_frame, width=35, text="Verify Checksums", command=lambda: (output_display.delete(1.0, tk.END), bmc.start_verification_process(directory_textbox.get(), False, enclosed_output_display(output_display)))),
    tk.Button(button_frame, width=35, text="Verify Checksums In All Direct Subfolders", command=lambda: (output_display.delete(1.0, tk.END), bmc.verify_all_checksums_in_all_direct_subdirectories(directory_textbox.get(), enclosed_output_display(output_display)))),
    tk.Button(button_frame, width=35, text="Upgrade Legacy Checksums", command=lambda: (output_display.delete(1.0, tk.END), bmc.start_upgrade_process(directory_textbox.get(), enclosed_output_display(output_display)))),
    ]

    buttons[0].grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)
    buttons[1].grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
    buttons[2].grid(row=1, column=0, padx=5, pady=5, sticky=tk.EW)
    buttons[3].grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
    buttons[4].grid(row=2, column=0, padx=5, pady=5, sticky=tk.EW)
    buttons[5].grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

    # Disable buttons initially
    disable_interface_buttons(buttons, True)

    directory_textbox_var = tk.StringVar()
    directory_textbox_var.trace_add("write", lambda *args: validate_directory(directory_textbox, buttons))
    directory_textbox.config(textvariable=directory_textbox_var)

    # Start the Tkinter event loop
    
    main_window.mainloop()

if __name__ == "__main__":
    
    """
    Runs the main function if this code is being run directly.
    """
    
    main()
