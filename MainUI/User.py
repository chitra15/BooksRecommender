class User:

    def __init__(self, userID, name, gender, preference):
        self.userID= userID
        self.name=name
        self.gender= gender
        self.preferences= preference

#     def display(self):
#         print(self.userID)
#         print(self.name)
#         print(self.gender)
#         print(self.preferences)
#
#
# usr= User(1, 'Hello', 'fem', 'preferences,cefer,cref')
# # usr.display()
# attr=getattr(usr,'name')
# print(attr)