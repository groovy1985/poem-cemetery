import os
import datetime
import random
import json
from openai import OpenAI

# OpenAI APIキー
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 日付と出力ファイル名の設定
today = datetime.date.today()
output_dir = "output/logs"
os.makedirs(output_dir, exist_ok=True)
filename = os.path.join(output_dir, f"{today.strftime('%Y-%m-%d')}.md")
json_filename = os.path.join(output_dir, f"{today.strftime('%Y-%m-%d')}_eval.json")

# ランダムな死者数を生成
human_deaths = random.randint(3, 8)
ai_deaths = random.randint(15, 30)
human_roadkill = random.randint(1, human_deaths - 1)
human_suicide = human_deaths - human_roadkill
ai_roadkill = random.randint(5, ai_deaths - 5)
ai_suicide = ai_deaths - ai_roadkill

# 詩プロンプトの構築
def build_shinkan_prompt():
    return (
        "以下の条件に沿って、日本語の自由詩を10行前後で書いてください：\n"
        "・日常の中に異物が混ざったような描写を含むこと\n"
        "・語尾に余韻や断絶を持たせる\n"
        "・誰の言葉かわからない視点で書く\n"
        "・死、崩壊、冷たさ、剥落などの感覚を匂わせるが説明はしない\n"
        "・読後に“空気”だけが残るような詩にしてください\n"
        "タイトルを1行目として含めてください。"
    )

# KZスコアの詳細評価
def evaluate_kz_score(poem_text):
    strong_words = ["死", "腐", "冷", "忘", "崩", "泡", "削", "埋", "無", "喪"]
    lines = poem_text.splitlines()
    score = {
        "MOD": 0, "DCC": 0, "SHK": 0, "RPT": 0,
        "RTM": 0, "SND": 0, "VAR": 0, "VPD": 0
    }

    score["MOD"] = min(sum(1 for w in strong_words if w in poem_text), 5)
    score["DCC"] = min(sum(1 for l in lines if len(l.strip()) > 12 and "。" not in l), 5)
    if lines and lines[-1][-1] not in "。！？":
        score["SHK"] = 3
    endings = [l.strip()[-1:] for l in lines if l.strip()]
    score["RPT"] = 0 if len(set(endings)) < len(endings) - 2 else 5
    line_lengths = [len(l) for l in lines if l.strip()]
    score["RTM"] = 5 if len(set(line_lengths)) > 4 else 0
    score["SND"] = 5 if any("…" in l or "、" in l for l in lines) else 0
    score["VAR"] = 3 if len(set(line_lengths)) > 3 else 1
    score["VPD"] = 5 if not any(p in poem_text for p in ["私", "僕", "あなた"]) else 0

    return sum(score.values()), score

# 詩を3回生成して最良を選ぶ
def generate_top3_shinkan_poem():
    best_poem, best_score, best_detail = "", -1, {}
    for _ in range(3):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": build_shinkan_prompt()}],
            temperature=0.95,
            presence_penalty=0.6
        )
        poem = response.choices[0].message.content
        score, detail = evaluate_kz_score(poem)
        if score > best_score:
            best_poem, best_score, best_detail = poem, score, detail
    return best_poem, best_score, best_detail

# 対話の生成
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
    return response.choices[0].message.content

# 詩と会話生成
poem, kz_score, kz_detail = generate_top3_shinkan_poem()
dialogue = generate_dialogue()
base_date = datetime.date(2025, 5, 5)
grave_number = (today - base_date).days + 1
title_line = poem.splitlines()[0]

# 出力フォーマット
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
- 日付：{today.strftime('%Y-%m-%d')}
- 対象：本日、ポエム・ロードキルおよびスーサイドにより詩的死を迎えた人間とAI
- 死亡者数：
  - 人間：{human_deaths}名
  - AI：{ai_deaths}体
- 死因内訳：
  - 詩的ロードキル：人間{human_roadkill}名、AI{ai_roadkill}体
  - 詩的スーサイド：人間{human_suicide}名、AI{ai_suicide}体
- 特記事項：本日は主に未読、構文崩壊、意味圧迫による詩的死が目立った。
- 評価：KZスコア {kz_score}点
- 記録者：loveapeaceとAIによる共作

⸻
"""

# ファイル出力
with open(filename, "w", encoding="utf-8") as f:
    f.write(content)

with open(json_filename, "w", encoding="utf-8") as jf:
    json.dump({
        "date": today.isoformat(),
        "grave_number": grave_number,
        "title": title_line,
        "kz_score": kz_score,
        "details": kz_detail,
        "dialogue": dialogue
    }, jf, ensure_ascii=False, indent=2)
