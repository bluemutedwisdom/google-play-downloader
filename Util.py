import os.path
import pycurl

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
            c = pycurl.Curl()
            c.setopt(pycurl.URL, url)
            c.setopt(pycurl.COOKIE, "MarketDA=%s" % market_da)
            c.setopt(pycurl.NOPROGRESS, 0)
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.setopt(pycurl.WRITEDATA, f)
            c.perform()
