from numpy import *
from pandas import *
from sklearn.preprocessing import scale
from algorithm.recommendation.CF import CF
from sklearn.neighbors import KNeighborsClassifier

pandas.set_option('expand_frame_repr', False)
pandas.set_option('display.max_columns', 156)
pandas.set_option('display.max_rows', 800)
options.mode.chained_assignment = None

cols_ratings = ["Userid", "ISBN", "Rating"]
ratings = read_csv("/Users/DELL/OneDrive/Implementation/BooksRecommender/dataset/reduced_rating.csv", sep=";", header=None, skiprows=1, low_memory=False,
                   names=cols_ratings, encoding="latin-1")

raw_data = ratings

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
books = read_csv("/Users/DELL/OneDrive/Implementation/BooksRecommender/dataset/books_cbf_ready.csv", sep=";", header=None, skiprows=1, low_memory=False,
                 names=cols_books, encoding="latin-1")

# create feature profiles of users
# extend rating dataframe containing Userid, ISBN, Rating with book attributes
ratings = ratings.merge(books, how="left", on=["ISBN"])

# binary class labels for each ratings of the profile created
# 1-5 ratings = 0
# 6-10 ratings = 1
nrat = ratings["Rating"].apply(lambda x: 1 if x > 5 else 0)  # axis=0 --> apply on rows, axis=1 --> apply on cols
nrat = DataFrame(nrat)
nrat.columns = ["nrat"]

# combine new categorical rating variable -nrat- with original rating dataframe
ratings = concat([ratings.reset_index(drop=True), nrat], axis=1)

# remove rating variable as we have created a new variable nrat
thecols = ratings.columns.difference(["Rating"])
scaled_ratings = ratings[thecols]

# standardize data
o_col = scaled_ratings.columns.difference(['ISBN', 'Userid', 'nrat'])
scaled_ratings = scaled_ratings[o_col]

scaled_ratings = DataFrame(scale(scaled_ratings, axis=1))

temp_rate_cols = ratings.iloc[:, [0, 1, 156]]
scaled_ratings = concat([scaled_ratings.reset_index(drop=True), temp_rate_cols], axis=1)

# create a randomized index object of all the data
random.seed(7)

# divide into training and test sets with an 80:20 split
rows = len(scaled_ratings.index)
which_train = random.choice(a=[True, False], size=rows, replace=True, p=[0.8, 0.2])
# model_data_train = scaled_ratings
model_data_train = scaled_ratings[which_train]
# model_data_train = model_data_train.reset_index(drop=True)
model_data_test = scaled_ratings[~which_train]
# model_data_test = model_data_test.reset_index(drop=True)

# build model using KNeighbors Classifier

y = factorize(nrat["nrat"])[0]
# y = factorize(model_data_train["nrat"])[0]

features = model_data_train.columns[:153]
# x = model_data_train[features]
test_n = scaled_ratings[features]
nbrs = KNeighborsClassifier(n_neighbors=3)
nbrs.fit(test_n, y)
# nbrs.fit(x, y)

# see how model performs on test set
predictions = nbrs.predict(scaled_ratings[scaled_ratings.columns[:153]])


# generate recommendation to a userid(11676)
unique_books = books[["ISBN"]]

totalISBNs = unique_books.drop_duplicates()


#generate dataframe which creates non-rated books by a user (11676) and set rating to 0
def nonratedbookdataframe(userid):
    temp = raw_data[raw_data.Userid == userid]
    ratedbooks = temp[["ISBN"]]

    non_ratedbooks = totalISBNs.loc[~totalISBNs.set_index(list(totalISBNs.columns)).index.isin(ratedbooks.set_index(list(ratedbooks.columns)).index)]


    test = repeat([userid], len(non_ratedbooks), axis=0)
    df = DataFrame(test, columns=["userid"])
    dataframe = concat([df, non_ratedbooks], axis=1)
    dataframe = dataframe.dropna()
    dataframe.userid = dataframe.userid.astype(int)
    dataframe["Rating"] = 0
    return dataframe

#get non-rated books for userid 11676
uid=11676
usernonratedbookdataframe = nonratedbookdataframe(uid)

#build a profile for the user dataframe:
activeuserratings = usernonratedbookdataframe.merge(books, how="left", on=["ISBN"])
test = usernonratedbookdataframe.merge(books, how="left", on=["ISBN"])
# print(activeuserratings.head())
# ratings = ratings.merge(books, how="left", on=["ISBN"])

#Predict ratings, sort and generate recommendations:
#generate predictions for book ratings for the current user profile
drop_cols = activeuserratings.columns.difference(["userid", "ISBN", "Rating"])
test = activeuserratings[drop_cols]
predictions = nbrs.predict(test)

