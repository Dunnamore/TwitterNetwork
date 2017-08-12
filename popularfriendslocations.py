import json
import operator

import tweepy

import secrets

auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
myfriends = api.friends(count=200)
locations = {}
for friend in myfriends:

    location = friend.location
    if location in locations:
        locations[location] += 1
    else:
        locations[location] = 1
locations = {k: v for k, v in locations.items() if v > 2 and k != ''}
mostcommon = sorted(locations.items(), key=operator.itemgetter(1), reverse=True)
print(mostcommon)
with open('commonlocations.json', 'w') as fp:
    json.dump(mostcommon, fp)
