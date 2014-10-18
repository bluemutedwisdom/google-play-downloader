from compat import httplib_compat, urllib_compat
import re, zlib

class Market:
  LOGIN_HOST    = "www.google.com"
  LOGIN_PAGE    = "/accounts/ClientLogin"
  LOGIN_SERVICE = "androidsecure"
  LOGIN_TYPE    = "HOSTED_OR_GOOGLE"
  API_HOST      = "android.clients.google.com"
  API_PAGE      = "/market/api/ApiRequest"

  def __init__( self, email, password ):
    self.email    = email
    self.password = password
    self.token    = None

  def login( self ):
    params = urllib_compat.urlencode({
      "Email"       : self.email,
      "Passwd"      : self.password,
      "service"     : Market.LOGIN_SERVICE,
      "accountType" : Market.LOGIN_TYPE
    })

    headers = {"Content-type": "application/x-www-form-urlencoded"}

    connection = httplib_compat.HTTPSConnection( Market.LOGIN_HOST )

    connection.request("POST", Market.LOGIN_PAGE, params, headers )

    response = connection.getresponse().read()

    connection.close()

    if "Error" in response:
      raise Exception( "Invalid login credentials." )

    for line in response.split("\n"):
      if "Auth=" in line:
        self.token = line.split("=")[1]

    if self.token is None:
      raise Exception( "Unexpected response." )

  def get_asset( self, request ):
    params = urllib_compat.urlencode({
      "version" : 2,
      "request" : request
    })

    headers = {"Content-type": "application/x-www-form-urlencoded"}

    connection = httplib_compat.HTTPSConnection( Market.API_HOST )

    connection.request( "POST", Market.API_PAGE, params, headers )
    gzipped = connection.getresponse().read()

    connection.close()

    response = zlib.decompress( gzipped, 16 + zlib.MAX_WBITS )

    dl_url    = ""
    dl_cookie = ""

    match = re.search( "(https?:\/\/[^:]+)", response )

    if match is None:
      raise Exception( "Unexpected response." )

    else:
      dl_url = match.group(1)

    match = re.search( "MarketDA.*?(\d+)", response )

    if match is None:
      raise Exception( "Unexpected response." )

    else:
      dl_cookie = match.group(1)

    return dl_url + "#" + dl_cookie


