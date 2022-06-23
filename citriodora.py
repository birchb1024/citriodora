
# sudo /usr/local/bin/pip3 --cert /etc/ssl/certs/tls-ca-bundle.pem install favicon

# $ CURL_CA_BUNDLE="" python36 citriodora.py <coles-sites.yaml  > foo.html


import os
import re
import sys
import yaml
import string

from pprint import pprint
from urllib.parse import urlparse

 # https://stackoverflow.com/questions/48391750/disable-python-requests-ssl-validation-for-an-imported-module

import favicon

parsed_yaml = yaml.load(sys.stdin, Loader=yaml.FullLoader)
print("<html><body>")
print("""<head>
<style>
body {background-color: powderblue;}
.item {
    /* To correctly align image, regardless of content height: */
    vertical-align: top;
    display: inline-block;
    /* To horizontally center images and caption */
    text-align: center;
    /* The width of the container also implies margin around the images. */
    width: 70px;
}
img {
    width: 50px;
    height: 50px;
    background-color: white;
}
.caption {
    display: block;
    word-wrap: break-word;
}
.dead {
    width: 50px;
    height: 50px;
    background-color: black;
}
</style>
</head>
""")

for obj in parsed_yaml:
    print([obj, type(obj)],file=sys.stderr)
    if type(obj) == dict:
        item = obj
    elif type(obj) == str:
        item = {'url': obj, 'name': obj}
    else:
        print("Error: unkown item in input file: {}".format(obj),file=sys.stderr)
        sys.exit(-1)

    u = urlparse(item['url'])
    if item['name'] == item['url']:
        item['name'] = u.hostname
    
    common = ['org', 'com', 'www', 'au', 'net', 'cmltd']
    nt = re.split('[\.:/]', item['name'])
    nn = [x for x in nt if not x in common]
#    item['name'] = string.capwords(' '.join(nn))
    item['name'] = ' '.join(nn)
    try:
        pprint(item, stream=sys.stderr)
        sys.stderr.flush()
        fi = favicon.get(item['url'])
        icon = fi[0].url
        for X in fi:
            if X.format == 'png':
                icon = X.url
                break
        for X in fi:
            if X.format == 'svg':
                icon = X.url
                break
        print('<div class="item"><a href="{}"><img src="{}" title="{}"></a><span class="caption">{}</span></div>'.format(item['url'], icon, item['url'], item['name']))
    except Exception as e:
        print(e, file=sys.stderr)
        print('<div class="item"><a href="{}"><img src="static.gif" title="{}"></a><span class="caption">{}</span></div>'.format(item['url'], item['url'], item['name']))
print("</body></html>")
