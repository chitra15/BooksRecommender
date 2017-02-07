from MainUI.Database import Database
from kivy.uix.label import Label
from kivy.uix.popup import Popup

class Login:

    def __init__(self, userID, username, password):
        self.userID= userID
        self.username= username
        self.password= password

    def loggedin(self, password, username):
        data = Database.getUsername(self, username)
        if len(data) == 0:
            print("No username available you need to sign up!")
            popup = Popup(title="Information", content=Label(text="No username available you need to sign up!"), size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        else:
            data = Database.getPassword(self, password)
            if len(data) == 0:
                print("Wrong password. Try again!")
                popup = Popup(title="Information", content=Label(text="Wrong password. Try again!"), size_hint=(None, None), size=(400, 200))
                popup.open()
                return
            else:
                print("Welcome")
                popup = Popup(title="Information", content=Label(text="Welcome"), size_hint=(None, None), size=(400, 200), auto_dismiss=True)
                popup.open()
                self.manager.current = 'categorymain'

    def register(self, password, username):
        Database.addUser(self, username, password)
        popup = Popup(title="Information", content=Label(text="Welcome"), size_hint=(None, None), size=(400, 200))
        popup.open()
        self.manager.current = 'categorymain'

    def logout(self):
        self.manager.current= 'signin'

