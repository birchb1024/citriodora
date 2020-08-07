
import sys
import yaml
import favicon

from pprint import pprint


parsed_yaml = yaml.load(sys.stdin, Loader=yaml.FullLoader)
print("<html><body>")
for url in parsed_yaml:
    try:
        fi = favicon.get(url)
        icon = fi[0].url
        for X in fi:
            if X.format == 'png':
                icon = X.url
                break
        for X in fi:
            if X.format == 'svg':
                icon = X.url
                break
        print('<a href="{}"><img src="{}" width="100px" title="{}"></a>'.format(url, icon, url))
    except Exception as e:
        print('<a href="{}">{}</a>'.format(url, url))
print("</body></html>")
