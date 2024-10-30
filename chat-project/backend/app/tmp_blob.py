import urllib.request as request

url = 'http://localhost:8888/e4324e1e-8ea2-4771-b41c-c800d9aff7b4'
# fake user agent of Safari
fake_useragent = 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25'
r = request.Request(url, headers={'User-Agent': fake_useragent})
f = request.urlopen(r)

# print or write
print(f.read())