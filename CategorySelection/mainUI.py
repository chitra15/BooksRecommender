import json
import requests
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from kivy.uix.listview import ListItemButton
from kivy.utils import get_color_from_hex
from kivy.lang import Builder

Builder.load_string('''
#: import mainUI mainUI
#: import ListItemButton kivy.uix.listview.ListItemButton
#: import ListAdapter kivy.adapters.listadapter.ListAdapter

<AddBookForm>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
    orientation: "vertical"
    search_input: search_box
    search_results: search_results_list
    spacing: 5
    ActionBar:
        background_color: 0, 0, 0, 0.5
        pos_hint: {'top': 1}
        spacing: 10
        ActionView:
            use_separator: True
            ActionPrevious:
                title: "Search Books"
                app_icon: "icons/close.png"
                with_previous: False
                on_release: root.exit_app()
            ActionOverflow:
            ActionButton:
                text: 'Home'
                icon: "icons/home.png"
            ActionButton:
                text: 'Profile'
                icon: "icons/profile.png"

    BoxLayout:
        spacing: 0
        orientation: "horizontal"
        size_hint_y: None
        height: "40dp"
        Button:
            text: ""
            size_hint_x: None
            width: "60dp"
            height: "40dp"
            on_press: root.search_book()
            background_color: [1, 1, 1, 0.1]
            Image:
                source: "icons/search.png"
                size_hint_x: None
                width: "40dp"
                height: "40dp"
                y: self.parent.y + self.parent.height - 40
                x: self.parent.x + 10
                allow_stretch: True

        TextInput:
            id: search_box
            size_hint_y: None
            size: (100, "40dp")
            cursor_color: [0, 0, 0, 1]
            font_size: "18sp"
            multiline: False
            on_text_validate: root.search_book()
            handle_image_left: "icons/search.png"
            hint_text: "Search books..."
            input_type: "text"
            keyboard_suggestions: True

    BoxLayout:
        orientation: "vertical"
        size_hint_y: None
        Label:
            text: '[color=003300]Search Results[/color]'
            markup: True
            underline: True #not working -- need dev version of kivy
            font_size: "20sp"
            bold: True
            valign: "top"  #not working



    BoxLayout:
        padding: 0, 15, 0, 0
        orientation: "vertical"
        ListView:
            id: search_results_list
            selected_color: [0, 0, 0, 1]
            adapter:
                ListAdapter(data=[], cls=main.BookButton, args_converter=root.args_converter)



<BookButton>:
    markup: True
    size: (150, "100dp")
    deselected_color: [0.7, 0.9, 1, 0.3]
    border: [10, 10, 10, 10]
    margin: 20
    color: [0, 0, 0, 1]
    text_size: (290, 40)  #proper text alignment
    on_press: app.root.show_book(self.book)

<CurrentBook>:  #selected book info from list  #fuck
    orientation: "vertical"
    ActionBar:
        background_color: 0, 0, 0, 0.5
        pos_hint: {'top': 1}
        spacing: 10
        ActionView:
            use_separator: True
            ActionPrevious:
                title: "{}".format(root.book[0])
                halign: "center"
                app_icon: "icons/back.png"
                with_previous: False
                on_release: app.root.show_book_form()
    BoxLayout:
        orientation: "horizontal"
        padding: 15, 0, 0, 0
        spacing: 60
        AsyncImage:
            source: "{}".format(root.book[3])
            size_hint_x: None
            width: "150dp"
            height: "200dp"
            y: self.parent.y
            x: self.parent.x
            allow_stretch: False
        Label:
            text: root.labeltext1
            markup: True
            color: [0, 0, 0, 1]
            size_hint_x: None

    BoxLayout:
        orientation: "vertical"
        padding: 20, 0, 20, 0
        spacing: 0
        Label:
            text: "[b]Rate this book: [/b]"
            markup: True
            color: [0, 0, 0, 1]
            size_hint: None, None
            halign: "left"
        BoxLayout:
            orientation: "horizontal"
            spacing: 0
            padding: 20, -150, 0, 0
            Image:
                id: star_1
                source: "{}".format(app.root.rate_1)
                size_hint_x: None
                width: "50dp"
                height: "40dp"
                y: self.parent.y + self.parent.height - 180
                x: self.parent.x + 200
                allow_stretch: False
                on_touch_down: if self.collide_point(*args[1].pos): app.root.getRating(1)
            Image:
                id: star_2
                source: "{}".format(app.root.rate_2)
                size_hint_x: None
                width: "50dp"
                height: "40dp"
                y: self.parent.y + self.parent.height - 180
                x: self.parent.x + 200
                allow_stretch: False
                on_touch_down: if self.collide_point(*args[1].pos): app.root.getRating(2)
            Image:
                id: star_3
                source: "{}".format(app.root.rate_3)
                size_hint_x: None
                width: "50dp"
                height: "40dp"
                y: self.parent.y + self.parent.height - 180
                x: self.parent.x + 200
                allow_stretch: False
                on_touch_down:
                on_touch_down: if self.collide_point(*args[1].pos): app.root.getRating(3)
            Image:
                id: star_4
                source: "{}".format(app.root.rate_4)
                size_hint_x: None
                width: "50dp"
                height: "40dp"
                y: self.parent.y + self.parent.height - 180
                x: self.parent.x + 200
                allow_stretch: False
                on_touch_down: if self.collide_point(*args[1].pos): app.root.getRating(4)
            Image:
                id: star_5
                source: "{}".format(app.root.rate_5)
                size_hint_x: None
                width: "50dp"
                height: "40dp"
                y: self.parent.y + self.parent.height - 180
                x: self.parent.x + 200
                allow_stretch: False
                on_touch_down: if self.collide_point(*args[1].pos): app.root.getRating(5)

    BoxLayout:
        orientation: "vertical"
        padding: 20, -70, 20, 0
        spacing: 0
        ScrollView:
            Label:
                size_hint_y: None
                text_size: self.width, None
                height: self.texture_size[1]
                text: root.labeltext2
                markup: True
                color: [0, 0, 0, 1]
''')

