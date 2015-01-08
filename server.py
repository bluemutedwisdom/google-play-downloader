import sys
import json
import re
import traceback
from compat import HTTPServer, BaseHTTPRequestHandler
from Market import Market
from OperatorModel import Operator
from AssetRequest import AssetRequest
from Util import Util

config = None


class ApkServerHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.handlers = {
            '/apps/(.*).apk': self.apps
        }

        # __init__ ultimately calls do_GET
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def apps(self, appid):
        request = AssetRequest(appid, market.token, config['device'], operator, config['devname'], config['sdklevel'])
        try:
            url, market_da = market.get_asset(request.encode())
        except:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(traceback.format_exc().encode('utf-8'))
            return

        generator, size = Util.download_apk_stream(appid, url, market_da)

        self.send_response(200)
        self.send_header('Content-Length', size)
        self.end_headers()
        for data in generator:
            self.wfile.write(data)

    def do_GET(self):
        for pattern, handler in self.handlers.items():
            matches = re.match(pattern, self.path)
            if matches:
                handler(*matches.groups())
                return

        # No handler found
        self.send_response(404)
        self.end_headers()


if __name__ == "__main__":
    try:
        with open('config.json', 'rb') as f:
            config = json.loads(f.read().decode('utf-8'))
    except:
        print('Unable to load config file')
        sys.exit(1)

    market = Market(config['email'], config['password'])
    market.login()

    operator = Operator(config['country'], config['operator'])

    try:
        server = HTTPServer(('', 5000), ApkServerHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down the web server')
        server.socket.close()
