import pandas as pd
import re
import nltk
import string
from pymystem3 import Mystem

mystem = Mystem()  

#converting oldschool emoticons to tokens
emoticons_str = r"""
		(?:
			[:=;] # Eyes
			[oO\-]? # Nose (optional)
			[D\)\]\(\]/\\OpP] # Mouth
		)"""

#making tokens from words, URLs, hashtags etc. 
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

#main process of text cleaning
def clean_tweets(tweets, model_path = None):
	
	#Get tweet list
	tweets = tweets.fillna('')
	tweets_text = tweets.text.values
	tweets_text = list(tweets.text.values)
	
  # Create stopword list
	stopwords = nltk.corpus.stopwords.words('russian')
	stopwords_delete = ['хорошо', 'лучше', 'может', 'никогда', 'нельзя', 'всегда']
	stopwords_add = ['это', 'который']
			
	new_stopwords = []
	for word in stopwords:
		if word not in stopwords_delete:
			new_stopwords.append(word)
	stopwords = new_stopwords
	if len(stopwords_add) != 0:
		stopwords += stopwords_add
	punctuation = list(string.punctuation)
	punctuation += ['–', '—', '"', "¿", "¡"]
  #list of everything wee need to remove
	stop = stopwords + punctuation + ['rt', 'via']
    
    
	tweets_clean = []
	for tweet in tweets_text:
		tokens = preprocess(tweet, lowercase=True)
		tweet_tok = []
		for token in tokens:
			if token not in stop and not emoticon_re.search(token) and not is_number(token) and not token.startswith(('#', '@', 'http')):
				tweet_tok.append(token)
										        
		if len(tweet_tok) > 0:
			tweets_clean.append(tweet_tok)
	return tweets_clean

#load tweets from CSV
tweets = pd.read_csv('tweets.csv', sep=',')
tweets_clean = clean_tweets(tweets)

#tweets preprodessed without lemmatization
tweets_clean_text = []
for t in tweets_clean:
    tweet_clean_text = " ".join(t)
    tweets_clean_text.append(tweet_clean_text)

print("lemmitizing")

#list of strings lemmatized
tweets_lemma = []
for tweet in tweets_clean_text:
    lem = mystem.lemmatize(tweet.lower())
    print("Lemma", lem)
    tweet_lemma = " ".join(lem)
    tweets_lemma.append(tweet_lemma)
    
#list of tokens lemmatized
tweets_lemma_tokenized = []
for t in tweets_lemma:
    words = t.split()
    tweet_tokenized = []
    for w in words: 
        tweet_tokenized.append(w)
    tweets_lemma_tokenized.append(tweet_tokenized)
