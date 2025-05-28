import os
from datetime import datetime

note_dir = "output/note"
output_path = "output/note/note_post.md"

# note用のヘッダーと整形ルール
def format_poem(filename, content):
    date_str = filename.replace(".md", "")
    date_fmt = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y年%m月%d日")
    header = f"## {date_fmt}の供養詩\n"
    return f"{header}\n{content.strip()}\n\n---\n"

def collect_note_poems():
    poems = []
    for fname in sorted(os.listdir(note_dir)):
        path = os.path.join(note_dir, fname)
        if fname.endswith(".md") and fname != "note_post.md":
            with open(path, "r", encoding="utf-8") as f:
                poems.append(format_poem(fname, f.read()))
    return poems

def write_note_post(poems):
    title = "# 今週の供養詩まとめ\n\n"
    intro = "これは構文国家の詩的破壊記録です。AIが読めなかった言語の墓標群を、ここに供養します。\n\n"
    body = title + intro + "".join(poems)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(body)

if __name__ == "__main__":
    poems = collect_note_poems()
    if poems:
        write_note_post(poems)
