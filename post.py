#!/usr/bin/env python3
"""YOSHiKAWA CiTY FC Instagram 投稿スクリプト（posts/<ID>.json を @yoshikawacity_fc に投稿）"""
import json
import os
import sys
import time

from igapi import api, wait_ready, media_url, is_video, EXPECTED_USERNAME


def main():
    if len(sys.argv) != 2:
        sys.exit("使い方: python post.py <投稿ID>")
    post_id = sys.argv[1]
    with open(f"posts/{post_id}.json", encoding="utf-8") as f:
        post = json.load(f)

    caption = post["caption"]
    files = post["media"]
    if not files:
        sys.exit("media が空です")
    if len(files) > 10:
        sys.exit("1回の投稿は10枚までです")

    ig = os.environ["IG_USER_ID"]

    # 1) 投稿先アカウントの確認（安全装置）
    me = api("GET", ig, fields="username")
    if me.get("username") != EXPECTED_USERNAME:
        sys.exit(f"投稿先が {EXPECTED_USERNAME} ではありません（{me.get('username')}）。中止します。")
    print(f"投稿先: @{me['username']}")

    # 2) メディアコンテナ作成
    if len(files) == 1:
        name = files[0]
        if is_video(name):
            c = api("POST", f"{ig}/media", media_type="REELS",
                    video_url=media_url(name), caption=caption,
                    share_to_feed="true")
        else:
            c = api("POST", f"{ig}/media", image_url=media_url(name), caption=caption)
        creation_id = c["id"]
        wait_ready(creation_id)
    else:
        children = []
        for name in files:
            if is_video(name):
                c = api("POST", f"{ig}/media", media_type="VIDEO",
                        video_url=media_url(name), is_carousel_item="true")
            else:
                c = api("POST", f"{ig}/media", image_url=media_url(name),
                        is_carousel_item="true")
            wait_ready(c["id"])
            children.append(c["id"])
        c = api("POST", f"{ig}/media", media_type="CAROUSEL",
                children=",".join(children), caption=caption)
        creation_id = c["id"]
        wait_ready(creation_id)

    # 3) 公開
    pub = api("POST", f"{ig}/media_publish", creation_id=creation_id)
    media_id = pub["id"]
    info = api("GET", media_id, fields="permalink")
    permalink = info.get("permalink", "")
    print(f"投稿しました: {permalink}")

    # 結果を記録（ワークフローがコミットする）
    post["status"] = "posted"
    post["media_id"] = media_id
    post["permalink"] = permalink
    post["posted_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    with open(f"posts/{post_id}.json", "w", encoding="utf-8") as f:
        json.dump(post, f, ensure_ascii=False, indent=2)

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(f"### 投稿完了\n{permalink}\n")


if __name__ == "__main__":
    main()
