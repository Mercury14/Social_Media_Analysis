import json
import nltk
import pandas as pd
import matplotlib.pyplot as plt
import re
import collections
import pygal
import numpy as np
import unicodedata
from textblob import TextBlob
from pygal.style import LightStyle


def main():
    
    
    #Reading Tweets
    print 'Reading Tweets\n'
    tweets_data_path = '/Users/simbar012/Projects/Twitter_Analysis/output.txt'
        
    tweets_data = []
   
    
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        
        
        except:
            continue
    


    
    
    # Create a data frame
    print 'Structuring Tweets\n'
    tweets = pd.DataFrame()
    
    # Populate data frame
    tweets['text'] = map(lambda tweet: tweet['text'] if 'text' in tweet else'', tweets_data)
    tweets['lang'] = map(lambda tweet: tweet['lang']if 'lang' in tweet else'', tweets_data)
    tweets['screen_name'] = map(lambda tweet: tweet['user']['screen_name'] if 'screen_name' in tweet else'',tweets_data)
    
        
        
    #Analyzing Tweets by Language
    print 'Analyzing tweets by language\n'
    plt.style.use('dark_background')
    tweets_by_lang = tweets['lang'].value_counts()
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Languages', fontsize=15)
    ax.set_ylabel('Number of tweets' , fontsize=15)
    ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
    tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')
    plt.savefig('tweet_by_lang', format='png')
    plt.clf()


    # Use collection for counting frequency


    user_count = collections.Counter()
    for i in tweets_data:
        try:
            user_count [i['user']['screen_name']] +=1
        except KeyError:
            pass


       


    # Prepare the SVG plot

    barplot = pygal.HorizontalBar( style=pygal.style.LightStyle, space=50, x_title='Number of Tweets')
    topnum = 10
    for i in range(topnum):
        barplot.add( user_count.most_common(topnum)[i][0],[{'value': user_count.most_common(topnum)[i][1],'label':user_count.most_common(topnum)[i][0]}])
    
    barplot.config.title=barplot.config.title="Top " + str(topnum) + " Most Prolific Tweeters"
    barplot.config.lengend_at_bottom=True
    
    barplot.render_to_file("Top_Tweeters.svg")


    # Tweets with the most RT count > 1
    count = collections.Counter()
    for i in tweets_data:
        try:
            count [i['text']] +=1
        except KeyError:
            pass
                   
                                 
    frdf = []
    for i,j in count.iteritems():
        if j > 10:
            frdf.append([j, i])
                                 
    df = pd.DataFrame(frdf, index=None, columns=["Count", "Tweet"])
    df.sort(columns="Count", inplace=True, ascending=False)

    for i,j,k in df.itertuples():
        print j,"\t", k


    # Sentiment analysis of tweets
    count_neg = 0
    count_neu = 0
    count_pos = 0


    for i in tweets_data:
        
        try:
            blob = TextBlob (i['text'])
            if blob.sentiment.polarity < 0:
                count_neg += 1
            elif blob.sentiment.polarity ==0:
                count_neu +=1
            else:
                count_pos +=1
        except KeyError:
            pass

    print '/n'
    print "Count of Tweet Sentiment \n"
    print "pos: ", count_pos, '\n'
    print "neu: ", count_neu, '\n'
    print "neg: ", count_neg, '\n'

    labels ='Positive', 'Neutral', 'Negative'
    sizes = [count_pos, count_neu, count_neg]
    colors = ['green', 'yellow', 'red']
    explode = (0.1, 0, 0)
    plt.style.use('dark_background')
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
    plt.axis('equal')
    plt.title("Count of Tweet Sentiment")
    plt.figure(1)
    plt.savefig('count_of_sentiment', format='png')


if __name__=='__main__':
    main()


