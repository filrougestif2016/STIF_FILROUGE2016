# -*- coding: utf8 -*-
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from contextlib import contextmanager
import multiprocessing
from optparse import OptionParser
import json
import re
import sys

#Variables that contains the user credentials to access Twitter API
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

output="twitter.output"
lexical="lexique.txt"

@contextmanager
def redirect_stdout(stream):
    old_stdout = sys.stdout
    sys.stdout = stream
    try:
        yield
    finally:
        sys.stdout = old_stdout

def handler(signum, frame):
    print ('Signal handler called with signal', signum)
    raise IOError("Twitter streaming stopped")

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        with open(output,'a+') as f:
            with redirect_stdout(f):
                print(data)
                return True

    def on_error(self, status):
        print(status)

def getAuth() :
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth

def getQueryContent():
    content=[]
    with open(lexical) as f:
        content = f.readlines()
    content = [x.rstrip() for x in content]
    return(content)



def twitterTrack(qry):
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    # auth = OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    auth = getAuth()
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=qry,languages=['fr'])




def printTweetsText(df):
    exclude = re.compile(r'^.*#MTVStars.*$')
    for index, row in df.iterrows():
        try :
            text = row['text']
        except:
            continue

        if not re.match(exclude, text):
            print("-------screen_name=",row['user']['screen_name'])
            print(text)


if __name__ == '__main__':
    words=getQueryContent()
    p = multiprocessing.Process(target=twitterTrack, name="twitterTrack",args=(words,))
    p.start()
    p.join(60)
    if p.is_alive():
        p.terminate()
        p.join()
