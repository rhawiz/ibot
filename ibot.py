import random
import sys
from time import sleep

from instagram_private_api import Client

from ids import USER_IDS


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


def follow(api, interval=1800, action_interval=4, rate=40, limit=2000):
    c = 0
    if not interval:
        interval = 1800
    if not action_interval:
        action_interval = 4
    if not rate:
        rate = 40
    if not limit:
        limit = 2000
    while True:
        rank_token = api.generate_uuid(False)
        user_id = random.choice(USER_IDS)
        user_followers = api.user_followers(user_id=user_id, rank_token=rank_token)
        for user in user_followers["users"]:
            c += 1
            _id = user["pk"]
            wait = 10
            if not c % rate:
                print("{} follow requests sent, sleeping for {} mins".format(rate, interval / 60))
                sleep(interval)
            while True:
                try:
                    resp = api.friendships_create(_id)
                    wait = 0
                    break

                except Exception as e:
                    print(e)
                    print("Going to fast...sleeping {} seconds".format(wait))
                    sleep(wait)
                    wait = wait * 2
            print(c, "Following", resp)
            if c >= limit:
                return

            sleep(action_interval + random.uniform(action_interval * -0.5, action_interval * 0.5))


def unfollow(api, interval=1800, action_interval=4, rate=40, limit=None):
    c = 0

    if not interval:
        interval = 1800
    if not action_interval:
        action_interval = 4
    if not rate:
        rate = 40

    followers = get_all_followers(api)

    for id in followers:
        c += 1
        wait = 10
        if not c % rate:
            print("{} unfollow requests sent, sleeping for {} mins".format(rate, interval / 60))
            sleep(interval)
        while True:
            try:
                resp = api.friendships_destroy(id)
                wait = 0
                break

            except Exception as e:
                print(e)
                print("Going to fast...sleeping {} seconds".format(wait))
                sleep(wait)
                wait = wait * 2

        print(c, "Unfollow", resp)
        if limit and c >= limit:
            return
        sleep(action_interval + random.uniform(action_interval * -0.5, action_interval * 0.5))


def main():
    if len(sys.argv) >= 3:
        user_name = sys.argv[1]
        password = sys.argv[2]
        wait_before_start = None
        interval = None
        action_interval = None
        rate = None
        if len(sys.argv) == 4:
            wait_before_start = int(sys.argv[3])
        if len(sys.argv) == 5:
            interval = int(sys.argv[4])
        if len(sys.argv) == 6:
            action_interval = int(sys.argv[5])
        if len(sys.argv) == 7:
            rate = int(sys.argv[6])

    else:
        user_name = input("Username:")
        password = input("Password:")
        wait_before_start = int(input("Time to wait before starting bot in seconds:"))
        interval = int(input("Interval in seconds (wait time between 40 requests):"))
        action_interval = int(input("Action Interval (wait time between each request):"))
        rate = int(input("Rate (amount of requests between each interval):"))

    print(">> Bot started. Waiting {} seconds before starting.".format(wait_before_start))
    sleep(wait_before_start)

    api = Client(user_name, password)
    print(">> Logged in with user '{}'".format(user_name))
    while True:
        follow(api, interval=interval, action_interval=action_interval, rate=rate, limit=2000)
        unfollow(api, interval=interval, action_interval=action_interval, rate=rate, limit=None)


if __name__ == "__main__":
    main()
