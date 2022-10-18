import pandas as pd
import numpy as np

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()
import string


#def top15_words(hoteloutputcsv):
df = pd.read_csv('Hotel Boss.csv', encoding = "ISO-8859-1")

#synonym check
_review_2 = []
# getting review strings and appending it to the _review_ list
for review in df.review_text:
    _review_2.append(review)

# setting a function that will split those reviews strings into separate words
def split_name(review):
    spl = str(review).split()
    return spl

# initializing empty list where we are going to have words counted
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
_review_count_ = []

# getting name string from our list and using split function, later appending to list above
# Punctuation: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
punctuation = [",",";",":","?",".","\'","\\","-","(",")","+","#","@","<",">","_","{","}","[","]","/","*","%"]

for x in _review_2:
    for word in split_name(x):
        if word in punctuation:
            continue
        else:
            word = word.strip() #removes whitespace
            word = word.lower()
            if word not in stopwords:
                word = word.translate(str.maketrans('', '', string.punctuation))
                _review_count_.append(word)

# we are going to use counter
from collections import Counter

comfortable_synonyms = ["comfy","cosy","warm","pleasant","enjoyable","agreeable","congenial","plush","secure","safe","homely","snuggly"]
service_synonyms = ["staff","staffs","servicing","assistance","help","cleaning","equipped","provided","housekeeping","reception","cleaned","towel","towels","sanitize","sanitise"]
dorm_synonyms = ["dorms"]
apartment_synonyms = ["apartments"]
toilet_synonyms = ["toilets","bathroom","bathrooms","lavatory","lavatories","urinal"]
pool_synonyms = ["pools","swim","swimming"]
kid_synonyms = ["kid","kids","children","child","youngster","baby","toddler","infant","minor","adolescent","teenager","youth"]
restaurant_synonyms = ["restaurants","eatery"]
aircon_synonyms = ["ac","aircon","air-con","aircondition","air-condition","airconditioner","air-conditioner"]
location_synonyms = ["spot","place","area"]
#_synonyms = []
for i in range(len(_review_count_)):
    if _review_count_[i] in comfortable_synonyms:
        _review_count_[i] = "comfortable"
    elif _review_count_[i] in service_synonyms:
        _review_count_[i] = "service"
    elif _review_count_[i] in dorm_synonyms:
        _review_count_[i] = "dorm"
    elif _review_count_[i] in apartment_synonyms:
        _review_count_[i] = "apartment"
    elif _review_count_[i] in toilet_synonyms:
        _review_count_[i] = "toilet"
    elif _review_count_[i] in pool_synonyms:
        _review_count_[i] = "pool"
    elif _review_count_[i] in kid_synonyms:
        _review_count_[i] = "kid-friendly"
    elif _review_count_[i] in restaurant_synonyms:
        _review_count_[i] = "restaurant"
    elif _review_count_[i] in aircon_synonyms:
        _review_count_[i] = "air-conditioned"
    elif _review_count_[i] in location_synonyms:
        _review_count_[i] = "location"
    else:
        continue

_top_15_w = Counter(_review_count_).most_common()
# Sort number of words viewed
_top_15_w = _top_15_w[0:15]

sub_w=pd.DataFrame(_top_15_w)
sub_w.rename(columns={0:'Words', 1:'Count'}, inplace=True)

plt.figure(figsize=(10,6))
viz_5=sns.barplot(x='Words', y='Count', data=sub_w)
viz_5.set_title('Top 15 words used in reviews')
viz_5.set_ylabel('Word Count')
viz_5.set_xlabel('Words')
viz_5.set_xticklabels(viz_5.get_xticklabels(), rotation=80)
plt.savefig('top15words.png')
plt.show()
