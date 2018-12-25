# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import random, base64


# Start your middleware class
class ProxyMiddleware(object):

    def __init__(self):
        self.proxyList = [
            "http://114.235.22.120:9000"
        ]

    # overwrite process request
    def process_request(self, request, spider):
        proxy = random.choice(self.proxyList)
        request.meta['proxy'] = proxy

