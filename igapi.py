"""Instagram Graph API helpers (YOSHiKAWA CiTY FC)"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

GRAPH = "https://graph.facebook.com/v21.0"
EXPECTED_USERNAME = "yoshikawacity_fc"
VIDEO_EXT = (".mp4", ".mov")


def api(method, path, **params):
    params["access_token"] = os.environ["IG_ACCESS_TOKEN"]
    data = urllib.parse.urlencode(params).encode()
    if method == "GET":
        req = urllib.request.Request(f"{GRAPH}/{path}?{data.decode()}")
    else:
        req = urllib.request.Request(f"{GRAPH}/{path}", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        # トークンがログに出ないようにエラー本文だけ表示する
        sys.exit(f"Graph API エラー ({e.code}) {path}: {body}")


def wait_ready(container_id, timeout_sec=600):
    """動画など処理に時間がかかるメディアの準備完了を待つ"""
    start = time.time()
    while True:
        st = api("GET", container_id, fields="status_code,status")
        code = st.get("status_code")
        if code == "FINISHED":
            return
        if code in ("ERROR", "EXPIRED"):
            sys.exit(f"メディアの処理に失敗しました: {st}")
        if time.time() - start > timeout_sec:
            sys.exit("メディアの処理がタイムアウトしました")
        time.sleep(5)


def media_url(name):
    if name.startswith("http://") or name.startswith("https://"):
        return name
    base = os.environ["MEDIA_BASE_URL"].rstrip("/") + "/"
    return base + urllib.parse.quote(f"media/{name}")


def is_video(name):
    return name.lower().endswith(VIDEO_EXT)
