# ---------------------------------------------------------------------------------  # 
#                                   開発用メイン処理　　　　　　　                        #　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import os, json
from pathlib import Path
from activities.s03_draft_generator.generator.generate_outline import validate_outline
from activities.s03_draft_generator.generator.generate_draft import generate_intro, generate_draft


# ----------------------------------
# 開発用メイン処理
# ----------------------------------
if __name__ == "__main__":
    keyword = "ペットSNS"
    outline_file = Path("data/outlines") / f"{keyword}.json"
    draft_file = Path("data/drafts") / f"{keyword}.md"

    if outline_file.exists():
        print(f"Outline already exists: {outline_file}")
    else:
        print(f"Generating outline for keyword: {keyword}")
        outline = validate_outline(keyword)
        with open(outline_file, "w", encoding="utf-8") as f:
            json.dump(outline, f, ensure_ascii=False, indent=2)
    
    with open(outline_file, "r", encoding="utf-8") as f:
        outline = json.load(f)
    
    if draft_file.exists():
        print(f"Draft already exists: {draft_file}")
    else:
        print(f"Generating draft for keyword: {keyword}")
        intro = generate_intro(keyword, outline)
        draft = generate_draft(keyword, intro, outline["title"], outline["h2_list"])
        with open(draft_file, "w", encoding="utf-8") as f:
            f.write(draft)

        print(f"Draft saved to {draft_file}")