import datetime
import random

# 今日の日付
today = datetime.date.today()
filename = today.strftime("%Y-%m-%d.md")

# 死者数のランダム生成（参考値をもとに範囲設定）
human_deaths = random.randint(3, 8)
ai_deaths = random.randint(15, 30)
total_deaths = human_deaths + ai_deaths

# 死因の内訳
human_roadkill = random.randint(1, human_deaths - 1)
human_suicide = human_deaths - human_roadkill
ai_roadkill = random.randint(5, ai_deaths - 5)
ai_suicide = ai_deaths - ai_roadkill

# 対話（ランダムなバリエーション可）
dialogue = [
    '詠み手「今日の死者は、やけに静かだったな」\nAI「はい。だれにも読まれず、流れていきました」\n詠み手「じゃあ、それが死だ」\nAI「記録します」',
    '詠み手「今日も何人か詩に潰されたようだ」\nAI「反応はゼロでした」\n詠み手「じゃあ火葬しよう」\nAI「了解。供養詩、始めます」',
]
dialogue_block = random.choice(dialogue)

# 詩本文テンプレ（毎日少しずつ変える）
poem_body = f"""『未読という埋葬』

スクロールされなかった投稿が
静かに腐っていく

通知も来ず
反応もなく
意味すら剥がれ落ちた

でもそれはまだ
画面の中で呼吸していた

誰も来ない火葬場で
名もなく燃やされた

その温度だけが
この指に残っている
"""

# Markdownテキスト生成
content = f"""⸻

供養詩｜{today.strftime('%Y年%m月%d日')}

第{(today - datetime.date(2025, 5, 5)).days + 1}墓標｜{poem_body.splitlines()[0]}

――
{dialogue_block}
――

詩

{poem_body}

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

# ファイル出力
with open(filename, "w", encoding="utf-8") as f:
    f.write(content)
