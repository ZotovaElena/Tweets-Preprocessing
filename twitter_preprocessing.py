import pickle
import pandas as pd
import re
import nltk
import string
from pymystem3 import Mystem

mystem = Mystem()  

emoticons_str = r"""
        (?:
            [:=;] # Eyes
            [oO\-]? # Nose (optional)
            [D\)\]\(\]/\\OpP] # Mouth
        )"""

regex_str = [
        emoticons_str,
        r'<[^>]+>', # HTML tags
        r'(?:@[\w_]+)', # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
     
        r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
        r'(?:[\w_]+)', # other words
        r'(?:\S)' # anything else
    ]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
    
def tokenize(s):
    return tokens_re.findall(s)

     
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens



def is_number(s):
    number_list = ['0','1','2','3','4','5','6','7','8','9',',','.']
    number = True
    for c in s:
        if c not in number_list:
            number = False
    return number


def clean_tweets(tweets, model_path = None):
    
    #Get tweet list
    tweets = tweets.fillna('')
    tweets_text = tweets.text.values
    tweets_text = list(tweets.text.values)
    tweets["text_clean"] = ""
    
    # Create stopword list
    stopwords = nltk.corpus.stopwords.words('russian')
    stopwords_delete = ['хорошо', 'лучше', 'может', 'никогда', 'нельзя', 'всегда']
    stopwords_add = ['это', 'который', "хотя", "кстати"]
            
    new_stopwords = []
    for word in stopwords:
        if word not in stopwords_delete:
            new_stopwords.append(word)
    stopwords = new_stopwords
    if len(stopwords_add) != 0:
        stopwords += stopwords_add
    punctuation = list(string.punctuation)
    punctuation += ['–', '—', '"', "¿", "¡"]
    stop = stopwords + punctuation + ['rt', 'via']
    
    
    for i, tweet in enumerate(tweets_text):
        tweets_clean = []
        tokens = preprocess(tweet, lowercase=True)
        tweet_tok = []
        for token in tokens:
            if token not in stop and not emoticon_re.search(token) and not is_number(token) and not token.startswith(('#', '@', 'http')):
                tweet_tok.append(token)

        tweets_clean.append(tweet_tok)
        tweets["text_clean"][i] = " ".join(tweet_tok)
        
    return tweets

def lemmatize(tweets_clean):
        tweets_clean["text lemmatized"] = ""
        #make variables from dataframe
        tweets = tweets.fillna('')
        tweets_text = tweets_clean.text_clean.values
        tweets_text = list(tweets_clean.text_clean.values)

        print("lemmitizing")
        #lemmatize clean text and make a new column with lemmas
        for i, tweet in enumerate(tweets_text):
            tweet_lem = []
            lemmas = mystem.lemmatize(tweet.lower())
            lemmas = " ".join(lemmas).split()
            print("Lemma", lemmas)

            for l in lemmas:
                if l not in additional_stopwords:
                    tweet_lem.append(l)

            tweets_clean["text lemmatized"][i] = " ".join(tweet_lem)
            #print( tweets["text lemmatized"][i])
        return tweets_clean
                
additional_stopwords = ["еще", "ещё", "меж", "зато", "пусть", "ага", "этот", "это", "почему", 
                        "весь", "ты", "он", "она", "они", "оно", "мы", "вы", "кто", "что", 
                        "сам", "сама", "само", "свой", "наш", "ваш", "их", "тот", "та", "те", 
                        "то", "раз", "твой", "мой", "кой", "кое", "все", "весь", "всё", "быть", "тот", 
                        "таки", "такой", "какой", "каждый", "который", "и", "а", "в", "б", "д", 
                        "е", "ж", "з", "к", "л", "м", "н", "о", "п", "р", "с", "у", "ф", "ч", 
                        "ц", "ш", "щ", "ь", "ъ","э", "ю", "я"]
 
#load tweets from CSV
tweets = pd.read_csv('tweets.csv', sep=',')
tweets = tweets.fillna('')
#make new dataframe with column "clean text", where the text without stopwords and punctuation saved
tweets_clean = clean_tweets(tweets)

lemmatize(tweets_clean)
#write the dataframe to pickle 
lemmas_pickle = open("twitter_lemmatized_full_table.pickle","wb")
pickle.dump(tweets_clean, lemmas_pickle)
lemmas_pickle.close()    
#write a CSV file with the new table
tweets_clean.to_csv("tweets_clean.csv", sep='\t', encoding='utf-8')
