import json
import operator
import re
import tweepy
import os

import secrets

list_name = "code"

auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
myfriends = api.friends(count=200)
code_list = api.list_members("mohamed3on", list_name, count=5000)

locations = {}


def remove_least_followed_N_from_list(list, n=100):
    sorted_list = sorted(list, key=lambda x: x.followers_count)
    print("list size:", len(sorted_list))
    for user in sorted_list[:n]:
        print(
            f'removing user {user.name} and {user.followers_count} followers')
        api.remove_list_member(
            owner_screen_name='mohamed3on', slug=list_name, id=user.id)


def addlocations(thelist, locations):

    for member in thelist:
        location = member.location
        if location != '':
            fulllocation = "\'" + location + "\'"
            all_locations = re.split(', | / ( ) & +', location)
            if len(all_locations) > 1:
                all_locations.append(fulllocation)
            for l in all_locations:
                if l is None:
                    continue
                l = l.strip()
                if l in locations:
                    locations[l] += 1
                else:
                    locations[l] = 1

    return locations


locations = addlocations(code_list, locations)
locations = addlocations(myfriends, locations)

locations = {k: v for k, v in locations.items() if v >= locations['Egypt']}
mostcommon = sorted(locations.items(),
                    key=operator.itemgetter(1), reverse=True)
print(mostcommon)
with open('commonlocations.json', 'w') as fp:
    json.dump(mostcommon, fp)
os.system('code commonlocations.json')
# remove_least_followed_N_from_list(code_list, 500)
