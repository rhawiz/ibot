import json
import re
from http.cookiejar import Cookie
from urllib.parse import urlencode, quote, urlparse

import requests

session = requests.Session()

html = session.get("https://www.hotukdeals.com/").content.decode("utf-8")
# name="_token" value="8u2Q3kcYNMRwMXPaN45h0Zu4ne4LTuPobKkABh3p"
m = re.search("name=\"_token\" value=\"(?P<token>.*?)\"", html).groupdict()

token = m["token"]

payload = {
    "_token": token,
    "source": "generic_join_button_header",
    "keyword": "",
    "email": "111163524@gmail.com",
    "username": "winstonchurchhill99991",
    "password": "",
    "termsConditionsAndPrivacy": "on"
}

cookies = {c.name: c.value for c in session.cookies}
print(cookies)
cookie_str = "; ".join("%s=%s" % (c.name, c.value) for c in session.cookies)
# cookie_str = urlencode(cookies , quote_via=quote)
headers = {
    "cookie": cookie_str,
    "Host": "www.hotukdeals.com",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.hotukdeals.com/",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "TE": "Trailers"
}

payload_str = urlencode(payload)
# payload_str = cookie_str = "&".join("%s=%s" % (k, v) for k,v in payload.items())

# for c in session.cookies:
#     assert isinstance(c, Cookie)
#     print(c.name, c.value)
print(payload_str)
r = session.post("https://www.hotukdeals.com/register", params=payload_str, headers=headers)

print(r.content.decode("utf-8"))
