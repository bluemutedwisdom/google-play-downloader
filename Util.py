import os.path
from compat import urllib_request_compat


class Util:
    def __init__(self):
        pass

    @staticmethod
    def download_apk(package, url):
        filename = "%s.apk" % package

        if os.path.exists(filename):
            print("File %s exists!" % filename)
            return

        with open(filename, 'wb') as f:
            req = Util._create_request(url)
            f.write(req.read())

    @staticmethod
    def download_apk_stream(package, url):
        req = Util._create_request(url)
        size = req.getheader('Content-Length')

        def generator():
            while True:
                data = req.read(1024)
                if not len(data):
                    break
                yield data
        return (generator(), size)

    @staticmethod
    def _create_request(url):
        opener = urllib_request_compat.build_opener(urllib_request_compat.HTTPRedirectHandler())
        return opener.open(url)
