import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()
from wordcloud import WordCloud
import numpy as np
import plotly.offline as py

import plotly.graph_objs as go
import plotly.tools as tls
import plotly.express as px

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
vader = SentimentIntensityAnalyzer()


#Use this function to read the file, input file path as input
def read_csv(filename):
    csv_file_df=pd.read_csv(filename)
    return csv_file_df
#Call this function and map it to a variable

#Use this function to generate a graph for data visualization with reference to the function read_csv
def generate_graph(csv_df):
    fig = px.histogram(csv_df, x="reviews_rating")

    # This Below is for the airbnb locally sourced data
    # fig = px.histogram(df, x="review_scores_rating")
    fig.update_traces(marker_color="blue", marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5)
    fig.update_layout(title_text='Product Score')
    fig.show()
    return fig

stopwords = set(stopwords.words('english'))

# use this function to generate a stop word with the input being the output of the function read_csv
def generate_stopword(csv_df):


    stopwords.update(["br", "href", "room", "hotel", "rooms", "good", "great"])
    textt = " ".join(map(str, csv_df.reviews_text))
    wordcloud = WordCloud(stopwords=stopwords).generate(textt)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('wordcloud12.png')
    plt.show()

def remove_punctuation(text):
    final = "".join(u for u in text if u not in ("?", ".", ";", ":",  "!",'"'))
    return final

 #Pre trained model to classify the test data
#Function to generate the data frame analysis column along with the vader lexicon compound numbers
#Used to get a solid breakdown later
def generate_dataframe_column(dataframe):
    dataframe = dataframe.dropna(subset=['reviews_text'])
    dataframe['reviews_text'] = dataframe['reviews_text'].apply(remove_punctuation)
    dataframenew = dataframe[['reviews_text']]
    function = lambda title: vader.polarity_scores(title)['compound']
    dataframenew['compound'] = dataframenew['reviews_text'].apply(function)
    return dataframenew




def getAnalysis(score): #Function to break down the compound scores given to us to determine if review is negative or positive
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

def breakdown_dataframe(new_dataframe): #Use with reference in regard to the generate_dataframe_column function
    new_dataframe['sentiment'] = new_dataframe['compound'].apply(getAnalysis)
    #print(new_dataframe.head())
    newest_dataframe = new_dataframe[['reviews_text','sentiment']]

    newest_dataframe['sentimentt'] = newest_dataframe['sentiment'].replace({'Negative' : -1})

    newest_dataframe['sentimentt'] = newest_dataframe['sentimentt'].replace({'Positive': 1})
    newest_dataframe['sentimentt'] = newest_dataframe['sentimentt'].replace({'Neutral': 0})
    #newest_dataframe.to_csv('Final_product.csv')
    #newest_dataframe = newest_dataframe[['reviews_text', 'sentimentt']]


    return newest_dataframe

def export_csv(dataframe):
    dataframe.to_csv('Final_product.csv')


def wordcloud_gen(dataframe): #Get dataframe from previous function breakdown_dataframe to generate word cloud
    positive = dataframe[dataframe['sentimentt'] == 1]
    negative = dataframe[dataframe['sentimentt'] == -1]
    # generate positive wordcloud
    pos = " ".join(review for review in positive.reviews_text)
    wordcloud2 = WordCloud(stopwords=stopwords).generate(pos)
    plt.imshow(wordcloud2, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('wordcloudPos.png')
    plt.show()

    # In[6]:

    # generate negative wordcloud
    neg = " ".join(review for review in negative.reviews_text)
    wordcloud3 = WordCloud(stopwords=stopwords).generate(neg)
    plt.imshow(wordcloud3, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('wordcloudNeg.png')
    plt.show()

if __name__ == '__main__':
    #Sample on how to use the whole program
    print("Test")
    test=read_csv(r"C:\Users\Reynaldi\Downloads\SITProject\datafiniti_hotel_reviews.csv") #Use your own local file location
    #graph=generate_graph(test)

    #graphz=generate_stopword(test)
    dataframez=generate_dataframe_column(test)
    new_dataframez = breakdown_dataframe(dataframez)

    print(new_dataframez.head())

    word_cloud_gen = wordcloud_gen(new_dataframez)
