"""
    A demo for search restaurants
"""

import pygourmet
import os

api = pygourmet.Api(keyid=os.environ.get("KEYID"))
results = api.get_restaurants(lat=35.170915, lng=136.8793482, radius=400)
for r in results:
    print(r["name"])
    print(r["address"])
    print(r["urls"]["pc"])
    print("\n")
