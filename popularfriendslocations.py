import json
import operator
import re
import tweepy
import os
import webbrowser

import secrets

main_list_id = "815723390048866304"

auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
myfriends = api.friends(count=200)


def remove_least_followed_N_from_list( n=100):

    list = api.list_members(list_id=main_list_id, count=5000)

    sorted_list = sorted(list, key=lambda x: x.followers_count)
    print("list size:", len(sorted_list))
    for user in sorted_list[:n]:
        url = f'https://twitter.com/{user.screen_name}'
        webbrowser.open_new_tab(url)
        print(
            f'removing {user.name} @{user.screen_name} with {user.followers_count} followers')
        api.remove_list_member(
            list_id=main_list_id, id=user.id)


def addlocations(thelist, locations,mutes):

    for member in thelist:

        if member.id in mutes:
            continue

        location = member.location
        if location != '':
            fulllocation = "\'" + location + "\'"
            all_locations = re.split(r', | \/ | & | \+ | and |\|', location)
            if len(all_locations) > 1:
                all_locations.append(fulllocation)
            for l in all_locations:
                if l is None:
                    continue
                l = l.strip()

                if len(l)>3:
                    # if it's a full word, then standarise its case
                    l=l.lower().capitalize()
                    # else it's probably an abbreviation, so uppercase
                    # it
                else: l = l.upper()

                if l in locations:
                    locations[l] += 1
                else:
                    locations[l] = 1

    return locations


def get_popular_friends_locations():
    locations = {}

    main_list = api.list_members(list_id=main_list_id, count=5000)

    mutes = api.mutes_ids()

    locations = addlocations(main_list, locations,mutes)
    locations = addlocations(myfriends, locations,mutes)

    locations = {k: v for k, v in locations.items() if v > locations['Worldwide']}
    mostcommon = sorted(locations.items(),
                        key=operator.itemgetter(1), reverse=True)

    with open('./toplocations.json', 'w') as fp:
        json.dump(mostcommon, fp)
    os.system('code ./toplocations.json')



# remove_least_followed_N_from_list(5)


get_popular_friends_locations()
