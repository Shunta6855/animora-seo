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
    first_section = next((s for s in markdown.split("\n\n") if s.strip()), "")
    description = re.sub(r"\s+", " ", first_section)[:120].rstrip() + "..."
    return title, description