#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import getpass
import json
import math
import os
import pixivpy3

PIXIV_API = None

def login_data():
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
    work_data= [{"url": []}]
    json_data = PIXIV_API.works(work_id)
    work_data[0]["title"] = json_data["response"][0]["title"].replace(" ", "_")
    if json_data["response"][0]["is_manga"]:
        for i in json_data["response"][0]["metadata"]["pages"]:
            work_data[0]["url"].append(i["image_urls"]["large"])
        return work_data
    work_data[0]["url"].append(json_data["response"][0]["image_urls"]["large"])
    return work_data

def user(user_id):
    user_data= []
    json_user_info = PIXIV_API.users(user_id)
    works_num = json_user_info["response"][0]["stats"]["works"]
    for page in range(1, math.ceil(works_num / 30) + 1):
        json_works = PIXIV_API.users_works(user_id, page = page)
        for i in json_works["response"]:
            if i["is_manga"]:
                user_data.append(work(i["id"])[0])
                continue
            user_data.append({
                "title": i["title"].replace(" ", "_"),
                "url": [i["image_urls"]["large"]]
            })
    return user_data

def make_aria2_file(data, file_name = "aria2_url.txt"):
    aria2_content = "(url)\n" \
                    "  header=User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0\n" \
                    "  header=Referer: http://www.pixiv.net\n" \
                    "  continue=true\n" \
                    "  dir=(dir)\n"
    with open(file_name, "w") as f:
        for i in data:
            for u in i["url"]:
                f.write(aria2_content.replace("(url)", u).replace("(dir)", i["title"]))
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("id", help = "The ID of work or user.", nargs = "+", type = int)
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument("-w", "--work", help = "Set ID type to work.", action = "store_true")
    group.add_argument("-u", "--user", help = "Set ID type to user.", action = "store_true")
    args = parser.parse_args()
    global PIXIV_API
    data = login_data()
    PIXIV_API = pixivpy3.PixivAPI()
    PIXIV_API.login(data["username"], data["password"])
    if args.work:
        for i in args.id:
            make_aria2_file(work(i), "work_%d.aria2" % (i))
        return
    for i in args.id:
        make_aria2_file(user(i), "user_%d.aria2" % (i))

if __name__ == "__main__":
    main()
