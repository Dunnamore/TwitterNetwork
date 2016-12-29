import time
import tweepy
import operator
import json
import numpy as np
import secrets
from pathlib import Path
auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
done=False
# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)
def network():
    my_file = Path("accounts.json")
    if my_file.is_file():
        json1_file = open('accounts.json')
        json1_str = json1_file.read()
        accounts = json.loads(json1_str)
    else:
        accounts = {}

    my_file = Path("friends.npy")
    if my_file.is_file():
        myFriends = np.load(open('friends.npy', 'rb'))
        print(len(myFriends))
    else:
        myFriends = api.friends_ids()
        np.array(myFriends).dump(open('friends.npy', 'wb'))
    my_file = Path("checked.npy")
    if my_file.is_file():
        checkedFriends = np.load(open('checked.npy', 'rb'))
        checkedFriends = np.ndarray.tolist(checkedFriends)
    else:
        checkedFriends = []
    friendsThreshold = 1000
    print (len(checkedFriends))
    try:
        for followerID in myFriends:
            if followerID not in checkedFriends:
                user = api.get_user(followerID)
                print("your friend: " + user.screen_name)
                if user.friends_count > friendsThreshold:
                    print("the friend follows more than ", friendsThreshold, "people")
                    checkedFriends.append(followerID)
                    np.array(checkedFriends).dump(open('checked.npy', 'wb'))
                    continue
                else:
                    checkedFriends.append(followerID)
                    friendsOfFriend = api.friends_ids(followerID)
                    for account in friendsOfFriend:
                        user = api.get_user(account)
                        name = user.screen_name
                        if not name in accounts:
                            accounts[name] = 1
                        else:
                            accounts[name] += 1
                        print("\t" + name + " is followed by ", accounts[name])
            else:
                print("the friend is already checked")
                continue
            np.array(checkedFriends).dump(open('checked.npy', 'wb'))
            with open('accounts.json', 'w') as fp:
                json.dump(accounts, fp)
    except:
        pass
    for name in accounts:
        if accounts[name] < 10: del accounts[name]
    sorted = sorted(accounts.items(), key=operator.itemgetter(1), reverse=True)
    with open('accounts.json', 'w') as fp:
        json.dump(sorted, fp)
    print(sorted)
    done=True
while not done:
    network()
    time.sleep(15)