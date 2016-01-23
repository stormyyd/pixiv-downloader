#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import re
import requests

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0"}
proxy = {}

class Pixiv_product():
    def __init__(self, url, session):
        self.url = url
        self.session = session
        r = self.session.get(url)
        self.source_code = r.text
        self.title = re.findall('(?<=<h1 class="title">).+?(?=</h1>(?:<p class="caption">|</section>))', self.source_code)[0]

    def get_images_url(self):
        manga_url = re.findall("member_illust\.php\?mode=manga&amp;illust_id=\d+", self.source_code)
        if len(manga_url) != 0:
            r = self.session.get("http://www.pixiv.net/" + manga_url[0])
            self.source_code = r.text
            images_thumb = re.findall("http://\w+?\.pixiv\.net/c/\d+x\d+/img-master/img/\d{4}/\d{2}/\d{2}/\d{2}/\d{2}/\d{2}/.+?(?:\.jpg|\.png|\.bmp|\.gif)", self.source_code)
            images_url = []
            for thumb_url in images_thumb:
                thumb_url = thumb_url.replace(re.findall("c/\d+x\d+/img-master", thumb_url)[0], "img-original")
                thumb_url = thumb_url.replace(re.findall("_master\d+", thumb_url)[0], "")
                images_url.append(thumb_url)
            return images_url
        images_url = re.findall("http://\w+?\.pixiv\.net/img-original/img/\d{4}/\d{2}/\d{2}/\d{2}/\d{2}/\d{2}/.+?(?:\.jpg|\.png|\.bmp|\.gif)", self.source_code)
        return images_url

class Pixiv_member():
    def __init__(self, url, session):
        self.url = url.replace("member.php", "member_illust.php")
        self.session = session
        r = self.session.get(self.url)
        self.numbers = int(re.findall('(?<=<span class="count-badge">)\d+(?=\w+?</span>)', r.text)[0])
        self.pages = math.ceil(self.numbers / 20)

    def get_product_url(self):
        product_url = []
        for i in range(1, self.pages + 1):
            url = self.url + "&type=all&p=%d" % i
            r = self.session.get(url)
            for pl in re.findall('(?<=<a href="/)member_illust\.php\?mode=medium&amp;illust_id=\d+(?=">)', r.text):
                pl = "http://www.pixiv.net/" + pl
                pl = pl.replace("&amp;", "&")
                product_url.append(pl)
        return product_url

def get_session(username, password):
    session = requests.Session()
    session.headers = headers
    session.proxies = proxy
    data = {
        "mode": "login",
        "pass": str(password),
        "pixiv_id": str(username),
        "skip": "1"
    }
    session.post(
        "https://www.secure.pixiv.net/login.php",
        data = data
    )
    return session
