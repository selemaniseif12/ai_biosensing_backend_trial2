import urllib.request
import urllib.error

base_url = "http://127.0.0.1:8000"
tests = [
    ("list", "/admin/tokens/list", "GET"),
    ("create", "/admin/tokens/create", "POST"),
    ("disable", "/admin/tokens/disable/test-token", "POST"),
    ("activate", "/admin/tokens/activate/test-token", "POST"),
    ("extend", "/admin/tokens/extend/test-token", "POST"),
]

for name, path, method in tests:
    request = urllib.request.Request(
        base_url + path,
        method=method,
    )

    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            print(f"{name}: HTTP {response.status}")
    except urllib.error.HTTPError as error:
        print(f"{name}: HTTP {error.code}")
    except Exception as error:
        print(f"{name}: {type(error).__name__}: {error}")
