from pandas import DataFrame, read_csv

from Testing.CBF import CBF
from Testing.CF import CF
from Testing.Merger import Merger

if __name__ == '__main__':
    #cf
    cf = CF({})
    cf.openDataset()
    cf_frame = cf.getRecommendation('11676')
    # print(cf_frame)


    #cbf
    cols_ratings = ["Userid", "ISBN", "Rating"]
    ratings = read_csv("/Users/Gopal/Downloads/Dataset/reduced_rating.csv", sep=";", header=None, skiprows=1, low_memory=False,
                       names=cols_ratings, encoding="latin-1")

    cols_books = ['ISBN', 'Games', 'Poetry', 'African Americans', 'Fiction', 'Juvenile Fiction', 'True Crime',
                  'Shipbuilding', 'History', 'Humor', 'Technology & Engineering',
                  'Social Science', 'Solar energy', 'Motorcycle gangs', 'Political Science', 'Biography & Autobiography',
                  'Psychology', 'Rock musicians', 'Family & Relationships',
                  'Body, Mind & Spirit', 'Health & Fitness', 'Angels', 'Self-confidence', 'Postage stamps', 'Science',
                  'Horses in art', 'Photography', 'Unknown', 'Suspense fiction', 'Art',
                  'House & Home', 'Naval ceremonies, honors, and salutes', 'Gay male couples', 'Television', 'Religion',
                  'Business & Economics', 'Atlantic Provinces', 'African American singers',
                  'World War, 1939-1945', 'Dreams', 'American literature', 'First loves', 'Irish', 'Time travel',
                  'Education', 'Language Arts & Disciplines', 'Cities and towns', 'Music', 'Philosophy',
                  'Cults', 'Nature', 'Political fiction', 'Happiness', 'Gardening', 'Self-Help', 'Friendship',
                  'Cookery (Natural foods)', 'Single fathers', 'Comics & Graphic Novels', 'Drama',
                  'Factories', 'Psychological fiction', 'Literary Criticism', "Alzheimer's disease",
                  'Detective and mystery stories', 'Families', 'Juvenile Nonfiction', 'Dublin (Ireland)', 'Gamblers',
                  'Short stories', 'Mathematics', 'Automobile racing', 'Architecture', 'Country life', 'France',
                  'Barbadians', 'Travel', 'Australian fiction', 'Sports & Recreation', 'Artists',
                  'Computers', 'Competition horses', 'Cooking', "Children's parties", 'Indic fiction (English)',
                  'Foreign Language Study', 'Crustacea', 'Actors and actresses', 'Canada', 'Christmas poetry', 'Chile',
                  'Crafts & Hobbies', 'An adventure in the Netherlands', 'Babysitters', 'Floods',
                  'Nursery rhymes, American', 'Composition (Music)', 'Fear', 'Adventure and adventurers',
                  "Children's stories", 'Amusements',
                  'Dating (Social customs)', 'Humorous stories', 'Coronary heart disease', 'Young Adult Fiction',
                  'Design', 'Discworld (Imaginary place)', 'Chemistry', 'Computer technicians', 'Study Aids',
                  'General Conference of Seventh-day Advenists, Session', 'Cookbooks', 'Contests',
                  'Rogers, Buck (Fictitious character)', 'Horror tales', 'Flags', 'Law', 'Hockey players',
                  "Children's plays, American", 'Cantatas, Secular', 'Success', 'Fantasy fiction, American',
                  'Performing Arts', 'Cats', 'BIOGRAPHY & AUTOBIOGRAPHY', 'Science fiction, American', 'Medical',
                  'Authors', 'Authors, American', 'Africa, Eastern', 'Butler, Harold Edgeworth, 1878-', 'Elves',
                  'Comic books', 'Historical fiction', 'Animals', 'Reference', 'Fantasy fiction, English',
                  'Betrayal', 'English drama', 'Pets', 'Love stories', 'Actors', 'Conduct of life', 'Fathers and sons',
                  'Comic books, strips, etc', 'India', 'Folklore', 'Gothic novels', 'Refugees',
                  'Horror tales, American', 'Murder', 'Owls', "Children's stories, English",
                  'American wit and humor, Pictorial']
    books = read_csv("/Users/Gopal/Downloads/Dataset/books_cbf_ready.csv", sep=";", header=None, skiprows=1, low_memory=False,
                     names=cols_books, encoding="latin-1")
    cbf = CBF(ratings, books)
    cbf_frame = cbf.getRecommendation(11676)

    merger = Merger(cf_frame, cbf_frame)
    print(merger.mergeAlgorithm())