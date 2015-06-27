import json
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import re



def main():
    
    
    #Reading Tweets
    print 'Reading Tweets\n'
    tweets_data_path = '/Users/simbar012/Projects/Twitter_Analysis/twitter_output_copy.txt'
    
    tweets_data = []
 
    
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            txt = TextBlob(tweet['text'])
            
            
            
        
            if txt.sentiment.polarity < 0:
                sent_val = "negative"
            elif txt.sentiment.polarity ==0:
                sent_val = "neutral"
            else:
                sent_val = "postive"
  
            tweet.append(sent_val)
            json.dump(tweet, tweets_file)
            
            
        except:
            continue


    # Structuring Tweets
    print 'Structuring Tweets\n'
    tweets=pd.DataFrame()
    tweets['sentiment'] = map(lambda tweet: tweets_data, tweets_data)
    tweets['text'] = map(lambda tweet: tweet['text'] if 'text'in tweet  else'', tweets_data)


    #Analyzing Tweets by Language
    print 'Analyzing tweets\n'

    tweets_by_sentiment = tweets['sentiment'].value_counts()
    fig, ax = plt.subplots()


    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Sentiment', fontsize=15)
    ax.set_ylabel('Number of tweets' , fontsize=15)
    ax.set_title('Sentiment Analysis', fontsize=15, fontweight='bold')
    tweets_by_sentiment[:3].plot(ax=ax, kind='bar', color='red')
    plt.savefig('tweet_by_sentiment', format='png')

if __name__=='__main__':
    main()


