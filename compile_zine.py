import os
import json
import datetime

# ディレクトリ設定
logs_dir = "output/logs"
poems_dir = "output/poems"
output_dir = "output/zine"
today = datetime.date.today()
month_key = today.strftime("%Y-%m")

# 出力ディレクトリ作成
os.makedirs(output_dir, exist_ok=True)

# 該当詩の抽出
entries = []

for fname in os.listdir(logs_dir):
    if not fname.endswith(".json"):
        continue

    log_path = os.path.join(logs_dir, fname)
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        continue

    if not data["date"].startswith(month_key):
        continue

    if data["kz_score"] < 91:
        continue

    date_str = data["date"]
    poem_path = os.path.join(poems_dir, f"{date_str}.md")
    if os.path.exists(poem_path):
        with open(poem_path, "r", encoding="utf-8") as f_md:
            poem_text = f_md.read()
        entries.append((date_str, data["title"], poem_text))

# 出力
if entries:
    entries.sort()
    zine_path = os.path.join(output_dir, f"zine_{month_key}.md")
    with open(zine_path, "w", encoding="utf-8") as zf:
        # 表紙
        zf.write(f"# 🌀 構文国家詩集ZINE｜{month_key}\n\n")
        zf.write(f"## 収録数：{len(entries)} 詩（KZ91点以上のみ）\n\n")
        zf.write("## 📚 目次\n\n")
        for i, (date_str, title, _) in enumerate(entries, 1):
            zf.write(f"{i}. [{date_str}｜{title}](#{date_str.replace('-', '')})\n")
        zf.write("\n⸻\n\n")

        # 本文
        for i, (date_str, title, poem) in enumerate(entries, 1):
            anchor = date_str.replace("-", "")
            zf.write(f"## {i}. {date_str}｜{title}\n")
            zf.write(f"<a name=\"{anchor}\"></a>\n\n")
            zf.write(poem)
            zf.write("\n\n⸻\n\n")

    print(f"✅ ZINE生成完了：{zine_path}")
else:
    print("⚠️ 今月はKZ91点以上の詩が存在しないため、ZINEは生成されませんでした。")
