#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Simple script to download emojis from emoji-cheat-sheet.com.
"""
import requests
import os
import sys

HOSTNAME = "https://api.github.com"
REPO = "/repos/arvida/emoji-cheat-sheet.com/contents/public/graphics/emojis"
FULL_URL = "{}{}".format(HOSTNAME, REPO)
DOWNLOAD_PATH = "flask_emoji/static/emoji/"


def download_image(url, name):
    full_path = "{}{}".format(DOWNLOAD_PATH, name)
    if not os.path.exists(os.path.abspath(DOWNLOAD_PATH)):
        print "%s does not exist." % os.path.abspath(DOWNLOAD_PATH)
        sys.exit(1)

    f = open(full_path, 'wb')
    f.write(requests.get(url).content)
    f.close()


def download():
    response = requests.get(FULL_URL)

    for image in response.json():
        download_image(url=image["download_url"], name=image["name"])


if __name__ == "__main__":
    download()
    print "Finished!"