# BEGIN AddBookForm

class AddBookForm(BoxLayout):
    googleapikey = "AIzaSyB9llME8kQSbPQFSFr1VZXbtOZ5aLfN0KU"  # Google Books API key
    search_input = ObjectProperty()  # specifies default value of the property

    def exit_app(self):
        App.get_running_app().stop()

    # BEGIN search_book
    def search_book(self):
        self.search_results.item_strings = ""
        if self.search_input.text == "":
            popup = Popup(title="Information",
                          content=Label(text="No book name specified"),
                          size_hint=(None, None), size=(400, 200))
            popup.open()
            return

        parameter = {"q": self.search_input.text, 'key': self.googleapikey, 'orderBy': "relevance", "maxResults": 5}
        search_url = "https://www.googleapis.com/books/v1/volumes"
        try:
            search_url = requests.get(url=search_url, params=parameter)
            data = search_url.json()

            books = [(d["volumeInfo"]["title"], d["volumeInfo"]["authors"], d["volumeInfo"]['description'],
                      d["volumeInfo"]["imageLinks"]["thumbnail"], d["volumeInfo"]["publisher"],
                      d["volumeInfo"]["publishedDate"])
                     for d in data["items"]]
            # print("\n".join(books))

            self.search_results.item_strings = books
            self.search_results.adapter.data.clear()
            self.search_results.adapter.data.extend(books)
            self.search_results._trigger_reset_populate()
        except Exception as e:
            print(e)
            popup = Popup(title="Not found!",
                          content=Label(text="'{}' not found. Try again.".format(self.search_input.text)),
                          size_hint=(None, None), size=(400, 200))

            popup.open()
            return

    # END search_book

    def args_converter(self, index, data_item):  # herefuck
        title, authors, desc, thumbnail, publisher, publishedDate = data_item
        return {'book': (title, authors, desc, thumbnail, publisher, publishedDate)}


# END AddBookForm

