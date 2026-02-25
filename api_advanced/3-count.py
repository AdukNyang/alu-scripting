#!/usr/bin/python3
"""Module to recursively count keywords in Reddit hot articles"""
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """Recursively counts keywords in hot article titles"""
    if counts is None:
        counts = {}
        for word in word_list:
            counts[word.lower()] = 0

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "python:subreddit.count:v1.0"}
    params = {"after": after, "limit": 100}
    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)
    if response.status_code != 200:
        return

    data = response.json().get("data", {})
    posts = data.get("children", [])
    after = data.get("after")

    for post in posts:
        title = post.get("data", {}).get("title", "").lower().split()
        for word in counts.keys():
            counts[word] += title.count(word)

    if after:
        return count_words(subreddit, word_list, after, counts)

    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    for word, count in sorted_counts:
        if count > 0:
            print(f"{word}: {count}")
