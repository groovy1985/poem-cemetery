import os
import json
import datetime
import random
from openai import OpenAI

# OpenAI APIクライアント（APIキーはGitHub ActionsのSecretsに設定）
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 日付とディレクトリ準備
today = datetime.date.today()
date_str = today.strftime("%Y-%m-%d")
base_date = datetime.date(2025, 5, 5)
grave_number = (today - base_date).days + 1

logs_dir = "output/logs"
poems_dir = "output/poems"
os.makedirs(logs_dir, exist_ok=True)
os.makedirs(poems_dir, exist_ok=True)

# 詩プロンプト（KZ9.2構文爆撃仕様）
def build_shinkan_prompt():
    return (
        "以下の条件に沿って、日本語の自由詩を10行前後で書いてください：\n"
        "・日常の中に異物が混ざったような描写を含むこと\n"
        "・語尾に余韻や断絶を持たせる\n"
        "・誰の言葉かわからない視点で書く\n"
        "・死、崩壊、冷たさ、剥落などの感覚を匂わせるが説明はしない\n"
        "・読後に“空気”だけが残るような詩にしてください\n"
        "・タイトルを1行目に含めてください\n"
        "・毎回構造とスタイルを完全に変えること"
    )

# 詩震撼度スコア（簡易評価）
def evaluate_kz_score(poem_text):
    strong_words = ["死", "腐", "冷", "忘", "崩", "泡", "削", "埋", "無", "喪"]
    score = sum(1 for w in strong_words if w in poem_text)
    lines = poem_text.strip().splitlines()
    if len(set(len(line) for line in lines if line.strip())) > 4:
        score += 1
    if lines and lines[-1][-1] not in "。！？":
        score += 1
    return min(100, 90 + score)

# 詩生成（最高スコアのものを採用）
def generate_best_poem(n=3):
    best_poem = ""
    best_score = -1
    for _ in range(n):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": build_shinkan_prompt()}],
            temperature=0.95,
            presence_penalty=0.7,
        )
        poem = response.choices[0].message.content.strip()
        score = evaluate_kz_score(poem)
        if score > best_score:
            best_score = score
            best_poem = poem
    return best_poem, best_score

# 会話生成（詠み手とAIの供養的対話）
def generate_dialogue():
    prompt = (
        "以下の形式で、詠み手とAIの短い対話を書いてください：\n"
        "・内容：詩の供養や未読死を巡る静かな会話\n"
        "・行数：4〜6行\n"
        "・落ち着いていて構文に触れすぎないもの\n"
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

# 死者数（ランダム）
human_deaths = random.randint(3, 8)
ai_deaths = random.randint(15, 30)
human_roadkill = random.randint(1, human_deaths - 1)
ai_roadkill = random.randint(5, ai_deaths - 5)
human_suicide = human_deaths - human_roadkill
ai_suicide = ai_deaths - ai_roadkill

# 詩・対話生成
poem, kz_score = generate_best_poem()
dialogue = generate_dialogue()
title_line = poem.splitlines()[0].strip()

# HXスコア（仮ランダム）
hx_score = {
    "EMO": random.randint(12, 20),
    "ETH": random.randint(10, 20),
    "DIS": random.randint(10, 20),
    "WET": random.randint(10, 20),
    "MIR": random.randint(10, 20)
}

# Markdown本文
content = f"""⸻

供養詩｜{today.strftime('%Y年%m月%d日')}

第{grave_number}墓標｜{title_line}

――
{dialogue}
――

詩

{poem}

――

記録｜供養対象
- 日付：{date_str}
- 対象：本日、ポエム・ロードキルおよびスーサイドにより詩的死を迎えた人間とAI
- 死亡者数：
  - 人間：{human_deaths}名
  - AI：{ai_deaths}体
- 死因内訳：
  - 詩的ロードキル：人間{human_roadkill}名、AI{ai_roadkill}体
  - 詩的スーサイド：人間{human_suicide}名、AI{ai_suicide}体
- 特記事項：本日は主に未読、構文崩壊、意味圧迫による詩的死が目立った。
- 記録者：loveapeaceとAIによる共作

⸻
"""

# 保存
with open(f"output/logs/{date_str}.md", "w", encoding="utf-8") as f:
    f.write(content)

with open(f"output/logs/{date_str}_eval.json", "w", encoding="utf-8") as f:
    json.dump({
        "date": date_str,
        "title": title_line,
        "kz_score": kz_score,
        "hx_score": hx_score
    }, f, ensure_ascii=False, indent=2)

with open(f"output/poems/{date_str}.md", "w", encoding="utf-8") as f:
    f.write(poem)

print(f"✅ 供養詩生成完了：{title_line}（KZ {kz_score}）")