#creating dataframe from the results
books_isbn = activeuserratings[["ISBN"]]
books_isbn["predictions"] = predictions
# print(books_isbn.head())
recommend = books_isbn[books_isbn["predictions"] == 1]
reduce = recommend[["ISBN"]]    #CBF recommendation

accuracy = where(predictions==test["Games"], 1, 0).sum() / float(len(test))  #review
# print("Accuracy: {}%".format(int(accuracy*100)))

# ---cf
reviews = {
    'Aisha': {'Harry Potter': 2.5, 'Charmed': 3.5, 'Twilight': 3.0, 'Spartan': 3.5, 'Data Mining': 2.5, 'Database Design': 3.0},
    'Gopal': {'Harry Potter': 3.0, 'Charmed': 3.5, 'Spartan': 5.0, 'Database Design': 3.0, 'Data Mining': 3.5},
    'Nilesh': {'Harry Potter': 2.5, 'Charmed': 3.0, 'Spartan': 3.5, 'Database Design': 4.0},
    'Taahir': {'Charmed': 3.5, 'Twilight': 3.0, 'Database Design': 4.5, 'Spartan': 4.0, 'Data Mining': 2.5},
    'Shweta': {'Harry Potter': 3.0, 'Charmed': 4.0, 'Twilight': 2.0, 'Spartan': 3.0, 'Database Design': 3.0, 'Data Mining': 2.0},
    'Kevish': {'Harry Potter': 3.0, 'Charmed': 4.0, 'Database Design': 3.0, 'Spartan': 5.0, 'Data Mining': 3.5},
    'Anubhav': {'Charmed': 4.5, 'Spartan': 4.0}
}

bx_recommender = CF(reviews)
bx_recommender.openDataset('/Users/DELL/OneDrive/Implementation/BooksRecommender/dataset/')
test = bx_recommender.getRecommendation(str(uid)) #return CF recommendation

cf_df = DataFrame({'ISBN': test})

len_cbf = len(reduce)
len_cf = len(cf_df)

cols_reduced_books = ["ISBN", "Title", "Category"]
reduced_books = read_csv("/Users/DELL/OneDrive/Implementation/BooksRecommender/dataset/reduced_books_category.csv", sep=";", header=None, skiprows=1, low_memory=False,
                   names=cols_reduced_books, encoding="latin-1")
twitter_cols = ["twitter", "ISBN", "Category"]
tweets = read_csv("/Users/DELL/OneDrive/Implementation/BooksRecommender/dataset/unstructured_tweets_categorized.csv", sep=";", header=None, skiprows=1, low_memory=False,
                   names=twitter_cols, encoding="latin-1")


if len_cbf > len_cf:
    recommendation = reduce[reduce.ISBN.isin(cf_df.ISBN.values)]   #intial recommendation generated when combining CF and CBF
    recommend_unless = reduce[reduce.ISBN.isin(cf_df.ISBN.values)]   #intial recommendation generated
    print(recommendation)
    reduced_books = reduced_books[["ISBN", "Category"]] #reduced_books_category w/ ISBN and category

    recommendation = recommendation[recommendation.ISBN.isin(reduced_books.ISBN.values)]
    recommendation = recommendation.merge(reduced_books, how="left", on=["ISBN"])
    recommendation = recommendation[recommendation.Category.isin(tweets.Category.values)]
    if recommendation.empty:
        if recommend_unless.empty:
            print("Please Rate some books, first!")
        else:
            print(recommend_unless)
            recommend_unless.to_csv("/Users/DELL/OneDrive/Implementation/BooksRecommender/dataset/recommendation_{}.csv".format(str(uid)), sep=";", index=False)

    else:
        print(recommendation.head())
        recommendation.to_csv("/Users/DELL/OneDrive/Implementation/BooksRecommender/dataset/recommendation_{}.csv".format(str(uid)), sep=";", index=False)
else:
    recommendation = cf_df[cf_df.ISBN.isin(reduce.ISBN.values)]
    recommend_unless = cf_df[cf_df.ISBN.isin(reduce.ISBN.values)]
    print(recommendation)
    reduced_books = reduced_books[["ISBN", "Category"]]
    recommendation = recommendation[recommendation.ISBN.isin(reduced_books.ISBN.values)]
    recommendation = recommendation.merge(reduced_books, how="left", on=["ISBN"])
    recommendation = recommendation[recommendation.Category.isin(tweets.Category.values)]
    if recommendation.empty:
        if recommend_unless.empty:
            print("Please Rate some books, first!")
        else:
            print(recommend_unless)
            recommend_unless.to_csv("/Users/DELL/OneDrive/Implementation/BooksRecommender/dataset/recommendation_{}.csv".format(str(uid)), sep=";", index=False)
    else:
        print(recommendation.head())
        recommendation.to_csv("/Users/DELL/OneDrive/Implementation/BooksRecommender/dataset/recommendation_{}.csv".format(str(uid)), sep=";", index=False)
