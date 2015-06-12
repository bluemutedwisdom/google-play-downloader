#!/usr/bin/python
#
# This file is part of GooglePlay Downloader.
#
# Copyright(c) 2012-2013 Simone Margaritelli aka evilsocket
# evilsocket@gmail.com
# http://www.evilsocket.net
#
# This file may be licensed under the terms of of the
# GNU General Public License Version 2 (the ``GPL'').
#
# Software distributed under the License is distributed
# on an ``AS IS'' basis, WITHOUT WARRANTY OF ANY KIND, either
# express or implied. See the GPL for the specific language
# governing rights and limitations.
#
# You should have received a copy of the GPL along with this
# program. If not, go to http://www.gnu.org/licenses/gpl.html
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
import traceback
import json
from ExtendedOptionParser import ExtendedOptionParser
from Market import Market
from OperatorModel import Operator
from AssetRequest import AssetRequest
from Util import Util
from http_request import set_default_proxy


def main():
        print("\n\tGooglePlay Downloader - Directly download apks from GooglePlay to your PC.\n" +
              "\tCopyleft Simone Margaritelli <evilsocket@evilsocket.net>\n" +
              "\thttp://www.evilsocket.net\n\n")

        defaults = {
            'email': None,
            'password': None,
            'package': None,
            'country': None,
            'operator': None,
            'device': None,
            'sdklevel': '19',
            'devname': 'hammerhead',
            'dry_run': False
        }

        usage = """usage: %prog [options]

EXAMPLE:
        %prog --email your-email@gmail.com --password your-password --name com.arttech.xbugsfree --country "Italy" --operator "3" --device your-device-id
"""
        parser = ExtendedOptionParser(defaults=defaults, usage=usage)

        parser.add_option_with_default("-e", "--email", action="store", dest="email", help="Your android account email.")
        parser.add_option_with_default("-p", "--password", action="store", dest="password", help="Your android account password.")
        parser.add_option_with_default("-n", "--name", action="store", dest="package", help="Package identifier (com.something.name).")
        parser.add_option_with_default("-c", "--country", action="store", dest="country", help="Your country.")
        parser.add_option_with_default("-o", "--operator", action="store", dest="operator", help="Your phone operator.")
        parser.add_option_with_default("-d", "--device", action="store", dest="device", help="Your device ID (can be obtained with this app https://play.google.com/store/apps/details?id=com.redphx.deviceid) .")
        parser.add_option_with_default("-s", "--sdklevel", action="store", dest="sdklevel", help="Android SDK API level (default is 19 like Android 4.4).")
        parser.add_option_with_default("-m", "--devname", action="store", dest="devname", help="Device name (default 'passion' like HTC Passion aka Google Nexus One.")
        parser.add_option_with_default("-t", "--dry-run", action="store_true", dest="dry_run", help="Test only, a.k.a. dry run")
        parser.add_option_with_default("--proxy", action="store", dest="proxy", default=None, help="Proxy server to use. Use the form user:pass@host:port")
        parser.add_option_with_default("--proxy-auth-digest", action="store_true", default=None, dest="proxy_auth_digest", help="Use digest authentication in proxies. Default is basic authentication")
        parser.add_option("-f", "--config", action="store", dest="config", default=None, help="Load additional settings from the specified config file. Parameters in this file always overwrite command line settings.")

        (o, args) = parser.parse_args()

        option_pool = {}

        for key in defaults:
            option_pool[key] = getattr(o, key)

        if o.config is not None:
            config = json.loads(open(o.config, 'rb').read().decode('utf-8'))
            for key in config:
                # in Python 2.x, json results are unicode
                option_pool[key] = str(config[key])

        if option_pool['email'] is None:
            print("No email specified.")

        elif option_pool['password'] is None:
            print("No password specified.")

        elif option_pool['package'] is None:
            print("No package specified.")

        elif option_pool['country'] is None or option_pool['country'] not in Operator.OPERATORS:
            print("Empty or invalid country specified, choose from: \n\n" + ", ".join(Operator.OPERATORS.keys()))

        elif option_pool['operator'] is None or option_pool['operator'] not in Operator.OPERATORS[option_pool['country']]:
            print("Empty or invalid operator specified, choose from: \n\n" + ", ".join(Operator.OPERATORS[option_pool['country']].keys()))

        elif option_pool['device'] is None:
            print("No device id specified.")

        elif int(option_pool['sdklevel']) < 2:
            print("The SDK API level cannot be less than 2.")

        else:
            if option_pool['proxy']:
                set_default_proxy(
                    option_pool['proxy'],
                    'digest' if option_pool['proxy_auth_digest'] else 'basic')
            print("@ Logging in ...")

            market = Market(option_pool['email'], option_pool['password'])
            market.login()

            print("@ Requesting package ...")

            operator = Operator(option_pool['country'], option_pool['operator'])

            request = AssetRequest(option_pool['package'], market.token, option_pool['device'], operator, option_pool['devname'], int(option_pool['sdklevel']))
            (url, market_da) = market.get_asset(request.encode())

            if not option_pool['dry_run']:
                print("@ Downloading...\n")

                Util.download_apk(option_pool['package'], url, market_da)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(traceback.format_exc())
