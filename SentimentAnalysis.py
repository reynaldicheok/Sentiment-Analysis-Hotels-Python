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


#Create word cloud
#This below is for the preset data
def read_csv(filename):
    csv_file_df=pd.read_csv(filename)
    return csv_file_df
df =pd.read_csv(r"C:\Users\Reynaldi\Downloads\SITProject\datafiniti_hotel_reviews.csv") #Change this in according to scrape data
dfx=pd.read_csv(r"C:\Users\Reynaldi\Downloads\SITProject\datafiniti_hotel_reviews.csv") #Change this in accordance to scrape data
#untouched=pd.read_csv(r"C:\Users\Reynaldi\Downloads\SITProject\datafiniti_hotel_reviews.csv")

#This below is for the airbnb locally sourced data,file contains latin special characters,encoding is used to make sure no error
#df =pd.read_csv(r"C:\Users\user\PycharmProjects\SITProject\listings.csv",encoding='latin1')
#df.head()
#print(len(df.index))


#This below is for the preset data
def generate_graph(csv_df):
    fig = px.histogram(csv_df, x="reviews_rating")

    # This Below is for the airbnb locally sourced data
    # fig = px.histogram(df, x="review_scores_rating")
    fig.update_traces(marker_color="blue", marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5)
    fig.update_layout(title_text='Product Score')
    fig.show()
    return fig

#Code below was for testing purpose feel free to remove at a later date
fig = px.histogram(df, x="reviews_rating")
figx= px.histogram(dfx, x="reviews_rating")
#This Below is for the airbnb locally sourced data
#fig = px.histogram(df, x="review_scores_rating")
fig.update_traces(marker_color="blue",marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5)
fig.update_layout(title_text='Product Score')
fig.show()
figx.update_traces(marker_color="blue",marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5)
figx.update_layout(title_text='Product Score')
figx.show()


# Create stopword list:
stopwords = set(stopwords.words('english'))

stopwords.update(["br", "href","room","hotel","rooms","good","great"])
textt = " ".join(map(str,df.reviews_text))
wordcloud = WordCloud(stopwords=stopwords).generate(textt)
print(wordcloud)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig('wordcloud12.png')
plt.show()


dfx = dfx[dfx['reviews_rating'] != 3]
df = df[df['reviews_rating']!=3] #Test data

dfx['sentiment'] = dfx['reviews_rating'].apply(lambda rating : +1 if rating > 3 else -1)

# split df - positive and negative sentiment:
positive = dfx[dfx['sentiment'] == 1]
negative = dfx[dfx['sentiment'] == -1]

#generate positive wordcloud
pos = " ".join(review for review in positive.reviews_text)
wordcloud2 = WordCloud(stopwords=stopwords).generate(pos)
plt.imshow(wordcloud2, interpolation='bilinear')
plt.axis("off")
plt.savefig('wordcloudPos.png')
plt.show()
dfx.head()


# In[6]:


#generate negative wordcloud
neg = " ".join(review for review in negative.reviews_text)
wordcloud3 = WordCloud(stopwords=stopwords).generate(neg)
plt.imshow(wordcloud3, interpolation='bilinear')
plt.axis("off")
plt.savefig('wordcloudNeg.png')
plt.show()


# In[7]:


dfx['sentimentt'] = dfx['sentiment'].replace({-1 : 'negative'})
dfx['sentimentt'] = dfx['sentimentt'].replace({1 : 'positive'})
fig = px.histogram(dfx, x="sentimentt")
fig.update_traces(marker_color="indianred",marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5)
fig.update_layout(title_text='Product Sentiment')
fig.show()


# In[8]:


dfx.head()
print(len(df.index))
def remove_punctuation(text):
    final = "".join(u for u in text if u not in ("?", ".", ";", ":",  "!",'"'))
    return final
dfx = dfx.dropna(subset=['reviews_text'])
dfx['reviews_text'] = dfx['reviews_text'].apply(remove_punctuation)
df=df.dropna(subset=['reviews_text'])
df['reviews_text'] = df['reviews_text'].apply(remove_punctuation)

#df['reviews_title'] = df['reviews_title'].apply(remove_punctuation)
dfNew = dfx[['reviews_text','sentiment']] #Control data set

dfnewer=df[['reviews_text']] #Used for testing later

function = lambda title: vader.polarity_scores(title)['compound'] #Pre trained model to classify the test data
dfnewer['compound'] = dfnewer['reviews_text'].apply(function)



def getAnalysis(score): #Function to break down the compound scores given to us to determine if review is negative or positive
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

dfnewer['sentiment'] = dfnewer['compound'].apply(getAnalysis) #Gives the data frame the values Negative Neutral or Positive under the sentiment column based on the compound number implemented by the function

dfnewest=dfnewer[['reviews_text','sentiment']] #creates a new dataframe that only has review text and sentiment column
dfnewest['sentimentt'] = dfnewest['sentiment'].replace({'Negative' : -1}) #Create a new column to change the classifications into numbers to be used later
dfnewest['sentimentt'] = dfnewest['sentimentt'].replace({'Positive' : 1})
dfnewest['sentimentt'] = dfnewest['sentimentt'].replace({'Neutral' : 0})
dfnewest=dfnewest[['reviews_text','sentimentt']] #New data frame containing only the number classification and the review text
dfnewest.to_csv('Pretrained_outputz.csv')

