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
stopwords.update(["br","href","hotel","room","rooms","stay","stayed","would","could","really","get","also","us","one","time","great",
                  "good","bad","nice","like","best","review","reviews","negative","positive","little","well","check","super",
                  "quite","india","singapore","malaysia","china","japan","korea","philippines","door","day","night","everything",
                  "nothing","entrance","need","first","last","close","even","in","pillow","pillows","still","wet","value","late",
                  "guest","guests","always","morning","sleep","place","places","feel","feels","people","floor","front","worth",
                  "walking","lovely","love","made","make","plus","overall","air","free","pressure","it","access","go","wonderful",
                  "probably","2","near","staying","within","better","request","around","size","long","way","activity","too","got"
                  "activities","two","loved","especially","much","property","back","desk","in","1","bit","ice","tap","told","side",
                  "water","take","cream","new","excellent","different","though","lobby","took","well","walk","available","next","3",
                  "wait","lack","perfect","book","booked","booking","early","fun","ask","asked","enough","amazing","rail","rails",
                  "easy","hard","difficult","extremely","extreme","4","smell","5","6","7","8","9","10","money","every","food","space",
                  "distance","many","hear","said","pay","days","ok","okay","price","luggage","pretty","fast","all","due","noise","dirty",
                  "filthy","greasy","sooty","moldy","grimy","grubby","soiled","unwashed","stain","stained","spotted","cloudy","muddy",
                  "dusty","paper"])
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
