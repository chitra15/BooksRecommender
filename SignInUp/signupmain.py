from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from SignInUp.categorymain import profile
from kivy.uix.screenmanager import ScreenManager, Screen
from MainUI.UserLogin import Login

class SignUpForm(Screen):
    username_box = ObjectProperty()
    password_box = ObjectProperty()
    confirm_box = ObjectProperty()

    def login(self):
        password = self.password_box.text
        username = self.username_box.text
        confirm = self.confirm_box.text
        if password == confirm:
            Login.register(self, password, username)
            return

        else:
            print("Error in password")
            popup = Popup(title="Information", content=Label(text="Error in password"), size_hint=(None, None), size=(400, 200))
            popup.open()
            return
            conn.close()



class SignUp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SignUpForm(name='signup'))
        sm.add_widget(profile(name='categorymain'))
        return sm

if __name__ == '__main__':
    SignUp().run()
