from numpy import *
from pandas import *
from sklearn.preprocessing import scale
from algorithms.recommendation.CF import CF
from sklearn.neighbors import KNeighborsClassifier

pandas.set_option('expand_frame_repr', False)
pandas.set_option('display.max_columns', 156)
pandas.set_option('display.max_rows', 800)
options.mode.chained_assignment = None


class CBF:
    def __init__(self, rating_set, book_set):
        self.rating_set = rating_set
        self.raw_data = self.rating_set
        self.book_set = book_set

    # create feature profiles dataframe of users (Uid, ISBN, Rating with book properties)
    def createFeatureProfile(self):
        self.rating_set = self.rating_set.merge(self.book_set, how="left", on=["ISBN"])

        # binary class labels for each ratings of the profile created
        # 1-5 ratings = 0
        # 6-10 ratings = 1
        nrat = self.rating_set["Rating"].apply(lambda x: 1 if x > 5 else 0)  # axis=0 --> apply on rows, axis=1 --> apply on cols
        nrat = DataFrame(nrat)
        nrat.columns = ["nrat"]

        # combine new categorical rating variable -nrat- with original rating dataframe
        self.rating_set = concat([self.rating_set.reset_index(drop=True), nrat], axis=1)
        return nrat


    def standardiseData(self):
        # remove rating variable as we have created a new variable nrat
        thecols = self.rating_set.columns.difference(["Rating"])
        scaled_ratings = self.rating_set[thecols]

        o_col = scaled_ratings.columns.difference(['ISBN', 'Userid', 'nrat'])
        scaled_ratings = scaled_ratings[o_col]

        scaled_ratings = DataFrame(scale(scaled_ratings, axis=1))

        temp_rate_cols = self.rating_set.iloc[:, [0, 1, 156]]
        scaled_ratings = concat([scaled_ratings.reset_index(drop=True), temp_rate_cols], axis=1)
        return scaled_ratings

    def splitDataIntoSets(self):
        # create a randomized index object of all the data
        random.seed(7)

        # divide into training and test sets with an 80:20 split
        scaled_ratings = self.standardiseData()
        rows = len(scaled_ratings.index)
        which_train = random.choice(a=[True, False], size=rows, replace=True, p=[0.8, 0.2])
        return which_train


    def modelClassifier(self):
        # build model using KNeighbors Classifier
        nrat = self.createFeatureProfile()
        y = factorize(nrat["nrat"])[0]

        scaled_ratings = self.standardiseData()
        which_train = self.splitDataIntoSets()
        model_data_train = scaled_ratings[which_train]
        model_data_test = scaled_ratings[~which_train]

        features = model_data_train.columns[:153]
        # x = model_data_train[features]
        test_n = scaled_ratings[features]
        nbrs = KNeighborsClassifier(n_neighbors=3)
        nbrs.fit(test_n, y)
        return nbrs

    def predictions(self):
        # check how model performs on test set
        return self.modelClassifier().predict(self.standardiseData()[self.standardiseData().columns[:153]])

    #generate dataframe which creates non-rated books by a user (11676) and set rating to 0
    def nonratedbookdataframe(self, userid):
        unique_books = self.book_set[["ISBN"]]
        totalISBNs = unique_books.drop_duplicates()
        temp = self.raw_data[self.raw_data.Userid == userid]
        ratedbooks = temp[["ISBN"]]
        non_ratedbooks = totalISBNs.loc[~totalISBNs.set_index(list(totalISBNs.columns)).index.isin(ratedbooks.set_index(list(ratedbooks.columns)).index)]

        test = repeat([userid], len(non_ratedbooks), axis=0)
        df = DataFrame(test, columns=["userid"])
        dataframe = concat([df, non_ratedbooks], axis=1)
        dataframe = dataframe.dropna()
        dataframe.userid = dataframe.userid.astype(int)
        dataframe["Rating"] = 0
        return dataframe

    def getRecommendation(self, userid):
        usernonratedbookdataframe = self.nonratedbookdataframe(userid)

        #build a profile for the user dataframe:
        activeuserratings = usernonratedbookdataframe.merge(self.book_set, how="left", on=["ISBN"])
        test = usernonratedbookdataframe.merge(self.book_set, how="left", on=["ISBN"])

        #generate predictions for book ratings for the current user profile
        drop_cols = activeuserratings.columns.difference(["userid", "ISBN", "Rating"])
        test = activeuserratings[drop_cols]
        predictions = self.modelClassifier().predict(test)

        #creating dataframe from the results
        books_isbn = activeuserratings[["ISBN"]]
        books_isbn["predictions"] = predictions
        recommend = books_isbn[books_isbn["predictions"] == 1]
        recommendationList = recommend[["ISBN"]]
        return recommendationList

