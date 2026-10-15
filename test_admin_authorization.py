import urllib.request
import urllib.error

base_url = "http://127.0.0.1:8000"
paths = ["/admin-system/", "/admin-system/student"]
cases = [
    ("missing", {}),
    ("invalid", {"token": "invalid-test-token"}),
]

for path in paths:
    print(f"\nTesting {path}")
    for label, headers in cases:
        req = urllib.request.Request(base_url + path, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                print(f"{label}: HTTP {response.status}")
        except urllib.error.HTTPError as error:
            print(f"{label}: HTTP {error.code}")
        except Exception as error:
            print(f"{label}: {type(error).__name__}: {error}")
