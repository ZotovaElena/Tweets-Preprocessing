# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 20:23:21 2020

перед тем, как прочитать tweet.js, нужно убрать текст перед самой первой скобкой и после самой последней скобки
так, чтобы .js начинался и заканчивался скобкой.   


"""

import json
import pandas as pd 

with open('data/tweet.js','r', encoding='utf-8') as f:
   data = f.read()
   twitter_data = json.loads(data)
   

tweets = []
dates = []
ids = []
retweeted = []
favorited = []
for i in twitter_data: 
	# здесь можно добавлять все поля или только те, которые интересны
	tweets.append(i['tweet']['full_text']) 		
	dates.append(i['tweet']['created_at'])
	ids.append(i['tweet']['id_str'])
	retweeted.append(i['tweet']['retweeted'])
	favorited.append(i['tweet']['favorited'])

years = []
months = []
times = []
for i in dates: 
	year = i.split()[-1]
	years.append(year)
	month = i.split()[1:3]
	months.append(' '.join(month))
	time = i.split()[3]
	times.append(time)
	
df = pd.DataFrame(list(zip(ids, dates, years, months, times, tweets, retweeted, favorited)), columns=['id', 
				  'date', 'year', 'month', 'time', 'tweet', 'is_retweeted', 'is_favorited'])
	
df.to_csv('my_twitter.tsv', sep='\t', index=False)
	