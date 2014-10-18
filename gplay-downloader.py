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
import optparse
import traceback
from Market import Market
from Operator import Operator
from AssetRequest import AssetRequest
from Util import Util

def main():
    print( "\n\tGooglePlay Downloader - Directly download apks from GooglePlay to your PC.\n" +
               "\tCopyleft Simone Margaritelli <evilsocket@evilsocket.net>\n" +
               "\thttp://www.evilsocket.net\n\n" );

    parser = optparse.OptionParser( usage = "usage: %prog [options]\n\n" +
                                            "EXAMPLE:\n" +
                                            "\t%prog --email your-email@gmail.com --password your-password --name com.arttech.xbugsfree --country \"Italy\" --operator \"3\" --device your-device-id"
    )

    parser.add_option( "-e", "--email",    action="store",  dest="email",    default=None, help="Your android account email.")
    parser.add_option( "-p", "--password", action="store",  dest="password", default=None, help="Your android account password.")
    parser.add_option( "-n", "--name",     action="store",  dest="package",  default=None, help="Package identifier ( com.something.name ).")
    parser.add_option( "-c", "--country",  action="store",  dest="country",  default=None, help="Your country.")
    parser.add_option( "-o", "--operator", action="store",  dest="operator", default=None, help="Your phone operator.")
    parser.add_option( "-d", "--device",   action="store",  dest="device",   default=None, help="Your device ID ( can be obtained with this app https://play.google.com/store/apps/details?id=com.redphx.deviceid ) .")
    parser.add_option( "-s", "--sdklevel", action="store",  type="int", dest="sdklevel", default=9, help="Android SDK API level (default is 9 like Android 2.3.1).")
    parser.add_option( "-m", "--devname",  action="store",  dest="devname",  default="passion", help="Device name (default 'passion' like HTC Passion aka Google Nexus One.")

    (o,args) = parser.parse_args()

    if o.email is None:
      print("No email specified.")

    elif o.password is None:
      print("No password specified.")

    elif o.package is None:
      print("No package specified.")

    elif o.country is None or o.country not in Operator.OPERATORS:
      print("Empty or invalid country specified, choose from : \n\n" + ", ".join( Operator.OPERATORS.keys() ))

    elif o.operator is None or o.operator not in Operator.OPERATORS[ o.country ]:
      print("Empty or invalid operator specified, choose from : \n\n" + ", ".join( Operator.OPERATORS[ o.country ].keys() ))

    elif o.device is None:
      print("No device id specified.")

    elif o.sdklevel < 2:
      print("The SDK API level cannot be less than 2.")

    else:
      print("@ Logging in ...")

      market = Market( o.email, o.password )
      market.login()

      print("@ Requesting package ...")

      operator = Operator( o.country, o.operator )
      request  = AssetRequest( o.package, market.token, o.device, operator, o.devname, o.sdklevel )
      (url, market_da)    = market.get_asset( request.encode() )

      print("@ Downloading...\n")

      Util.download_apk(o.package, url, market_da)

if __name__ == '__main__':
  try:
    main()
  except Exception as e:
    print(traceback.format_exc())
