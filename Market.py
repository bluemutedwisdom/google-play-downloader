import re
import zlib
from http_request import http_request


class Market:
    LOGIN_PAGE = "https://android.clients.google.com/auth"
    LOGIN_SERVICE = "androidsecure"
    LOGIN_TYPE = "HOSTED_OR_GOOGLE"
    API_PAGE = "https://android.clients.google.com/market/api/ApiRequest"

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.token = None

    def login(self):
        params = {
            "Email": self.email,
            "Passwd": self.password,
            "service": self.LOGIN_SERVICE,
            "accountType": self.LOGIN_TYPE
        }

        data = http_request(self.LOGIN_PAGE, params)

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

        data = http_request(self.API_PAGE, params)

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
