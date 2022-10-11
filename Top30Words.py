import pandas as pd
import numpy as np

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()


df = pd.read_csv('datafiniti_hotel_reviews (2).csv', encoding = "ISO-8859-1")
_review_ = []
# getting review strings and appending it to the list
for review in df.reviews_text:
    _review_.append(review)

# setting a function that will split those reviews strings into separate words
def split_name(review):
    spl = str(review).split()
    return spl

# initializing empty list where we are going to have words counted
stopwords = set(stopwords.words('english'))
stopwords.update(["br", "href","room","hotel","rooms","good","great"])
_review_count_ = []
# getting name string from our list and using split function, later appending to list above
for x in _review_:
    for word in split_name(x):
        word = word.lower()
        if word not in stopwords:
            _review_count_.append(word)

# we are going to use counter
from collections import Counter


_top_20_w = Counter(_review_count_).most_common()
# Sort number of words viewed
_top_20_w = _top_20_w[0:30]

sub_w=pd.DataFrame(_top_20_w)
sub_w.rename(columns={0:'Words', 1:'Count'}, inplace=True)

plt.figure(figsize=(10,6))
viz_5=sns.barplot(x='Words', y='Count', data=sub_w)
viz_5.set_title('Counts of the top 30 used words for reviews')
viz_5.set_ylabel('Count of words')
viz_5.set_xlabel('Words')
viz_5.set_xticklabels(viz_5.get_xticklabels(), rotation=80)
plt.savefig('top20words.png')
plt.show()
