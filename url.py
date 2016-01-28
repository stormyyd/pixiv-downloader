#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass
import json
import math
import os
import re
import sys
import pixivpy3

PIXIV_API = None

def config():
    if not os.path.isfile("config.json"):
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        data = {
            "username": str(username),
            "password": str(password)
        }
        with open("config.json", "w") as f:
            f.write(json.dumps(data))

    with open("config.json") as f:
        data = json.loads(f.read())
    return data

def work(work_id):
    json_data = PIXIV_API.works(work_id)
    if json_data["response"][0]["is_manga"]:
        with open("url.txt", "a") as f:
            for i in json_data["response"][0]["metadata"]["pages"]:
                f.write(i["image_urls"]["large"] + "\n")
        return
    with open("url.txt", "a") as f:
        f.write(json_data["response"][0]["image_urls"]["large"] + "\n")

def user(user_id):
    json_user_info = PIXIV_API.users(user_id)
    works_num = json_user_info["response"][0]["stats"]["works"]
    for page in range(1, math.ceil(works_num / 30) + 1):
        json_works = PIXIV_API.users_works(user_id, page = page)
        for i in json_works["response"]:
            if i["is_manga"]:
                work(i["id"])
                continue
            with open("url.txt", "a") as f:
                f.write(i["image_urls"]["large"] + "\n")

def main():
    global PIXIV_API
    data = config()
    PIXIV_API = pixivpy3.PixivAPI()
    PIXIV_API.login(data["username"], data["password"])
    if "illust_id" in sys.argv[1]:
        work(int(re.findall("(?<=illust_id=)\d+", sys.argv[1])[0]))
        return
    user(int(re.findall("(?<=member\.php\?id=)\d+", sys.argv[1])[0]))

if __name__ == "__main__":
    main()
