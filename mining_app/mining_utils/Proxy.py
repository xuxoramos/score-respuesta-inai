import requests
from lxml.html import fromstring
from itertools import repeat
from numpy.random import randint


class ProxyList:
    def __init__(self, max_size: int = 100):
        self.build(max_size)

    def build(self, max_size: int):
        url = "https://free-proxy-list.net/"
        response = requests.get(url)
        parser = fromstring(response.text)
        proxy_list = set()
        for i in parser.xpath("//tbody/tr")[:max_size]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                # Grabbing IP and corresponding PORT
                proxy = ":".join(
                    [i.xpath(".//td[1]/text()")[0], i.xpath(".//td[2]/text()")[0]]
                )
                proxy_list.add(proxy)

        proxy_list = list(proxy_list)
        self.list = proxy_list
        self.n = len(proxy_list)

    def get(self):
        i = randint(low=0, high=self.n)
        p = f"http://{self.list[i]}"
        return i, {"http": p, "https": p}
