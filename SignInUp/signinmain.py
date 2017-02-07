from kivy.app import App
from kivy.properties import ObjectProperty  # at top of file
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from SignInUp.categorymain import profile
from MainUI.UserLogin import Login

class SignInForm(Screen):
    username_box = ObjectProperty()
    password_box = ObjectProperty()

    def login(self):
        password = self.password_box.text
        username = self.username_box.text
        Login.loggedin(self, password, username)




    # def returncred(self):
    #     username = 'dweferg'#self.username_box.text
    #     print(username)
    #     return username


class SignIn(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SignInForm(name='signin'))
        sm.add_widget(profile(name='categorymain'))
        return sm


if __name__ == '__main__':
    SignIn().run()



