import time
import timeit

import tweepy
import operator
import json
import numpy as np
from pathlib import Path

consumer_key = "CnGjnBXexjsAlx48a0MFC826O"
consumer_secret = "upAHjcZJt0ZnYQJAhtqxrh0Thl5pZyT2TEx6iTieKtWCaPCxUo"
access_token = "213291513-dqihUb8K4wZLqQRpfwi04SOUTxQlgm5pTZPZuOuC"
access_token_secret = "9Xitc5joaDCPtNzltC7iih4bosgLIR6elzhwfX9VLdWOr"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
previous=time.time()
totalP=time.time()
count=0
myFriends = api.friends_ids()
for followerID in myFriends:
     user = api.get_user(followerID)
     if user.friends_count<=1000: count+=1
     elapsed=time.time()-previous
     previous = time.time()
     print(elapsed)
print("total: ",(time.time()-totalP))
print("count: ",count)