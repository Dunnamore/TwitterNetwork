import tweepy
import os
import json
import operator
import secrets


auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_most_liked_people():
    people = {}
    for page in range(1,60):
        likes = api.favorites(page=page)
        for x in likes:
            user = x.user.screen_name
            if user in people:
                people[user] += 1
            else:
                people[user] = 1


    people = {k: v for k, v in people.items() if v > 5}

    mostcommon = sorted(people.items(),
                        key=operator.itemgetter(1), reverse=True)

    with open('./most-liked-people.json', 'w') as fp:
        json.dump(mostcommon, fp)
    os.system('code ./most-liked-people.json')

get_most_liked_people()
