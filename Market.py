from compat import urllib_parse_compat, urllib_request_compat
import re
import zlib


class Market:
    LOGIN_PAGE = "https://www.google.com/accounts/ClientLogin"
    LOGIN_SERVICE = "androidsecure"
    LOGIN_TYPE = "HOSTED_OR_GOOGLE"
    API_PAGE = "https://android.clients.google.com/market/api/ApiRequest"

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.token = None
        self._opener = urllib_request_compat.build_opener()

    def _request(self, url, params):
        encoded_params = urllib_parse_compat.urlencode(params)
        connection = self._opener.open(url, encoded_params.encode('utf-8'))
        data = connection.read()
        return data

    def login(self):
        params = {
            "Email": self.email,
            "Passwd": self.password,
            "service": self.LOGIN_SERVICE,
            "accountType": self.LOGIN_TYPE
        }

        data = self._request(self.LOGIN_PAGE, params)

        response = str(data.decode('UTF-8'))

        if "Error" in response:
            raise Exception("Invalid login credentials.")

        for line in response.split("\n"):
            if "Auth=" in line:
                self.token = line.split("=")[1]

        if self.token is None:
            raise Exception("Unexpected response.")

    def get_asset(self, request):
        params = {
            "version": 2,
            "request": request
        }

        data = self._request(self.API_PAGE, params)

        decompressed = zlib.decompress(data, 16 + zlib.MAX_WBITS)

        dl_url = ""
        dl_cookie = ""

        match = re.search(b"(https?:\/\/[^:]+)", decompressed)

        if match is None:
            raise Exception("Unexpected response.")

        else:
            dl_url = match.group(1).decode('utf-8')

        match = re.search(b"MarketDA.*?(\d+)", decompressed)

        if match is None:
            raise Exception("Unexpected response.")

        else:
            dl_cookie = match.group(1).decode('utf-8')

        return (dl_url, dl_cookie)
