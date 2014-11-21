import json
from flask import Flask, Response
from Market import Market
from Operator import Operator
from AssetRequest import AssetRequest
from Util import Util
app = Flask(__name__)
config = None

@app.route("/apps/<appid>.apk")
def apps(appid):
    global config, market, operator

    request = AssetRequest(appid, market.token, config['device'], operator, config['devname'], config['sdklevel'])
    url, market_da = market.get_asset(request.encode())

    generator, size = Util.download_apk_stream(appid, url, market_da)
    return Response(response=generator, headers={'Content-Length': size})

@app.route("/reload")
def reload():
    global config

    config = json.loads(open('config.json', 'rb').read().decode('utf-8'))

    return json.dumps(config)

if __name__ == "__main__":
    reload()

    market = Market(config['email'], config['password'])
    market.login()

    operator = Operator(config['country'], config['operator'])

    app.run(host='0.0.0.0', debug=True, use_reloader=False)
