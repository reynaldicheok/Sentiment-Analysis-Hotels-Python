#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


#Create word cloud
#This below is for the preset data
df =pd.read_csv(r"C:\Users\Reynaldi\Downloads\SITProject\datafiniti_hotel_reviews.csv")
dfx=pd.read_csv(r"C:\Users\Reynaldi\Downloads\SITProject\datafiniti_hotel_reviews.csv")
#This below is for the airbnb locally sourced data,file contains latin special characters,encoding is used to make sure no error
#df =pd.read_csv(r"C:\Users\user\PycharmProjects\SITProject\listings.csv",encoding='latin1')
df.head()
print(len(df.index))


# In[3]:


#This below is for the preset data
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


# In[4]:


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


# In[5]:


dfx = dfx[dfx['reviews_rating'] != 3]
df = df[df['reviews_rating']==3] #Test data
print(len(df.index))
dfx['sentiment'] = dfx['reviews_rating'].apply(lambda rating : +1 if rating > 3 else -1)

# split df - positive and negative sentiment:
positive = dfx[dfx['sentiment'] == 1]
negative = dfx[dfx['sentiment'] == -1]
print(len(df.index))
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


# In[84]:


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
dfNew = dfx[['reviews_text','sentiment']]
dfNew.head()
dfnewer=df[['reviews_text']]
dfnewer.head()
function = lambda title: vader.polarity_scores(title)['compound']
dfnewer['compound'] = dfnewer['reviews_text'].apply(function)
dfnewer.head(100)


# In[87]:


def getAnalysis(score):
 if score < 0:
    return 'Negative'
 elif score == 0:
    return 'Neutral'
 else:
    return 'Positive'

dfnewer['sentiment'] = dfnewer['compound'].apply(getAnalysis)

dfnewer.head(5)
dfnewest=dfnewer[['reviews_text','sentiment']]
dfnewest.head(200)
dfnewest['sentimentt'] = dfnewest['sentiment'].replace({'Negative' : -1})
dfnewest['sentimentt'] = dfnewest['sentimentt'].replace({'Positive' : 1})
dfnewest['sentimentt'] = dfnewest['sentimentt'].replace({'Neutral' : 0})
dfnewest=dfnewest[['reviews_text','sentimentt']]
dfnewer.head(20)


# In[54]:


index = dfx.index
indexs=df.index

dfx['random_number'] = np.random.randn(len(index))
dfnewest['random_number'] = np.random.randn(len(indexs))
train = dfx[dfx['random_number'] <= 0.7]
test = dfx[dfx['random_number'] > 0.7]
train_x = dfnewest[dfnewer['random_number'] <= 0.7]
test_x = dfnewest[dfnewer['random_number'] > 0.7]
#print(len(test_x.index))
#print(len(test.index))
print(len(train.index))
#print(len(dfNew.index))
#train.head()
test_x.head()
print(len(test_x.index))
print(len(train_x.index))
#print(train[['reviews_text','sentiment']])
#print(test[['reviews_text','sentiment']])


# In[55]:


from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(token_pattern=r'\b\w+\b',stop_words=None)
train_matrix = vectorizer.fit_transform(train['reviews_text'])
test_matrix = vectorizer.transform(test['reviews_text'])
testx_matrix = vectorizer.transform(test_x['reviews_text'])
trainx_matrix = vectorizer.transform(train_x['reviews_text'])


# In[56]:


from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(solver='lbfgs', max_iter=15003,verbose=1)
lrx = LogisticRegression(solver='lbfgs', max_iter=15003,verbose=1)


# In[59]:


X_train = train_matrix
X_test = test_matrix
y_train = train['sentiment']
y_test = test['sentiment']
xx_test=testx_matrix
xxtrain=trainx_matrix


test_x['sentimentt'].astype(str).astype(int)
train_x['sentimentt'].astype(str).astype(int)
yy_train=train_x['sentimentt']
yy_test=test_x['sentimentt']
yy_train.head()


# In[60]:


lr.fit(X_train,y_train)
lrx.fit(xxtrain,yy_train)
lr.classes_


# In[77]:


predictions = lr.predict(X_test)
prediction2= lr.predict(xx_test)
predictionx=lrx.predict(xx_test)
print(predictionx)
test_x.head()


# In[71]:


from sklearn.metrics import confusion_matrix,classification_report
new = np.asarray(y_test)
#confusion_matrx(prediction2,yy_test)
confusion_matrix(prediction2,yy_test)


# In[81]:


target_names = ['Negative', 'Positive']
target_namesz = ['Negative', 'Neutral','Positive']
print(classification_report(y_test,predictions,target_names=target_names))
print(classification_report(yy_test,prediction2,target_names=target_namesz))
print(classification_report(yy_test,predictionx,target_names=target_namesz))


# In[ ]:




