from compat import httplib_compat, urllib_parse_compat
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
    params = urllib_parse_compat.urlencode({
      "Email"       : self.email,
      "Passwd"      : self.password,
      "service"     : Market.LOGIN_SERVICE,
      "accountType" : Market.LOGIN_TYPE
    })

    headers = {"Content-type": "application/x-www-form-urlencoded"}

    connection = httplib_compat.HTTPSConnection( Market.LOGIN_HOST )

    connection.request("POST", Market.LOGIN_PAGE, params, headers )

    response = str(connection.getresponse().read().decode('UTF-8'))

    connection.close()

    if "Error" in response:
      raise Exception( "Invalid login credentials." )

    for line in response.split("\n"):
      if "Auth=" in line:
        self.token = line.split("=")[1]

    if self.token is None:
      raise Exception( "Unexpected response." )

  def get_asset( self, request ):
    params = urllib_parse_compat.urlencode({
      "version" : 2,
      "request" : request
    })

    headers = {"Content-type": "application/x-www-form-urlencoded"}

    connection = httplib_compat.HTTPSConnection( Market.API_HOST )

    connection.request( "POST", Market.API_PAGE, params, headers )
    response = connection.getresponse()
    data = response.read()

    resp_code = response.status
    if resp_code != httplib_compat.OK:
        print(data.decode('utf-8'))
        raise Exception("%d %s" % (resp_code, httplib_compat.responses[resp_code]))

    connection.close()

    decompressed = zlib.decompress( data, 16 + zlib.MAX_WBITS )

    dl_url    = ""
    dl_cookie = ""

    match = re.search( b"(https?:\/\/[^:]+)", decompressed )

    if match is None:
      raise Exception( "Unexpected response." )

    else:
      dl_url = match.group(1).decode('utf-8')

    match = re.search( b"MarketDA.*?(\d+)", decompressed )

    if match is None:
      raise Exception( "Unexpected response." )

    else:
      dl_cookie = match.group(1).decode('utf-8')

    return (dl_url, dl_cookie)


