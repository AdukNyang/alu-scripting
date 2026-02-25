#!/usr/bin/python3
"""Module to query Reddit API for top 10 hot posts"""
import requests


def top_ten(subreddit):
    """Prints titles of first 10 hot posts for a given subreddit"""
    if subreddit is None or not isinstance(subreddit, str):
        print("None")
        return
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:1-top_ten:v1.0.0 (by /u/bdov_)"}
    params = {"limit": 10}
    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False, timeout=5)
        if response.status_code == 200:
            data = response.json()
            posts = data.get("data", {}).get("children", [])
            for post in posts:
                print(post.get("data", {}).get("title"))
        else:
            print("None")
    except Exception:
        print("None")
