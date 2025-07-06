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

import os
import threading
import core as bmc

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

from plyer import filechooser

class BMChecksumGUI(App):

    def build(self):
        """
        Builds the main application interface using Kivy.
        :return: The main layout of the application.
        """
        
        self.window_size = (725, 480)
        self.title = "BMChecksum version 0.3.0"
        self.layout = GridLayout(cols=1, padding=10, spacing=10)

        # Output display section

        self.output_display = TextInput(readonly=True, size_hint=(1, 4))
        self.scroll_container = ScrollView(size_hint=(1, 4))
        self.scroll_container.add_widget(self.output_display)
        self.layout.add_widget(self.scroll_container)

        # Interface controls section with a documentation label, a row with directory entry and a buttons panel

        # Set label to wrap as needed based on window size.

        doc_display = Label(text="Welcome to BMChecksum. Please select the required directory and then the calculate, verify or upgrade buttons to start.", size_hint_y=None, height=40, text_size=(725, None), halign="center", valign="center")
        self.layout.add_widget(doc_display)
        
        # Directory selection panel
        
        dir_layout = GridLayout(cols=2, height=30, size_hint_y=None)
        self.dir_input = TextInput(hint_text="Select directory", size_hint_x=9)
        self.dir_input.bind(text=self.check_directory_validity)
        browse_button = Button(text="Browse", size_hint_x=1)
        browse_button.bind(on_release=self.open_plyer_selector)
        dir_layout.add_widget(self.dir_input)
        dir_layout.add_widget(browse_button)
        self.layout.add_widget(dir_layout)

        # Button panel

        self.button_layout = GridLayout(cols=2)

        buttons = [
            ("Calculate All Checksums", lambda _: threading.Thread(target=lambda: self.start_operation(0), daemon=True).start()),
            ("Calculate MD5 Checksums", lambda _: threading.Thread(target=lambda: self.start_operation(1), daemon=True).start()),
            ("Calculate SHA-1 Checksums", lambda _: threading.Thread(target=lambda: self.start_operation(2), daemon=True).start()),
            ("Verify Checksums", lambda _: threading.Thread(target=lambda: self.start_operation(3), daemon=True).start()),
            ("Verify Checksums In Subfolders", lambda _: threading.Thread(target=lambda: self.start_operation(4), daemon=True).start()),
            ("Upgrade Legacy Checksums", lambda _: threading.Thread(target=lambda: self.start_operation(5), daemon=True).start()),
        ]

        for text, action in buttons:
            action_button = Button(text=text)
            action_button.bind(on_release=action)
            self.button_layout.add_widget(action_button)
        
        # Disable buttons initially
        for button in self.button_layout.children:
            button.disabled = True
        
        self.layout.add_widget(self.button_layout)

        return self.layout
    
    def clear_output_display(self):
        """
        Designed to allow a thread other than the main one to clear the output display.
        """
        Clock.schedule_once(lambda dt: self.immediately_clear_output_display())

    def immediately_clear_output_display(self):
        """
        Immediately clears the output display.
        """
        self.output_display.text = ""

    def start_operation(self, button_index):
        """
        Starts the operation based on the button index.
        :button_index: The index number of the button that was pressed.
        """
        # Clear the output display
        self.clear_output_display()

        # Disable all buttons to prevent multiple clicks
        for button in self.button_layout.children:
            button.disabled = True
        
        # Start the appropriate thread based on the button index
        if button_index == 0:
            bmc.start_checksum_process(self.dir_input.text, 0, self.update_output_display)
        elif button_index == 1:
            bmc.start_checksum_process(self.dir_input.text, 1, self.update_output_display)
        elif button_index == 2:
            bmc.start_checksum_process(self.dir_input.text, 2, self.update_output_display)
        elif button_index == 3:
            bmc.start_verification_process(self.dir_input.text, False, self.update_output_display)
        elif button_index == 4:
            bmc.verify_all_checksums_in_all_direct_subdirectories(self.dir_input.text, self.update_output_display)
        elif button_index == 5:
            bmc.start_upgrade_process(self.dir_input.text, self.update_output_display)

        # Re-enable buttons after the operation is complete
        for button in self.button_layout.children:
            button.disabled = False

    def update_output_display(self, text):
        """
        Designed to allow the core functionality thread to update the Kivy interface
        :text: The text to append to output_display.
        """
        # Call the function that actually provides the display update code
        Clock.schedule_once(lambda dt: self.immediately_update_display(text))

    def immediately_update_display(self, text):
        """
        Immediately updates the display.
        :text: The text to append.
        """
        self.output_display.text += text + "\n"
        # Scroll to the top of the output display
        self.scroll_container.scroll_y = 1
    
    def check_directory_validity(self, directory, *args):
        """
        Validates the selected directory and enables/disables buttons accordingly.
        :directory: The directory path to validate.
        :args: Additional unneeded arguments.
        :return: True if valid, False otherwise.
        """
        # Check if the directory exists and is a directory
        if os.path.isdir(directory.text):
            # Enable buttons based on the selected directory
            for button in self.button_layout.children:
                button.disabled = False
        else:
            # Disable buttons if the directory is invalid
            for button in self.button_layout.children:
                button.disabled = True
    
    def open_plyer_selector(self, instance):
        """
        Opens the directory selection box using plyer.
        :instance: The button instance that triggered the event.
        """

        filechooser.choose_dir(title="Select Directory", on_selection=self.process_plyer_selection)

    def process_plyer_selection(self, dir_selection):
        """
        Processes the directory selection output
        :dir_selection: The selected directory path.
        """

        if dir_selection:
            dir_path = dir_selection[0]
            # Update the TextInput with the selected directory path
            self.dir_input.text = dir_path
            # Move back the cursor in the directory box to the start
            self.dir_input.cursor = (0, 0)
            # Enable buttons based on the selected directory
            for button in self.button_layout.children:
                button.disabled = False
        else:
            # Disable buttons if no directory is selected
            for button in self.button_layout.children:
                button.disabled = True

if __name__ == "__main__":
    """
    Starts the main class if this code is being run directly.
    """
    BMChecksumGUI().run()
