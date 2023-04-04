"""
    A demo for search restaurants
"""
import os

import pygourmet

api = pygourmet.Api(keyid=os.environ.get("KEYID"))
results = api.search(lat=35.170915, lng=136.8793482, radius=400, count=3)
for r in results:
    print(r["name"])
    print(r["catch"])
    print(r["address"])
    print(r["urls"]["pc"])
    print("\n")
