import time
import string
from collections import defaultdict

class URL:
    def __init__(self, id, long_url, short_url, expiry_time=None):
        self.id = id
        self.long_url = long_url
        self.short_url = short_url
        self.creation_time = time.time()
        self.expiry_time = expiry_time
        self.click_count = 0


class URLRepository:
    def __init__(self):
        self.id_counter = 0
        self.short_to_url = {}
        self.long_to_short = {}

    def get_next_id(self):
        self.id_counter += 1
        return self.id_counter

    def save(self, url_obj):
        self.short_to_url[url_obj.short_url] = url_obj
        self.long_to_short[url_obj.long_url] = url_obj.short_url

    def find_by_short_url(self, short_url):
        return self.short_to_url.get(short_url)

    def find_by_long_url(self, long_url):
        return self.long_to_short.get(long_url)


class Base62Encoder:
    BASE62 = string.digits + string.ascii_letters

    def encode(self, num):
        if num == 0:
            return self.BASE62[0]
        base62 = []
        while num > 0:
            base62.append(self.BASE62[num % 62])
            num //= 62
        return ''.join(reversed(base62))

    def decode(self, s):
        num = 0
        for char in s:
            num = num * 62 + self.BASE62.index(char)
        return num


class URLShortenerService:
    DOMAIN = "http://short.ly/"

    def __init__(self):
        self.repo = URLRepository()
        self.encoder = Base62Encoder()

    def shorten_url(self, long_url, expiry_secs=None):
        existing = self.repo.find_by_long_url(long_url)
        if existing:
            return self.DOMAIN + existing

        new_id = self.repo.get_next_id()
        short_key = self.encoder.encode(new_id)
        expiry_time = time.time() + expiry_secs if expiry_secs else None

        url_obj = URL(new_id, long_url, short_key, expiry_time)
        self.repo.save(url_obj)
        return self.DOMAIN + short_key

    def expand_url(self, short_url):
        short_key = short_url.replace(self.DOMAIN, "")
        url_obj = self.repo.find_by_short_url(short_key)
        if not url_obj:
            raise Exception("URL not found")

        if url_obj.expiry_time and time.time() > url_obj.expiry_time:
            raise Exception("URL expired")

        url_obj.click_count += 1
        return url_obj.long_url
