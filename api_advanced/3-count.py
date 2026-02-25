#!/usr/bin/python3
"""Module to recursively count keywords in Reddit hot articles"""
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """Recursively counts keywords in hot article titles"""
    if counts is None:
        counts = {}
        for word in word_list:
            word_lower = word.lower()
            if word_lower in counts:
                counts[word_lower] += 0
            else:
                counts[word_lower] = 0

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"after": after, "limit": 100}
    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)
    if response.status_code != 200:
        return

    data = response.json().get("data", {})
    posts = data.get("children", [])
    after = data.get("after")

    for post in posts:
        title = post.get("data", {}).get("title", "").lower()
        words = title.split()
        for word in words:
            if word in counts:
                counts[word] += 1

    if after:
        return count_words(subreddit, word_list, after, counts)

    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    for word, count in sorted_counts:
        if count > 0:
            print("{}: {}".format(word, count))
