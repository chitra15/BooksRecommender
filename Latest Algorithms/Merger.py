from pandas import read_csv

class Merger:
    def __init__(self, cfFrame, cbfFrame):
        # self.userid = userid
        self.cfFrame = cfFrame
        self.cbfFrame = cbfFrame

    def mergeAlgorithm(self):
        len_cbf = len(self.cbfFrame)
        len_cf = len(self.cfFrame)

        cols_reduced_books = ["ISBN", "Title", "Category"]
        reduced_books = read_csv("/Users/Gopal/Downloads/Dataset/reduced_books_category.csv", sep=";", header=None,
                                 skiprows=1, low_memory=False,
                                 names=cols_reduced_books, encoding="latin-1")
        twitter_cols = ["twitter", "ISBN", "Category"]
        tweets = read_csv("/Users/Gopal/Downloads/Dataset/unstructured_tweets_categorized.csv", sep=";", header=None,
                          skiprows=1, low_memory=False,
                          names=twitter_cols, encoding="latin-1")

        if len_cbf > len_cf:
            recommendation = self.cbfFrame[
                self.cbfFrame.ISBN.isin(self.cfFrame.ISBN.values)]  # intial recommendation generated when combining CF and CBF
            recommend_unless = self.cbfFrame[self.cbfFrame.ISBN.isin(self.cfFrame.ISBN.values)]  # intial recommendation generated
            # print(len(recommendation))
            reduced_books = reduced_books[["ISBN", "Category"]]  # reduced_books_category w/ ISBN and category

            recommendation = recommendation[recommendation.ISBN.isin(reduced_books.ISBN.values)]
            recommendation = recommendation.merge(reduced_books, how="left", on=["ISBN"])
            recommendation = recommendation[recommendation.Category.isin(tweets.Category.values)]
            if recommendation.empty:
                if recommend_unless.empty:
                    # print("Please Rate some books, first!")
                    return "Please Rate some books, first!"
                else:
                    # print(recommend_unless)
                    # recommend_unless.to_csv("/Users/Gopal/Downloads/Dataset/recommendation_{}.csv".format(str(self.userid)),
                    #                         sep=";", index=False)
                    return recommend_unless

            else:
                # print(len(recommendation))
                # recommendation.to_csv("/Users/Gopal/Downloads/Dataset/recommendation_{}.csv".format(str(self.userid)), sep=";",
                #                       index=False)
                return recommendation
        else:
            recommendation = self.cfFrame[self.cfFrame.ISBN.isin(self.cbfFrame.ISBN.values)]
            recommend_unless = self.cfFrame[self.cfFrame.ISBN.isin(self.cbfFrame.ISBN.values)]
            print(len(recommendation))
            reduced_books = reduced_books[["ISBN", "Category"]]
            recommendation = recommendation[recommendation.ISBN.isin(reduced_books.ISBN.values)]
            recommendation = recommendation.merge(reduced_books, how="left", on=["ISBN"])
            recommendation = recommendation[recommendation.Category.isin(tweets.Category.values)]
            if recommendation.empty:
                if recommend_unless.empty:
                    # print("Please Rate some books, first!")
                    return "Please Rate some books, first!"
                else:
                    # recommend_unless.to_csv("/Users/Gopal/Downloads/Dataset/recommendation.csv",
                    #                         sep=";", index=False)
                    return recommend_unless
            else:
                # recommendation.to_csv("/Users/Gopal/Downloads/Dataset/recommendation.csv", sep=";",
                #                       index=False)
                return recommendation













