from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from SignInUp.signinmain import SignInForm
from SignInUp.categorymain import profile

Builder.load_string('''
<RootScreen>:
    profile:
    SignInForm:
    SignUpForm:

<SignInForm>:
    username_box: username_input
    password_box: password_input

    BoxLayout:
        orientation: "vertical"
        size_hint_y: None
        height: "500dp"
        padding: "10dp"

        Label:
            text: 'Books Recommender'
            font_size: 40

        GridLayout:
            cols: 2
            row_default_height: "50dp"
            row_force_default: True
            spacing: "10dp"
            padding: "10dp"

            Label:
                text: "Username"
                size_hint_x: None
                width: "200dp"

            TextInput:
                id: username_input
                size_hint_x: None
                width: "500dp"
            Label:
                text: "Password"
            TextInput:
                password: True
                id: password_input

        GridLayout:
            cols: 1
            row_default_height: "50dp"
            row_force_default: True
            spacing: "50dp"
            padding: "50dp"
            Button:
                size_hint_y: None
                height: "40dp"
                text: "Login"
                size_hint_x: None
                width: "675dp"
                on_press:
                    root.login()
                    root.manager.current= 'profile'

<SignUpForm>:
    username_box: username_input
    password_box: password_input
    confirm_box: confirm_input

    BoxLayout:
        orientation: "vertical"
        size_hint_y: None
        height: "500dp"
        padding: "10dp"

        Label:
            text: 'Books Recommender'
            font_size: 40

        GridLayout:
            cols: 2
            row_default_height: "50dp"
            row_force_default: True
            spacing: "10dp"
            padding: "10dp"

            Label:
                text: "Username"
                size_hint_x: None
                width: "200dp"

            TextInput:
                id: username_input
                size_hint_x: None
                width: "500dp"
            Label:
                text: "Password"
            TextInput:
                password: True
                id: password_input
            Label:
                text: "Confirm Password"

            TextInput:
                password: True
                id: confirm_input

        GridLayout:
            cols: 1
            row_default_height: "50dp"
            row_force_default: True
            spacing: "50dp"
            padding: "50dp"
            Button:
                size_hint_y: None
                height: "40dp"
                text: "Login"
                size_hint_x: None
                width: "675dp"
                on_press:
                    root.login()
                    root.manager.current= 'profile'

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
                            root.manager.current= 'SelectPopup'

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

# class SignInForm(Screen):
#     pass
#
# class SignUpForm(Screen):
#     pass

class RootScreen(ScreenManager):
    pass

class maininterface(App):
    def build(self):
        # sm = ScreenManager()
        # sm.add_widget(profile(name='categorymain'))
        # sm.add_widget(SignInForm(name='signin'))
        #
        # sm.add_widget(SignUpForm(name='signup'))
        # # sm.current= 'signin'
        #
        # return sm
        return RootScreen()


if __name__ == '__main__':
    maininterface().run()