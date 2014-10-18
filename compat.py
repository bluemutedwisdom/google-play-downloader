try:
    import httplib as httplib_compat
except:
    import http.client as httplib_compat

try:
    import urllib.request as urllib_compat
except:
    import urllib as urllib_compat
