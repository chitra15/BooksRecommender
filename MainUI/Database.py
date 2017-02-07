import sqlite3

class Database:

    def getUsername(self, username):
        conn = sqlite3.connect('booksrecommender.db')
        cursor = conn.cursor()
        for row in username:
            cursor.execute("SELECT UserID FROM Authentication WHERE UserName = ?", (username,))
            return cursor.fetchall()

    def getPassword(self, password):
        conn = sqlite3.connect('booksrecommender.db')
        cursor = conn.cursor()
        for row in password:
            cursor.execute("SELECT UserID FROM Authentication WHERE Password = ?", (password,))
            return cursor.fetchall()

    def addUser(self, username, password):
        conn = sqlite3.connect('booksrecommender.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Authentication VALUES (NULL, ?, ? )", (username, password));
        conn.commit()