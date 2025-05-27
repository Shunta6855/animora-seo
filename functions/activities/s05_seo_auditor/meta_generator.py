# ライブラリのインストール
import re
# ----------------------------------
# メタタグ(タイトル、ディスクリプション)の生成
# ----------------------------------
def gen_meta(outline: dict[str, str | list[str]], markdown: str) -> tuple[str, str]:
    """
    Generate the meta tags(title, description) from the outline and the first section.
    
    Args:
        outline: The outline of the article
        markdown: The markdown of the article

    Returns:
        The title and the description
    """
    title = str(outline.get("title", "")).strip()[:32]

    # Markdown を行単位で分割
    lines = markdown.strip().split("\n")

    # 導入文の探索: 最初の # タイトルの後に続く最初の段落を description に使う
    description = ""
    found_title = False
    for i, line in enumerate(lines):
        if line.startswith("#"):
            found_title = True
        elif found_title and line.strip():
            description = re.sub(r"\s+", " ", line.strip())[:120].rstrip() + "..."
            break

    print(f"Title: {title}")
    print(f"Description: {description}")
    return title, description