import tweepy
import os
import json
import operator
import secrets


auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
auth.set_access_token(secrets.access_token, secrets.access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)


def get_most_liked_people():
    seen_ids = set()
    people = {}
    last_id = None
    while True:
        likes = api.get_favorites(count=200, max_id=last_id)

        if len(likes) == 1 or likes[1].id in seen_ids:
            break

        for x in likes:
            if x.id in seen_ids:
                continue

            user = x.user.screen_name
            if user in people:
                people[user] += 1
            else:
                people[user] = 1

            seen_ids.add(x.id)
            last_id = x.id

    people = {k: v for k, v in people.items() if v > 5}

    mostcommon = sorted(people.items(),
                        key=operator.itemgetter(1), reverse=True)

    with open('./most-liked-people.json', 'w') as fp:
        json.dump(mostcommon, fp)
    os.system('code ./most-liked-people.json')


get_most_liked_people()
