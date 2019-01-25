# Russian Tweets Preprocessing

Script for Russian text preprocessing of Twitter. It can be used to:
- tokenize the text with regular expressions
- clean up the text: remove punctuation, links, ats, hashtags, stopwords. You can add and remove your own stopwords and remove or leave any token. 
- set all the words to their initial form 
- return a new dataframe with two additional columns: Clean text and Lemmitized text
- store the dataframe in Pickle and .CSV. 

Requirements: 

Python 3 

pickle
pandas 
re
nltk
string
Mystem
