try:
    import httplib as httplib_compat
except:
    import http.client as httplib_compat

try:
    import urllib.parse as urllib_parse_compat
except:
    import urllib as urllib_parse_compat

try:
    import urllib.request as urllib_request_compat
except:
    import urllib2 as urllib_request_compat

try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer
