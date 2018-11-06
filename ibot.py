import json
import random
import sys
from time import sleep

from instagram_private_api import Client, ClientCompatPatch

from ids import USER_IDS


def follow(api, max=2000):
    c = 0
    while True:
        rank_token = api.generate_uuid(False)
        user_id = random.choice(USER_IDS)
        user_followers = api.user_followers(user_id=user_id, rank_token=rank_token)
        for user in user_followers["users"]:
            c += 1
            _id = user["pk"]
            wait = 1
            if not c % 100:
                print("100 follow requests sent, sleeping for 2.5 mins")
                sleep(180)
            while True:
                try:
                    resp = api.friendships_create(_id)
                    wait = 0
                    break

                except Exception as e:
                    print("Going to fast...sleeping {}".format(wait * 10))
                    sleep(wait * 10)
                    wait += 1
            print(c, "Following", resp)
            if c >= max:
                return
            sleep(random.randint(1, 4))


def get_all_followers(api):
    followers = []
    rank_token = api.generate_uuid(False)

    resp = api.user_followers(api.authenticated_user_id, rank_token=rank_token)

    followers += [x["pk"] for x in resp["users"]]

    while "next_max_id" in resp:
        max_id = resp["next_max_id"]
        resp = api.user_followers(api.authenticated_user_id, rank_token=rank_token, max_id=max_id)
        followers += [x["pk"] for x in resp["users"]]

    return followers


def unfollow(api, max=None):
    c = 0

    followers = get_all_followers(api)

    for id in followers:
        c += 1
        wait = 1
        if not c % 100:
            print("100 unfollow requests sent, sleeping for 2.5 mins")
            sleep(180)
        while True:
            try:
                resp = api.friendships_destroy(id)
                wait = 0
                break

            except Exception as e:
                print("Going to fast...sleeping {}".format(wait * 10))
                sleep(wait * 10)
                wait += 1

        print(c, "Unfollow", resp)
        if max and c >= max:
            return
        sleep(random.randint(1, 4))


def main():
    if len(sys.argv) >= 3:
        user_name = sys.argv[1]
        password = sys.argv[2]
    else:
        user_name = input("Username:")
        password = input("Password:")

    api = Client(user_name, password)

    while True:
        follow(api, 2000)
        unfollow(api)


if __name__ == "__main__":
    main()
