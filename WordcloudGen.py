import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()
from wordcloud import WordCloud

import plotly.offline as py

import plotly.graph_objs as go
import plotly.tools as tls
import plotly.express as px

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

#Create word cloud
#This below is for the preset data
df =pd.read_csv(r"C:\Users\user\PycharmProjects\SITProject\SingaporeHotel.csv")
#This below is for the airbnb locally sourced data,file contains latin special characters,encoding is used to make sure no error
#df =pd.read_csv(r"C:\Users\user\PycharmProjects\SITProject\listings.csv",encoding='latin1')
df.head()
#This below is for the preset data
fig = px.histogram(df, x="review-score")
#This Below is for the airbnb locally sourced data
#fig = px.histogram(df, x="review_scores_rating")
fig.update_traces(marker_color="blue",marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5)
fig.update_layout(title_text='Review Score')
fig.show()

# Create stopword list:
stopwords = set(stopwords.words('english'))
stopwords.update(["br", "href","room","hotel","rooms","good","great"])
textt = " ".join(map(str,df.review_text))
wordcloud = WordCloud(stopwords=stopwords).generate(textt)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig('wordcloud12.png')
plt.show()

# assign reviews with score > 3 as positive sentiment
# score < 3 negative sentiment
# remove score = 3

df = df[df['review-score'] != 3]
df['sentiment'] = df['review-score'].apply(lambda rating : +1 if rating > 3 else -1)

# split df - positive and negative sentiment:
positive = df[df['sentiment'] == 1]
negative = df[df['sentiment'] == -1]

#generate positive wordcloud
pos = " ".join(review for review in positive.review_text)
wordcloud2 = WordCloud(stopwords=stopwords).generate(pos)
plt.imshow(wordcloud2, interpolation='bilinear')
plt.axis("off")
plt.savefig('wordcloudPos.png')
plt.show()
#generate negative wordcloud
neg = " ".join(review for review in negative.review_text)
wordcloud3 = WordCloud(stopwords=stopwords).generate(neg)
plt.imshow(wordcloud3, interpolation='bilinear')
plt.axis("off")
plt.savefig('wordcloudNeg.png')
plt.show()