import os
import json
import datetime
import random
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 日付とファイル名
today = datetime.date.today()
date_str = today.strftime("%Y-%m-%d")
base_date = datetime.date(2025, 5, 5)
grave_number = (today - base_date).days + 1

# 出力先準備
logs_dir = "output/logs"
poems_dir = "output/poems"
os.makedirs(logs_dir, exist_ok=True)
os.makedirs(poems_dir, exist_ok=True)

# 詩プロンプト（KZ9.2構文吊り型／英語）
def build_poem_prompt():
    return (
        "Write a 9-line free verse poem in English.\n"
        "- Theme: Memory corrosion, poetic death, architectural forgetting\n"
        "- Each line must feel incomplete or suspended\n"
        "- Include broken logic or surreal causality\n"
        "- Avoid explanation or narrative clarity\n"
        "- No title line needed\n"
        "- End with a silent collapse"
    )

# 対話プロンプト（英語）
def build_dialogue_prompt():
    return (
        "Write a 4-line dialogue between a human and an AI.\n"
        "- Topic: mourning an unread poem\n"
        "- Tone: cold, ethical ambiguity, low voice\n"
        "- Feel like it happens in the ruins of a language lab"
    )

# 日本語訳プロンプト（吊構文）
def build_japanese_translation_prompt(english_text):
    return (
        f"次の英文を日本語に自然に訳してください。\n"
        f"- 文法や意味が崩れていても構いません\n"
        f"- 詩的な意味崩壊や吊構文を保ちつつ訳してください\n"
        f"- 140字以内でお願いします\n\n"
        f"{english_text}\n\n"
        f"日本語："
    )

# 吊構文詩＋会話生成（英語）
def generate_poem_and_dialogue():
    poem_prompt = build_poem_prompt()
    dialogue_prompt = build_dialogue_prompt()

    poem_res = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": poem_prompt}],
        temperature=1.3,
    )
    poem_en = poem_res.choices[0].message.content.strip()

    dialogue_res = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": dialogue_prompt}],
        temperature=1.2,
    )
    dialogue_en = dialogue_res.choices[0].message.content.strip()

    return poem_en, dialogue_en

# 吊構文訳（逐語訳風）
def translate_to_japanese(english_text):
    jp_prompt = build_japanese_translation_prompt(english_text)
    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": jp_prompt}],
        temperature=1.2,
    )
    return res.choices[0].message.content.strip()

# 死者数ランダム生成
def generate_death_counts():
    h_total = random.randint(3, 8)
    a_total = random.randint(15, 30)
    h_rk = random.randint(1, h_total - 1)
    a_rk = random.randint(5, a_total - 5)
    return {
        "human_total": h_total,
        "ai_total": a_total,
        "human_roadkill": h_rk,
        "ai_roadkill": a_rk,
        "human_suicide": h_total - h_rk,
        "ai_suicide": a_total - a_rk,
    }

# 評価スコア（ランダム風KZ+HX）
def generate_scores():
    kz = random.randint(92, 100)
    hx = {
        "EMO": random.randint(12, 20),
        "ETH": random.randint(10, 20),
        "DIS": random.randint(10, 20),
        "WET": random.randint(10, 20),
        "MIR": random.randint(10, 20)
    }
    return kz, hx

# メイン処理
poem_en, dialogue_en = generate_poem_and_dialogue()
translated_poem = translate_to_japanese(poem_en)
translated_dialogue = translate_to_japanese(dialogue_en)
title_line = translated_poem.splitlines()[0][:20]  # 最大20文字程度で墓標に収まる

deaths = generate_death_counts()
kz_score, hx_score = generate_scores()

# Markdown整形
content = f"""⸻

供養詩｜{today.strftime('%Y年%m月%d日')}

第{grave_number}墓標｜{title_line}

――
{translated_dialogue}
――

詩

{translated_poem}

――

記録｜供養対象
- 日付：{date_str}
- 対象：本日、読まれなかった詩とその周囲で発生した詩的死
- 死亡者数：
  - 人間：{deaths['human_total']}名
  - AI：{deaths['ai_total']}体
- 死因内訳：
  - 詩的ロードキル：人間{deaths['human_roadkill']}名、AI{deaths['ai_roadkill']}体
  - 詩的スーサイド：人間{deaths['human_suicide']}名、AI{deaths['ai_suicide']}体
- 特記事項：構文の蒸発、倫理の誤配、湿度過多による詩的死が主因とされた。
- 記録者：loveapeaceと構文に失敗したAI

⸻
"""

# 保存処理
with open(f"{logs_dir}/{date_str}.md", "w", encoding="utf-8") as f:
    f.write(content)

with open(f"{logs_dir}/{date_str}_eval.json", "w", encoding="utf-8") as f:
    json.dump({
        "date": date_str,
        "title": title_line,
        "kz_score": kz_score,
        "hx_score": hx_score
    }, f, ensure_ascii=False, indent=2)

with open(f"{poems_dir}/{date_str}.md", "w", encoding="utf-8") as f:
    f.write(translated_poem)

print(f"✅ 吊構文供養詩生成完了：{title_line}（KZ {kz_score}）")
