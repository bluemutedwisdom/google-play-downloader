from compat import urllib_parse_compat, urllib_request_compat
try:
    import pycurl
except ImportError:
    pass
import io


PYCURL_AVAILABLE = 'pycurl' in globals()

if PYCURL_AVAILABLE:
    proxy_auth_methods = {
        'basic': pycurl.HTTPAUTH_BASIC,
        'digest': pycurl.HTTPAUTH_DIGEST,
    }


default_proxy = (None, 'basic')


def set_default_proxy(proxy, auth_method='basic'):
    global default_proxy
    default_proxy = (proxy, auth_method)
    if not PYCURL_AVAILABLE and default_proxy is not None:
        raise Exception('Proxy are not supported without pycurl')
    print('Use proxy %s with %s authentication' % (proxy, auth_method))


def http_request(url, params):
    encoded_params = urllib_parse_compat.urlencode(params)

    if not PYCURL_AVAILABLE:
        connection = urllib_request_compat.urlopen(url, encoded_params.encode('utf-8'))
        data = connection.read()
        return data
    else:
        b = io.BytesIO()
        ch = pycurl.Curl()
        ch.setopt(pycurl.URL, url)
        ch.setopt(pycurl.POSTFIELDS, encoded_params)
        ch.setopt(pycurl.WRITEFUNCTION, b.write)

        if default_proxy[0] is not None:
            scheme, user, password, hostport = urllib_request_compat._parse_proxy(default_proxy[0])
            hostport = hostport.split(':')
            ch.setopt(pycurl.PROXY, hostport[0])
            if len(hostport) == 2:
                ch.setopt(pycurl.PROXYPORT, int(hostport[1]))
            ch.setopt(pycurl.PROXYUSERPWD, '%s:%s' % (user, password))
            ch.setopt(pycurl.PROXYAUTH, proxy_auth_methods[default_proxy[1]])

        ch.perform()

        return b.getvalue()
