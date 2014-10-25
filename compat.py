try:
    import httplib as httplib_compat
except:
    import http.client as httplib_compat

try:
    import urllib.parse as urllib_parse_compat
except:
    import urlparse as urllib_parse_compat

try:
    import urllib.request as urllib_request_compat
except:
    import urllib2 as urllib_request_compat
