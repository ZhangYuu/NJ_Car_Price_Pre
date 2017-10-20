#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 16:40:41 2017

@author: Memo
"""
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import datetime
import json
# set your keys to access tweets 
consumer_key = '7IKU6Hu1SfGPpyelNdJQOsMFc'
consumer_secret = 'rIibmcfcKxP6Z1o1owJz7kNc07R8odwlXqQZLi6twL7o6A0tMg'
access_token = '910751477613912064-5RlHjVTdAkAydsBfQeMDR7fGRWMMP65'
access_secret = 'KD2sFx2dGgTaeTrvoPYLVLcmPCiD9Py9O19XenU0SDx0g'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

class MyListener(StreamListener):   
    # constructor
    def __init__(self, output_file, time_limit):        
            # attribute to get listener start time
            self.start_time=datetime.datetime.now()
            # attribute to set time limit for listening
            self.time_limit=time_limit            
            # attribute to set the output file
            self.output_file=output_file            
            # initiate superclass's constructor
            StreamListener.__init__(self)    
    # on_data is invoked when a tweet comes in
    # overwrite this method inheritted from superclass
    # when a tweet comes in, the tweet is passed as "data"
    def on_data(self, data):        
        # get running time
        running_time=datetime.datetime.now()-self.start_time
        print(running_time)        
        # check if running time is over time_limit
        if running_time.seconds/60.0<self.time_limit:            
            # ***Exception handling*** 
            # If an error is encountered, 
            # a try block code execution is stopped and transferred
            # down to the except block. 
            # If there is no error, "except" block is ignored
            try:
                # open file in "append" mode
                with open(self.output_file, 'a') as f:
                    # Write tweet string (in JSON format) into a file
                    f.write(data)                    
                    # continue listening
                    return True               
            # if an error is encountered
            # print out the error message and continue listening           
            except BaseException as e:
                print("Error on_data:" , str(e))               
                # if return "True", the listener continues
                return True           
        else:  # timeout, return False to stop the listener
            print("time out")
            return False
    # on_error is invoked if there is anything wrong with the listener
    # error status is passed to this method
    def on_error(self, status):
        print(status)
        # continue listening by "return True"
        return True
    
def get_tweets():
    tweet_listener=MyListener(output_file="python.txt",time_limit=3)
    
    # start a staeam instance using authentication and the listener
    twitter_stream = Stream(auth, tweet_listener)
    # filtering tweets by topics
    twitter_stream.filter(track=['#Nissan'])
    
    tweets=[]
    with open("python.txt", 'r') as f:
    # each line is one tweet string in JSON format
        for line in f:
            tweet = json.loads(line)               
            tweets.append(tweet)
    # write the whole list back to JSON
    json.dump(tweets, open("Assignment.json",'w'))
    
    # to load the whole list
    # pay attention to json.load and json.loads
    tweets=json.load(open("Assignment.json",'r'))
    print("number of tweets:", len(tweets))
    
    all_tweets=[]
    
    tweets=json.load(open("Assignment.json",'r'))
    print("number of tweets:", len(tweets))
    
    for tweet in tweets:
        all_tweets.append( (tweet["created_at"], tweet["text"]) )
    return all_tweets

if __name__ == "__main__":
    b=get_tweets()
    print b