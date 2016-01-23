#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import getpass
import json
import os
import re
import sys
import time
import pixiv

def check_type(url):
    if len(re.findall("http://www\.pixiv\.net/member\.php\?id=\d+", url)) != 0:
        return "member"
    if len(re.findall("http://www\.pixiv\.net/member_illust\.php\?mode=medium&illust_id=\d+", url)) != 0:
        return "work"
    raise Exception("Unknown URL type.")

def config():
    if os.path.isfile("config.json"):
        with open("config.json") as f:
            data = json.loads(f.read())
        return data
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    data = {
        "username": username,
        "password": password
    }
    with open("config.json", "w") as f:
        f.write(json.dumps(data))
    return data

def download_product(url, session):
    p = pixiv.Pixiv_product(url, session)
    images_url = p.get_images_url()
    if not os.path.isdir(p.title):
        os.mkdir(p.title)
    url_file_name = base64.b64encode(str(time.time()).encode()).decode()
    with open(url_file_name, "a") as f:
        for i in images_url:
            f.write(i + "\n")
    cmd = 'wget -c' \
          ' -P "' + p.title + '"' \
          ' -i "' + url_file_name + '"' \
          ' --user-agent="User-Agent:Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0"' \
          ' --header="Referer: ' + url + '"'
    os.system(cmd)
    os.remove(url_file_name)

def main():
    url = sys.argv[1]
    data = config()
    session = pixiv.get_session(data["username"], data["password"])
    if check_type(url) == "member":
        p = pixiv.Pixiv_member(url, session)
        for i in p.get_product_url():
            try:
                download_product(i, session)
            except:
                session = pixiv.get_session(data["username"], data["password"])
                download_product(i, session)
        return
    download_product(url, session)

if __name__ == "__main__":
    main()
