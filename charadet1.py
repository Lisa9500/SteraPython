import chardet
from urllib.request import urlopen

with urlopen('http://qiita.com/') as response:
    html = response.read()
    print(chardet.detect(html))
