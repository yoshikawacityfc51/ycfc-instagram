# ycfc-instagram

YOSHiKAWA CiTY FC（@yoshikawacity_fc）の Instagram 投稿用リポジトリ。

## 流れ
1. 稲葉さんが Claude に「この写真で〇〇の投稿を」と指示
2. Claude がキャプション・ハッシュタグを作り、プレビューを見せる
3. **稲葉さんの OK をもらってから**、Claude が `media/` に画像、`posts/<投稿ID>.json` を追加して push
4. Claude が「Instagramに投稿」ワークフローを `confirm=yes` で起動
5. 投稿後、メディアは `media/` から削除され、`posts/<投稿ID>.json` に投稿URLが記録される

## 投稿ファイルの形
```json
{
  "caption": "本文\n\n#吉川シティFC #ジュニアユース",
  "media": ["20261115_01.jpg", "20261115_02.jpg"]
}
```
- 画像1枚 / 複数枚（最大10枚、カルーセル）/ 動画1本（リール、.mp4）
- 画像は JPEG 推奨

## Secrets（Settings → Secrets and variables → Actions）
| 名前 | 内容 |
|---|---|
| `IG_ACCESS_TOKEN` | Yoshikawa City FC U-15 のページアクセストークン（期限なし） |
| `IG_USER_ID` | 17841453182297932 |

## 安全装置
- 手動起動のみ（自動・定期実行はしない）、`confirm=yes` が必要
- 投稿先のユーザー名が `yoshikawacity_fc` でなければ中止
