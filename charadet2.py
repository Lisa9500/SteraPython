from chardet.universaldetector import UniversalDetector
from urllib.request import urlopen

detector = UniversalDetector()

with urlopen('http://qiita.com/') as response:
    for l in response:
        detector.feed(l)
        if detector.done:
            break
detector.close()
print(detector.result)
