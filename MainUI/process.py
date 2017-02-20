import time
from pandas import *
import requests
import re

class Preprocess:
    def __init__(self, location):
        self.location = location
        # self.cols = cols

    def readDataset(self):
        cols = ["ISBN", "Book-Title", "Book-Author", "Year-Of-Publication", "Publisher", "Image-URL-S", "Image-URL-M", "Image-URL-L"]
        books = read_csv(self.location, names=cols, header=None, sep=';', encoding='latin-1', low_memory=False, skiprows=1)
        cols_reduced = books[["ISBN", "Book-Title"]]
        return cols_reduced

    def removesquarebrackets(self):
        cols = ["ID", "ISBN", "Book-Title", "Category"]
        books = read_csv(self.location, names=cols, header=None, sep=';', encoding='latin-1', low_memory=False, skiprows=2)
        return books[["ISBN","Book-Title", "Category"]]



# p = Preprocess("BX-Books.csv")
p = Preprocess("Rawcategory.csv")
# result = p.readDataset()
result = p.removesquarebrackets()
# print(result.head(10))


# def connectToGoogleBooks(text):
#     key = "AIzaSyD_bI7AO3JrLP4l3Pb86oDYHTwUxofNtBc"
#     parameter = {"q": text, 'key': key}
#     search_url = "https://www.googleapis.com/books/v1/volumes"
#     try:
#         search_url = requests.get(url=search_url, params=parameter)
#         data = search_url.json()
#         book_desc = data["items"][0]["volumeInfo"]['categories']
#         return book_desc
#     except Exception as e:
#         print(str(e))
#
# options.mode.chained_assignment = None
#
# for index, row in result.iterrows():
#     book = row['Book-Title']
#     desc = connectToGoogleBooks(book)
#     # time.sleep(10)
#     result.loc[index, 'Description'] = desc
#     result.to_csv("books_desc.csv", sep=";")
#
# print(result)

for index, row in result.iterrows():

    # output= re.sub(r'\[\'(?:[^\]|]*\|)?([^\]|]*)\'\]', r'\1', result.loc[index, 'Category'])
    line = result.loc[index, 'Category']
    output = re.sub(r'\[\'(?:[^\]|]*\|)?([^\]|]*)\'\]', r'\1', str(line))
    result.loc[index, 'Category'] = ""
    result.loc[index, 'Category'] = output
    # print(result.loc[index, 'Category'])
    result.to_csv("category.csv", sep=";")

# line = "0;1559581565;Super Mario World Game Secrets (Secrets of the Games Series);['Games']"
# output= re.sub(r'\[\'(?:[^\]|]*\|)?([^\]|]*)\'\]', r'\1', line)
# print(output)