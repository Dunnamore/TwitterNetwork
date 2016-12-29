import json
import operator
import time
from pathlib import Path
import numpy as np
import tweepy

import secrets

auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
done = False


def loadfiles():
    my_file = Path("accounts.json")
    if my_file.is_file():
        json1_file = open('accounts.json')
        json1_str = json1_file.read()
        accounts = json.loads(json1_str)
    else:
        accounts = dict()

    my_file = Path("friends.npy")
    if my_file.is_file():
        myFriends = np.load(open('friends.npy', 'rb'))
    else:
        myFriends = api.friends_ids()
        # noinspection PyTypeChecker
        np.array(myFriends).dump(open('friends.npy', 'wb'))
    my_file = Path("checked.npy")
    if my_file.is_file():
        checkedFriends = np.load(open('checked.npy', 'rb'))
        checkedFriends = np.ndarray.tolist(checkedFriends)
    else:
        checkedFriends = []
    return accounts, myFriends, checkedFriends


#@profile
def run():
    timeBefore = time.time()
    accounts, myFriends, checkedFriends = loadfiles()
    callsCount = 0
    print("checked friends: ", len(checkedFriends), "remaining: ", (len(myFriends) - len(checkedFriends)))
    try:
        for followerID in myFriends:
            if followerID not in checkedFriends:
                print("API calls= ", callsCount)
                # 15 is the threshold of calls every 15 minutes
                if callsCount % 15 == 0:
                    print("remaining friends: ", (len(myFriends) - len(checkedFriends)))
                checkedFriends.append(followerID)
                friendsOfFriend = api.friends_ids(followerID, count=2000)
                callsCount += 1
                print("your friend: ", followerID, " follows ", len(friendsOfFriend), " people")
                for friendOfFriendID in friendsOfFriend:
                    account = str(friendOfFriendID)
                    if account in accounts:
                        accounts[account] += 1
                    else:
                        accounts[account] = 1
                    print("\t friendOfFriend ", account, " is followed by ",
                          accounts[account], " friends")
            else:
                continue
                # save the arrays
            # noinspection PyTypeChecker
            np.array(checkedFriends).dump(open('checked.npy', 'wb'))
            with open('accounts.json', 'w') as fp:
                json.dump(accounts, fp)
    except Exception as e:
        print(str(e))
    myID = api.get_user(secrets.username).id
    filteredAccounts = {k: v for k, v in accounts.items() if v >= 10 and k != myID}
    # dict of user names instead of IDs
    addedUsernames = dict()
    for account in filteredAccounts:
        username = api.get_user(account).screen_name
        addedUsernames[username] = filteredAccounts[account]
    # sort by most mutual friends
    sortedAccounts = sorted(addedUsernames.items(), key=operator.itemgetter(1), reverse=True)
    with open('sortedAccounts.json', 'w') as fp:
        json.dump(sortedAccounts, fp)
    timeAfter = time.time() - timeBefore
    print("total time taken: ", timeAfter / 60, " minutes")
    return True


while not run():
    run()
    time.sleep(15)
