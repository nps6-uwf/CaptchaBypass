# Author: NS
# Testing the captcha solver service.
# send one off get requests to test the captcha service.

from requests import get

threshold = 0
fname = "image_0"
rmFile = 0
URL = f"http://127.0.0.1:5000/{fname}/{threshold}/{rmFile}"

r = get(URL)
print(r.text)