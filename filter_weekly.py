import os
import json
import datetime

# ディレクトリ設定
logs_dir = "output/logs"
poems_dir = "output/poems"
output_dir = "output/note"
today = datetime.date.today()
start_date = today - datetime.timedelta(days=7)

# 出力先ディレクトリ作成（noteまとめ保存）
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# ログディレクトリが存在しない場合はスキップ
if not os.path.exists(logs_dir):
    print(f"⚠️ ログディレクトリが見つかりませんでした: {logs_dir}")
    exit(0)

# 該当詩リスト
selected_poems = []

# ログファイルを走査
for fname in os.listdir(logs_dir):
    if not fname.endswith(".json"):
        continue

    path = os.path.join(logs_dir, fname)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"⚠️ ログ読み込み失敗: {fname} → {e}")
        continue

    # 日付・スコア判定
    try:
        date = datetime.date.fromisoformat(data["date"])
        if date < start_date:
            continue
        if data["kz_score"] < 91:
            continue
    except:
        continue

    # 詩本文（.md）取得
    poem_md_path = os.path.join(poems_dir, f"{date.strftime('%Y-%m-%d')}.md")
    if os.path.exists(poem_md_path):
        with open(poem_md_path, "r", encoding="utf-8") as f_md:
            poem_text = f_md.read()
        selected_poems.append((date, poem_text))

# ソート（新しい順）
selected_poems.sort(reverse=True)

# 出力Markdownを生成
if selected_poems:
    out_path = os.path.join(output_dir, f"note_{today.strftime('%Y-%m-%d')}.md")
    with open(out_path, "w", encoding="utf-8") as out_file:
        out_file.write("# 🕯️ 詩的供養週報｜構文国家\n\n")
        for date, poem in selected_poems:
            out_file.write(f"## 📅 {date.strftime('%Y年%m月%d日')}\n\n")
            out_file.write(poem)
            out_file.write("\n\n⸻\n\n")
    print(f"✅ noteまとめ生成完了：{out_path}")
else:
    print("⚠️ 該当詩なし（今週はKZ91以上の供養詩がありません）")
