import json
import time
from pathlib import Path
import os
import numpy as np
import tweepy

import secrets

auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
api = tweepy.API(auth)
minimumMutualFollowers = 15


def loadfiles():
    my_file = Path("accounts.json")
    if my_file.is_file():
        json1_file = open('accounts.json')
        json1_str = json1_file.read()
        accounts = json.loads(json1_str)
    else:
        accounts = dict()
    myFriends = api.friends_ids()

    my_file = Path("checked.npy")
    if my_file.is_file():
        checkedFriends = np.load(open('checked.npy', 'rb'),allow_pickle=True)
        checkedFriends = np.ndarray.tolist(checkedFriends)
    else:
        checkedFriends = []
    return accounts, myFriends, checkedFriends


def run():
    timeBefore = time.time()
    accounts, myFriends, checkedFriends = loadfiles()
    print("checked friends: ", len(checkedFriends),
          "remaining: ", (len(myFriends) - len(checkedFriends)))
    try:
        mutes = api.mutes_ids()
        for followerID in myFriends:
            if followerID not in checkedFriends and followerID not in mutes:
                try:
                    friendsOfFriend = api.friends_ids(followerID, count=2000)

                except tweepy.TweepError:
                    print('sleeping for 15 mins')
                    # save the arrays
                    np.array(checkedFriends).dump(open('checked.npy', 'wb'))
                    print("checked accounts: ", len(checkedFriends),
                    "remaining: ", (len(myFriends) - len(checkedFriends)))

                    # wait for rate limit
                    time.sleep(60 * 15)
                    # try again
                    friendsOfFriend = api.friends_ids(followerID, count=2000)


                checkedFriends.append(followerID)
                print("your friend: ", followerID, " follows ",
                      len(friendsOfFriend), " people")
                for friendOfFriendID in friendsOfFriend:
                    account = str(friendOfFriendID)
                    if account in accounts:
                        accounts[account] += 1
                    else:
                        accounts[account] = 1
            else:
                continue
                # save the arrays
            np.array(checkedFriends).dump(open('checked.npy', 'wb'))
            with open('accounts.json', 'w') as fp:
                json.dump(accounts, fp)
    except Exception as e:
        np.array(checkedFriends).dump(open('checked.npy', 'wb'))
        print(str(e))
    saveaccounts(accounts, myFriends)
    timeAfter = time.time() - timeBefore
    print("total time taken: ", timeAfter / 60, " minutes")
    return True


def saveaccounts(accounts, myFriends):
    print("filtering accounts gathered")
    filteredAccounts = {k: v for k,
                        v in accounts.items() if v >= minimumMutualFollowers}
    # dict of user names instead of IDs
    addedUsernames = dict()
    print("transforming IDs into usernames")
    myUsername = secrets.username

    for account in filteredAccounts:
        try:
            # this could be vastly improved by using the lookup method (takes 100 accounts per call) but I don't have the
            # time
            user = api.get_user(account)
            username = user.screen_name
            bio = user.description
            avatar = user.profile_image_url
            followers = user.followers_count
            name = user.name
            following = user.friends_count
            print("ID: ", account, " user: ", username)
            if username == myUsername:
                continue
            else:
                addedUsernames[username] = {}
                addedUsernames[username]['id'] = account
                addedUsernames[username]['count'] = filteredAccounts[account]
                addedUsernames[username]['bio'] = bio
                addedUsernames[username]['avatar'] = avatar
                addedUsernames[username]['followers'] = followers
                addedUsernames[username]['name'] = name
                addedUsernames[username]['following'] = following
        except Exception as e:
            print(str(e))
            continue
        # sort by most mutual friends
    print("sorting accounts...")
    sortedAccounts = sorted(addedUsernames.items(),
                            key=lambda x: x[1]['count'], reverse=True)
    print("saving file..")
    with open('sortedAccounts.json', 'w') as fp:
        json.dump(sortedAccounts, fp)
    os.remove('accounts.json')
    os.remove('checked.npy')
    return True


while not run():
    run()
    time.sleep(15)
