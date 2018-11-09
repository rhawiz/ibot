import json

from instagram_private_api import Client
from instagram_web_api import Client as Cl

api = Client("world.of.jokes", "raw12743")

#
rank_token = api.generate_uuid()
# # api2 = Cl("hwzspace", "raw12743")
x = api.feed_tag("gcse", rank_token=rank_token)

print(json.dumps(x))

# print(api.feed_location("213385402"))

# print(api.media_likers("1908250564341439433"))
#
#
# api.post_photo()