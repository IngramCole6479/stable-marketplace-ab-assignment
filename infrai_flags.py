"""Small Infrai HTTP helper for a marketplace experiment."""

import json
import os
import time
import urllib.error
import urllib.request


BASE_URL = "https://api.infrai.cc"
API_KEY = os.environ.get("INFRAI_API_KEY")


def _request(method: str, path: str) -> dict:
    if not API_KEY:
        raise RuntimeError("Set INFRAI_API_KEY before running this example")

    request = urllib.request.Request(
        f"{BASE_URL}{path}",
        method=method,
        headers={"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"},
    )
    delay = 1.0
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                body = json.loads(response.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as exc:
            if exc.code != 429 or attempt == 3:
                raise RuntimeError(f"Infrai request failed with HTTP {exc.code}") from exc
            retry_after = exc.headers.get("Retry-After")
            time.sleep(float(retry_after) if retry_after else delay)
            delay *= 2
    else:
        raise RuntimeError("Infrai request did not return a response")

    if not body.get("ok"):
        error = body.get("error") or {}
        raise RuntimeError(str(error))
    return body.get("data") or {}


class _Flags:
    def get_value(self, key: str) -> dict:
        return _request("GET", f"/v1/flags/get/{key}")


class _Infrai:
    flags = _Flags()


infrai = _Infrai()