class CurrentBook(BoxLayout):
    labeltext1=StringProperty()
    labeltext2= StringProperty()

    current_book = ObjectProperty()  # specifies default value of the property
    # rating = NumericProperty()
    rate_1 = StringProperty("icons/star_empty.png")
    rate_2 = StringProperty("icons/star_empty.png")
    rate_3 = StringProperty("icons/star_empty.png")
    rate_4 = StringProperty("icons/star_empty.png")
    rate_5 = StringProperty("icons/star_empty.png")

    def __init__(self, **kwargs):
        super(CurrentBook, self).__init__(**kwargs)
        self.labeltext1="[b]Author(s):[/b] [i]{}[/i]\n[b]Publisher: [/b][i]{}[i]\n[b]Published Date: [/b][i]{}[/i]".format(self.book[1][0], self.book[4].strip('".'), self.book[5])
        self.labeltext2= "[b]Description:[/b]\n[i]{}[/i]".format(self.book[2])


    googleapikey = "AIzaSyCZ_cKrDww83eJ8W7tFHUiNKMelzothD3k"  # Google Books API key
    book = ListProperty(["Harry Potter", "J.K Rowling"])
    thumbnail = StringProperty()
    publisher = StringProperty()
    date = StringProperty()
    description = StringProperty()

    def update_book(self):
        query = self.book[0]
        # print("{} saem sa".format(query))
        parameters = {"q": query, 'key': self.googleapikey}
        print(parameters)
        search_template = "https://www.googleapis.com/books/v1/volumes"
        search_url = requests.get(url=search_template, params=parameters)
        # print(search_url.url)
        data = search_url.json()

    def book_retrieved(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.thumbnail = data["volumeInfo"]["imageLinks"]["thumbnail"]
        self.publisher = data["volumeInfo"]["publisher"]
        self.date = data["volumeInfo"]["publishedDate"]
        self.description = data["volumeInfo"]["description"]

    def getRating(self, rating):
        if rating == 1:
            if self.rate_1 == "icons/star_empty.png":
                self.rate_1 = "icons/star_filled.png"
            else:
                self.rate_1 = "icons/star_empty.png"
        elif rating == 2:
            if self.rate_2 == "icons/star_empty.png":
                self.rate_1 = "icons/star_filled.png"
                self.rate_2 = "icons/star_filled.png"
            else:
                self.rate_1 = "icons/star_empty.png"
                self.rate_2 = "icons/star_empty.png"
        elif rating == 3:
            if self.rate_3 == "icons/star_empty.png":
                self.rate_1 = "icons/star_filled.png"
                self.rate_2 = "icons/star_filled.png"
                self.rate_3 = "icons/star_filled.png"
            else:
                self.rate_1 = "icons/star_empty.png"
                self.rate_2 = "icons/star_empty.png"
                self.rate_3 = "icons/star_empty.png"
        elif rating == 4:
            if self.rate_4 == "icons/star_empty.png":
                self.rate_1 = "icons/star_filled.png"
                self.rate_2 = "icons/star_filled.png"
                self.rate_3 = "icons/star_filled.png"
                self.rate_4 = "icons/star_filled.png"
            else:
                self.rate_1 = "icons/star_empty.png"
                self.rate_2 = "icons/star_empty.png"
                self.rate_3 = "icons/star_empty.png"
                self.rate_4 = "icons/star_empty.png"
        elif rating == 5:
            if self.rate_5 == "icons/star_empty.png":
                self.rate_1 = "icons/star_filled.png"
                self.rate_2 = "icons/star_filled.png"
                self.rate_3 = "icons/star_filled.png"
                self.rate_4 = "icons/star_filled.png"
                self.rate_5 = "icons/star_filled.png"
            else:
                self.rate_1 = "icons/star_empty.png"
                self.rate_2 = "icons/star_empty.png"
                self.rate_3 = "icons/star_empty.png"
                self.rate_4 = "icons/star_empty.png"
                self.rate_5 = "icons/star_empty.png"

    def show_book(self, book=None):
        self.clear_widgets()
        if book is None and self.current_book is None:
            book = ("Nothing found", "None")
            self.current_book = CurrentBook()
        if book is not None:
            # self.current_book = Factory.CurrentBook()
            self.current_book = CurrentBook(book=book)
            # self.current_book.title = book
        self.current_book.update_book()
        self.add_widget(self.current_book)
        # self.manager.current = 'signin'

    def show_book_form(self):
        self.clear_widgets()
        self.add_widget(AddBookForm())


# BEGIN BookButton
class BookButton(ListItemButton):
    book = ListProperty()


# END BookButton

# BEGIN BooksRecommendationApp
class BooksRecommendationApp(App):


    def build(self):
        # sm = ScreenManager()
        # sm.add_widget(AddBookForm(name='booksrecommendation'))
        # sm.add_widget(SignInForm(name='signin'))
        self.title = "Books Recommendation System"
        self.icon = "icons/books.png"
        # BookButton.text= "[b]{}[/b]\nBy {}".format(self.BookButton.book[0], self.BookButton.book[1][0])
        return AddBookForm

    def on_start(self):
        Window.size = (1000, 700)


# END BooksRecommendationApp


# BEGIN MAIN
if __name__ == '__main__':
    # Window.clearcolor = get_color_from_hex('#101216')
    BooksRecommendationApp().run()