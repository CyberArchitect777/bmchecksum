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

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class BMChecksumGUI(App):

    def build(self):
        """
        Builds the main application interface using Kivy.
        """

        self.window_size = (725, 480)
        self.title = "BMChecksum version 0.3.0"
        self.layout = GridLayout(cols=1, padding=10, spacing=10)

        # Output display section

        output_display = TextInput(readonly=True, size_hint=(1, 4))
        scroll_container = ScrollView(size_hint=(1, 4))
        scroll_container.add_widget(output_display)
        self.layout.add_widget(scroll_container)

        # Interface controls section with a documentation label, a row with directory entry and a buttons panel

        # Set label to wrap as needed based on window size.

        doc_display = Label(text="Welcome to BMChecksum. Please select the required directory and then the calculate, verify or upgrade buttons to start.", size_hint_y=None, height=40)
        self.layout.add_widget(doc_display)
        
        # Directory selection panel
        
        dir_layout = GridLayout(cols=2)
        dir_input = TextInput(hint_text="Select directory", size_hint_x=9, height=20)
        browse_button = Button(text="Browse", size_hint_x=1, height=20)
        dir_layout.add_widget(dir_input)
        dir_layout.add_widget(browse_button)   
        self.layout.add_widget(dir_layout)

        # Button panel

        button_layout = GridLayout(cols=2)
        button_layout.add_widget(Button(text="Calculate All Checksums"))
        button_layout.add_widget(Button(text="Calculate MD5 Checksums"))
        button_layout.add_widget(Button(text="Calculate SHA-1 Checksums"))
        button_layout.add_widget(Button(text="Verify Checksums"))
        button_layout.add_widget(Button(text="Verify Checksums In Subfolders"))
        button_layout.add_widget(Button(text="Upgrade Legacy Checksums"))

        self.layout.add_widget(button_layout)

        return self.layout

if __name__ == "__main__":
    """
    Starts the main class if this code is being run directly.
    """
    BMChecksumGUI().run()
