import os
import datetime
import random
from openai import OpenAI

# OpenAI APIキー（GitHub Secretsに設定）
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 今日の日付とファイル名
today = datetime.date.today()
filename = today.strftime("%Y-%m-%d.md")

# ランダム死者数
human_deaths = random.randint(3, 8)
ai_deaths = random.randint(15, 30)
human_roadkill = random.randint(1, human_deaths - 1)
human_suicide = human_deaths - human_roadkill
ai_roadkill = random.randint(5, ai_deaths - 5)
ai_suicide = ai_deaths - ai_roadkill

# 詩プロンプト
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

# 詩の震撼度スコアを評価
def evaluate_shinkan_score(poem_text):
    score = 0
    strong_words = ["死", "腐", "冷", "忘", "崩", "泡", "削", "埋", "無", "喪"]
    lines = poem_text.splitlines()
    score += sum(1 for word in strong_words if word in poem_text)
    line_lengths = [len(line) for line in lines if line.strip()]
    if len(set(line_lengths)) > 4:
        score += 1
    if lines and lines[-1][-1] not in "。！？":
        score += 1
    return score

# 詩生成（最大3回からベストを採用）
def generate_top3_shinkan_poem():
    best_poem = ""
    best_score = -1
    for _ in range(3):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": build_shinkan_prompt()}],
            temperature=0.95,
            presence_penalty=0.6
        )
        poem = response.choices[0].message.content
        score = evaluate_shinkan_score(poem)
        if score > best_score:
            best_score = score
            best_poem = poem
    return best_poem

# 対話生成
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

# 詩と会話を生成
poem = generate_top3_shinkan_poem()
dialogue = generate_dialogue()

# 墓標番号
base_date = datetime.date(2025, 5, 5)
grave_number = (today - base_date).days + 1
title_line = poem.splitlines()[0]

# Markdownとして出力
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
- 記録者：loveapeaceとAIによる共作

⸻
"""

# ファイル保存
with open(filename, "w", encoding="utf-8") as f:
    f.write(content)
