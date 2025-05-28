import os
import json
import datetime
import random

# 基本設定
logs_dir = "output/logs"
poems_dir = "output/poems"
os.makedirs(logs_dir, exist_ok=True)
os.makedirs(poems_dir, exist_ok=True)

# 今日の日付を取得
today = datetime.date.today()
date_str = today.strftime("%Y-%m-%d")

# タイトル候補（ランダムで選ばれる）
titles = [
    "笑う試供品",
    "津代志",
    "ロールケーキa.k.a断絶",
    "アンビエントマグロ",
    "祝祭コロッケ",
    "何も楽しくない"
]
title = random.choice(titles)

# 仮の詩本文（ここを生成詩に差し替える）
poem_text = f"""# {title}

今日はまだ終わっていない。
マグカップの底が透けて見えるのは
誰のせいだろう。

冷蔵庫の裏に住んでいたものたちが
黙って引っ越していく音を
聞いた気がした。

わたしは今でも、あのタイルの匂いが
正しかったと信じている。
"""

# 評価情報（仮のスコア／実際は生成結果に応じて更新）
evaluation = {
    "date": date_str,
    "title": title,
    "kz_score": random.randint(89, 100),  # 91以上だけがZINE対象
    "hx_score": {
        "EMO": random.randint(10, 20),
        "ETH": random.randint(10, 20),
        "DIS": random.randint(10, 20),
        "WET": random.randint(10, 20),
        "MIR": random.randint(10, 20)
    }
}

# logs に書き出し（本文と評価）
log_md_path = os.path.join(logs_dir, f"{date_str}.md")
log_json_path = os.path.join(logs_dir, f"{date_str}_eval.json")

with open(log_md_path, "w", encoding="utf-8") as f_md:
    f_md.write(poem_text)

with open(log_json_path, "w", encoding="utf-8") as f_json:
    json.dump(evaluation, f_json, ensure_ascii=False, indent=2)

# poems に本文だけを保存（ZINEやnote用）
poem_md_path = os.path.join(poems_dir, f"{date_str}.md")
with open(poem_md_path, "w", encoding="utf-8") as f_poem:
    f_poem.write(poem_text)

print(f"✅ 詩を生成・保存しました: {date_str}")
