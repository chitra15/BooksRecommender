import codecs
from math import sqrt

from pandas import DataFrame


class CF:
    #initialise class variables
    def __init__(self, reviews, max_num_recommendation=100, k=1, datasetLocation='/Users/Gopal/Downloads/'): #k = value for KNN
        self.reviews = reviews
        self.datasetLocation = datasetLocation
        self.max_num_recommendation = max_num_recommendation
        self.k = k
        self.fn = self.compute_pearson_score
        self.ISBN_title_conv = {}


    def ISBN_Title(self, isbn):
        if isbn in self.ISBN_title_conv:
            return self.ISBN_title_conv[isbn]
        else:
            return isbn

    #parse and convert dataset into a dictionary
    def openDataset(self):
        self.reviews = {}
        ctr = 0
        file = codecs.open(self.datasetLocation + "reduce_rating_w_0.csv", 'r', 'latin-1') #load book ratings into self.reviews
        for line in file:
            ctr += 1
            col = line.split(';')
            user_id = col[0]
            isbn = col[1]
            rating = int(col[2])
            if user_id in self.reviews:
                currentRatings = self.reviews[user_id]
            else:
                currentRatings = {}
            currentRatings[isbn] = rating
            self.reviews[user_id] = currentRatings
        file.close()

        file = codecs.open(self.datasetLocation + "books_cf.csv", 'r', 'latin-1')
        for line in file:
            ctr += 1
            col = line.split(';')
            isbn = col[0]
            bk_title = col[1]
            self.ISBN_title_conv[isbn] = bk_title
        file.close()

    #determine how similar 2 users' are
    def compute_pearson_score(self, u1, u2):
        sumofProd = 0
        sum_u1 = 0
        sum_u2 = 0
        sum_u1_squared = 0
        sum_u2_squared = 0
        no_similarBooks = 0
        for book in u1:
            if book in u2:
                no_similarBooks += 1
                rating_u1 = u1[book]
                rating_u2 = u2[book]
                sumofProd += rating_u1 * rating_u2
                sum_u1 += rating_u1
                sum_u2 += rating_u2
                sum_u1_squared += pow(rating_u1, 2)
                sum_u2_squared += pow(rating_u2, 2)
        if no_similarBooks == 0:
            return 0

        bottom = (sqrt(sum_u1_squared - pow(sum_u1, 2) / no_similarBooks) * sqrt(sum_u2_squared - pow(sum_u2, 2) / no_similarBooks))

        if bottom == 0:  #if denom 0 : return 0
            return 0
        else:
            top = (sumofProd - (sum_u1 * sum_u2) / no_similarBooks)
            score = top / bottom
            return score

    def calc_kNN(self, user_id):
        dist_to_user = []
        for row in self.reviews:
            if row != user_id:
                dist = self.fn(self.reviews[user_id], self.reviews[row])
                dist_to_user.append((row, dist))
        dist_to_user.sort(key=lambda artistTuple: artistTuple[1], reverse=True) #sort dist_to_user array'
        return dist_to_user


    #generate list of recommendations
    def getRecommendation(self, user_id):
        list_recommendations = {}
        close_users = self.calc_kNN(user_id)
        ratings = self.reviews[user_id]  #get list of rating for user-id
        sum_dist = 0.0
        for j in range(self.k): #cycle through the closest users and sum up all their ratings
            sum_dist += close_users[j][1]
        for j in range(self.k):
            weight = (close_users[j][1] / sum_dist)
            user = close_users[j][0]
            ratings_of_neighbor = self.reviews[user]
            for book in ratings_of_neighbor:
                if not book in ratings:
                    if book not in list_recommendations:
                        list_recommendations[book] = (ratings_of_neighbor[book] * weight)
                    else:
                        list_recommendations[book] = (list_recommendations[book] + ratings_of_neighbor[book] * weight)

        list_recommendations = list(list_recommendations.items())
        list_recommendations = [k for (k, v) in list_recommendations]

        list_recommendations.sort(key=lambda bookRow: bookRow[1], reverse=True)
        return DataFrame({'ISBN': list_recommendations[:self.max_num_recommendation]})