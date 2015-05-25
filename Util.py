import os.path
from compat import urllib_request_compat


class Util:
    def __init__(self):
        pass

    @staticmethod
    def download_apk(package, url, market_da):
        filename = "%s.apk" % package

        if os.path.exists(filename):
            print("File %s exists!" % filename)
            return

        with open(filename, 'wb') as f:
            req = Util._create_request(url, market_da)
            f.write(req.read())

    @staticmethod
    def download_apk_stream(package, url, market_da):
        req = Util._create_request(url, market_da)
        size = req.getheader('Content-Length')

        def generator():
            while True:
                data = req.read(1024)
                if not len(data):
                    break
                yield data
        return (generator(), size)

    @staticmethod
    def _create_request(url, market_da):
        opener = urllib_request_compat.build_opener(urllib_request_compat.HTTPRedirectHandler())
        opener.addheaders.append(('Cookie', 'MarketDA=%s' % market_da))
        return opener.open(url)
