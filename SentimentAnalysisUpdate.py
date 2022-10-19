import csv

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


# Use this function to read the file, input file path as input
def read_csv(filename):
    csv_file_df = pd.read_csv(filename)
    return csv_file_df


# Call this function and map it to a variable

# Use this function to generate a graph for data visualization with reference to the function read_csv
def generate_graph(csv_df):
    fig = px.histogram(csv_df, x="review-score")  # Change according to the current data set using

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
    textt = " ".join(map(str, csv_df.review_text))
    wordcloud = WordCloud(stopwords=stopwords).generate(textt)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('wordcloud12.png')
    plt.show()


def remove_punctuation(text):
    final = "".join(u for u in text if u not in ("?", ".", ";", ":", "!", '"'))
    return final


# Pre trained model to classify the test data
# Function to generate the data frame analysis column along with the vader lexicon compound numbers
# Used to get a solid breakdown later
def generate_dataframe_column(dataframe_input):
    dataframez = dataframe_input.dropna(subset=['review_text'])

    dataframenew = dataframez[['hotelname', 'postalcode', 'review_pos', 'review_neg', 'review_text', 'review-score']]
    function = lambda title: vader.polarity_scores(title)['compound']
    dataframenew['compound'] = dataframenew['review_text'].apply(function)
    dataframenew['sentiment_score'] = dataframenew['review-score'].apply(
        lambda rating: 'Positive' if rating > 3 else ('Neutral' if rating == 3 else 'Negative'))

    return dataframenew


def getAnalysis(
        score):  # Function to break down the compound scores given to us to determine if review is negative or positive
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'


def breakdown_dataframe(new_dataframe):  # Use with reference in regard to the generate_dataframe_column function important for later parts so please use this
    new_dataframe['sentiment'] = new_dataframe['compound'].apply(getAnalysis)
    # print(new_dataframe.head())
    newest_dataframe = new_dataframe[['hotelname', 'postalcode', 'review_pos', 'review_neg', 'review_text', 'review-score','sentiment','sentiment_score','compound']]

    newest_dataframe['sentimentt'] = newest_dataframe['sentiment'].replace({'Negative': -1})

    newest_dataframe['sentimentt'] = newest_dataframe['sentimentt'].replace({'Positive': 1})
    newest_dataframe['sentimentt'] = newest_dataframe['sentimentt'].replace({'Neutral': 0})
    # newest_dataframe.to_csv('Final_product.csv')
    # newest_dataframe = newest_dataframe[['reviews_text', 'sentimentt']]
    newest_dataframe['Combined Sentiment'] = newest_dataframe['sentiment_score']+newest_dataframe['sentiment'] #Merges sentiment together with rating first then reviews
    return newest_dataframe


def export_csv(dataframe): #outputs final csv file with the analysis portion done
    dataframe.to_csv('Final_product.csv')

def filterhotel(csvfile,hotelpostal): #Filter hotel base on postal code
    reader=csvfile
    reader=reader[reader['postalcode']==hotelpostal]
    hotelname=reader['hotelname'][0]
    reader.to_csv(hotelname+'.csv')

def lowest_review(csvfile): #most negative review
    reader=csvfile
    mostnegative=reader['compound'].min()
    listtest=reader.loc[reader['compound'] == mostnegative]
    finaltest=listtest.values.tolist()
    output=finaltest[0][0::]
    return output

def highest_review(csvfile): #Most positive review
    reader=csvfile
    mostpositive=reader['compound'].max()
    listtest=reader.loc[reader['compound'] == mostpositive]
    finaltest=listtest.values.tolist()
    output=finaltest[0][0::]
    return output

def wordcloud_gen(dataframe):  # Get dataframe from previous function breakdown_dataframe to generate word cloud
    positive = dataframe[dataframe['sentimentt'] == 1]
    negative = dataframe[dataframe['sentimentt'] == -1]
    # generate positive wordcloud
    pos = " ".join(review for review in positive.review_text)
    wordcloud2 = WordCloud(stopwords=stopwords).generate(pos)
    plt.imshow(wordcloud2, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('wordcloudPos.png')
    plt.show()

    # In[6]:

    # generate negative wordcloud
    neg = " ".join(review for review in negative.review_text)
    wordcloud3 = WordCloud(stopwords=stopwords).generate(neg)
    plt.imshow(wordcloud3, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('wordcloudNeg.png')
    plt.show()


def func(pct, allvalues): #Pie chart formatting
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n({:d})".format(pct, absolute)

def rating(csvfile):#Data display
    rowcount=len(csvfile.index)
    pos_count=len(csvfile[csvfile['sentiment_score']=='Positive'])
    neg_count=len(csvfile[csvfile['sentiment_score']=='Negative'])
    neutral_count=len(csvfile[csvfile['sentiment_score']=='Neutral'])
    pietest=np.array([pos_count,neg_count,neutral_count])
    mylabels = ["Positive", "Negative", "Neutral"]
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.pie(pietest,labels = mylabels, startangle = 90,autopct=lambda pct: func(pct, pietest),)
    ax.set_title("Overall review ratings")
    ax.legend(mylabels,title ="Sentiment",
          loc ="center left",
          bbox_to_anchor =(1, 1))
    plt.show()

def rating_further(csvfile):#DAta display with the neutral positive and neutral negative scores and neutral neutral
    pos_count = len(csvfile[csvfile['sentiment_score'] == 'Positive'])
    neg_count = len(csvfile[csvfile['sentiment_score'] == 'Negative'])
    neutral_count = len(csvfile[csvfile['sentiment_score'] == 'Neutral'])
    neutral_pos=len(csvfile[csvfile['Combined Sentiment']=='NeutralPositive'])
    neutral_neg=len(csvfile[csvfile['Combined Sentiment']=='NeutralNegative'])
    neutral_neutral = len(csvfile[csvfile['Combined Sentiment'] == 'NeutralNeutral'])
    total_pos=pos_count+neutral_pos
    total_neg=neg_count+neutral_neg
    total_neutral=neutral_count+neutral_neutral
    pietest = np.array([total_pos, total_neg, total_neutral])
    mylabels = ["Positive", "Negative", "Neutral"]
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.pie(pietest, labels=mylabels, startangle=90, autopct=lambda pct: func(pct, pietest), )
    ax.set_title("Overall review ratings with neutral breakdown")
    ax.legend(mylabels, title="Sentiment",
              loc="center left",
              bbox_to_anchor=(1, 1))
    plt.show()


if __name__ == '__main__':
    # Sample on how to use the whole program
    print("Test")
    test = pd.read_csv(r"C:\Users\Reynaldi\Downloads\SingaporeHotel (3).csv",
                       encoding='latin1')  # Use your own local file location
    #graph = generate_graph(test)
    print("pass")
    #graphz = generate_stopword(test)
    dataframez = generate_dataframe_column(test)
    new_dataframez = breakdown_dataframe(dataframez)
    rating(new_dataframez)
    rating_further(new_dataframez)
    #print(new_dataframez.head())

    #word_cloud_gen = wordcloud_gen(new_dataframez)
    #export_csv(new_dataframez)
    #print(new_dataframez.head(10))
    #filterhotel(dataframez,189673)
