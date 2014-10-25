import json
from flask import Flask, Response
from Market import Market
from Operator import Operator
from AssetRequest import AssetRequest
from Util import Util
app = Flask(__name__)

config = json.loads(open('config.json', 'rb').read().decode('utf-8'))

@app.route("/apps/<appid>.apk")
def apps(appid):
    market = Market(config['email'], config['password'])
    market.login()

    operator = Operator(config['country'], config['operator'])
    request = AssetRequest(appid, market.token, config['device'], operator, config['devname'], config['sdklevel'])
    url, market_da = market.get_asset(request.encode())

    generator, size = Util.download_apk_stream(appid, url, market_da)
    return Response(response=generator, headers={'Content-Length': size})

if __name__ == "__main__":
    app.run(debug=True)
