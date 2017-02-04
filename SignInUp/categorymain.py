from kivy.base import runTouchApp
from kivy.uix.spinner import Spinner
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.actionbar import ActionBar, ActionButton
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.listview import ListItemButton, ListView
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
import sqlite3
from kivy.adapters.listadapter import ListAdapter

Builder.load_string('''
<profile>:
    dropbtn: dropdownbtn
    ActionBar:
        pos_hint: {'top':1}
        ActionView:
            ActionPrevious:
                with_previous: True
                title: 'User'

            ActionButton:
                text: 'Btn0'
                icon: 'description.png'

    BoxLayout:
        orientation: "vertical"
        padding: "10dp"
        spacing: "30dp"
        BoxLayout:
            size_hint_y: 90
        BoxLayout:
            size_hint_y: 300
            padding: "10dp"
            canvas:
                Color:
                    rgb: [0.129, 0.125, 0.125]
                Rectangle:
                    pos: self.pos
                    size:self.size
            AsyncImage
                source: 'user1.png'
            Label:
                text: "ratings"

            Label:
                text: "Books Viewed"
        BoxLayout:
            size_hint_y: 75
            spacing: "30dp"

            ActionBar:
                pos_hint: {'top':1}
                ActionView:
                    ActionPrevious:
                        with_previous: False
                        app_icon: 'star.png'
                        title: 'Preferences'

                    ActionButton:
                        id: dropdownbtn
                        text: 'Btn0'
                        icon: 'plus1.png'
                        halign: 'left'
                        on_press: root.open()

                    ActionButton:
                        text: 'Btn1'
                        canvas:
                            Color:
                                rgb: [0.129, 0.125, 0.125]
                            Rectangle:
                                pos: self.pos
                                size:self.size

        BoxLayout:
            size_hint_y: 400

        ''')

class profile(Screen):
    dropbtn= ObjectProperty()

    def open(self):
        dropdown = DropDown()
        dropdown.auto_width= False

        items = ['Juvenile Fiction', 'Young Adult\nFiction', 'Performing Arts', 'Drama', 'Literary Criticism',
                 'Children', 'Contests',
                 'Law', 'Social Science', 'Study Aids', 'Juvenile\nNonfiction', 'Biography\n& Autobiography',
                 'Business\n& Economics', 'Man-woman\nrelationships',
                 'History', 'Psychology', 'Pressure vessels', 'Architecture', 'Rivets and\nriveting',
                 'Technology\n& Engineering', 'Stream\nmeasurements']

        for item in items:
            btn = Button(text= item, size_hint_y=None, height=40, size_hint_x=2, width= 200, font_size= '12sp')
            dropdown.add_widget(btn)
            btn.bind(on_press= self.add())
        actionBtn= self.dropbtn
        actionBtn.bind(on_release= dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(actionBtn, 'text', x))

    def add(self):
        conn = sqlite3.connect('booksrecommender.db')





class TestApp(App):
    def build(self):
        return profile()

if __name__ == '__main__':
    TestApp().run()


