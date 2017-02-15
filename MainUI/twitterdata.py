from tweepy import OAuthHandler
import tweepy
from MainUI.Database import Database
from nltk.tokenize import RegexpTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import sqlite3


class Tweets:
    # -------------------add result in database------------------
    def fetch(self):
        access_token = '4204466597-rHw64J65sdQdrkThqYoxIU4pEOgTU2kl9pCJsXb'
        access_token_secret = 'TwwMFZCqvCoYOGOm3LQbLnmJ4qBQMbGgplXcExB9o6ElB'
        consumer_key = 'SBsZKzoy7YgfeuVonSg4zq5XU'
        consumer_secret = 'kLxNsuuRh4RPxn5sM9blj3k6dGbq5krck0XjMDjkc3fduIWti2'

        auth= OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api= tweepy.API(auth)
        results= api.search(q="@worldbooksPage", count= 100)

        for result in results:
            user= result.user.screen_name
            status= result.text
            updatedstatus= status.replace('@worldbooksPage','')

            for row in updatedstatus:
                Database.fetchalltweets(self, user, updatedstatus)

#-------------------tokenize------------------------------

    def gettokens(self):
        tweets= Database.getTweets(self)

        tokenizer= RegexpTokenizer(r'\w+')
        stoplist = {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during',
                    'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours',
                    'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from',
                    'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his',
                    'through',
                    'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their',
                    'while',
                    'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before',
                    'them', 'same',
                    'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what',
                    'over', 'why',
                    'so', 'can', 'did', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only',
                    'myself',
                    'which', 'those', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by',
                    'doing', 'it',
                    'how', 'further', 'was', 'here', 'than', 'i\'ve'}

        for tweet in tweets:
            text=tweet[2].lower()
            tokens= tokenizer.tokenize(text)
            filtered_sentence = []
            for w in tokens:
                if w not in stoplist:
                    filtered_sentence.append(w)

            print(filtered_sentence)

    #------------------------get sentiment--------------------------

    def getSentiment(self):
        tweets = Database.getTweets(self)
        sid = SentimentIntensityAnalyzer()
        conn = sqlite3.connect('booksrecommender.db')
        cursor = conn.cursor()

        for tweet in tweets:
            id= tweet[0]
            ss = sid.polarity_scores(tweet[2])
            scorePos= ss["pos"]
            scoreNeg= ss["neg"]

            if scorePos > scoreNeg:
                print(tweet[2])
                cursor.execute(" UPDATE Status SET Sentiment= ?, Preference= ? WHERE ID= ? ", (scorePos, "positive", id));
                print(scorePos)
                conn.commit()

            elif scoreNeg > scorePos:
                print(tweet[2])
                cursor.execute(" UPDATE Status SET Sentiment= ?, Preference= ? WHERE ID= ? ", (scoreNeg, "negative", id));
                print(scoreNeg)
                conn.commit()











if __name__== '__main__':

    t= Tweets()
    t.gettokens()
