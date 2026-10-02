import urllib.request
import time
import sys

urls = [
    'http://127.0.0.1:8000/order.html',
    'http://127.0.0.1:8000/bootstrap.min.css',
    'http://127.0.0.1:8000/common.js',
    'http://127.0.0.1:8000/order.js',
]

time.sleep(1)
for url in urls:
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            print(f'{url} {response.status}')
    except Exception as exc:
        print(f'{url} ERROR {exc}')
        sys.exit(1)
