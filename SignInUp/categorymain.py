from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import sqlite3
from MainUI.UserLogin import Login

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
                        on_press:
                            root.select()


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

<SelectPopup>:
    title: 'Category of Books'
    size_hint: None, None
    size: 500, 500
    auto_dismiss: True
    GridLayout:
        cols: 2
        Label:
            text: 'Juvenile Fiction'
        CheckBox:
            on_active: root.add('Juvenile Fiction')
        Label:
            text: 'Young Adult Fiction'
        CheckBox:
            on_active: root.add('Young Adult Fiction')
        Label:
            text: 'Performing Arts'
        CheckBox:
            on_active: app.root.color = 'Blue'
        Label:
            text: 'Drama'
        CheckBox:
            on_active: app.root.color = 'Blue'
        Label:
            text: 'Literary Criticism'
        CheckBox:
            on_active: app.root.color = 'Blue'
        Label:
            text: 'Children'
        CheckBox:
            on_active: app.root.color = 'Blue'
        Label:
            text: 'Contests'
        CheckBox:
            on_active: app.root.color = 'Blue'
        Label:
            text: 'Law'
        CheckBox:
            on_active: app.root.color = 'Blue'
        Label:
            text: 'Social Science'
        CheckBox:
            on_active: app.root.color = 'Blue'
        Label:
            text: 'Study Aids'
        CheckBox:
            on_active: app.root.color = 'Blue'
        Label:
            text: 'Juvenile Nonfiction'
        CheckBox:
            on_active: app.root.color = 'Blue'
        Label:
            text: 'Biography & Autobiography'
        CheckBox:
            on_active: app.root.color = 'Blue'
        Label:
            text: 'Business & Economics'
        CheckBox:
            on_active: app.root.color = 'Blue'
        Label:
            text: 'Man-woman relationships'
        CheckBox:
            on_active: app.root.color = 'Blue'
        Label:
            text: 'History'
        CheckBox:
            on_active: app.root.color = 'Blue'
        Label:
            text: 'Psychology'
        CheckBox:
            on_active: app.root.color = 'Blue'
        Label:
            text: 'Technology& Engineering'
        CheckBox:
            on_active: app.root.color = 'Blue'

        ''')
class SelectPopup(Popup):
    def add(self, x):
        conn = sqlite3.connect('booksrecommender.db')
        cursor = conn.cursor()
        # cursor.execute("INSERT INTO UserPreferences VALUES (NULL, ?, ? )", (username, password));
        conn.commit()

        print(x)


class profile(Screen):
    def select(self):
        SelectPopup().open()

        user= Login.getUsername(self)
        print(user)

class TestApp(App):
    def build(self):
        return profile()

if __name__ == '__main__':
    TestApp().run()


