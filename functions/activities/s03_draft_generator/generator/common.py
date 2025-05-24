# ---------------------------------------------------------------------------------  # 
# 　　　　　　                 記事生成における共通アクティビティ 　　                  　　　 #
# ---------------------------------------------------------------------------------  #


# ----------------------------------
# AI Search からコンテキストを構築
# ----------------------------------
def build_context(chunks: list[dict]) -> str:
    """
    Concatenate the chunks into a single string and build context block.

    Args:
        chunks (list[dict]): The chunks to build the context from.

    Returns:
        str: The concatenated string.
    """
    return "\n".join(
        f"<doc id='{c['id']}'><h2>{c['heading']}</h2>{c['content']}</doc>"
        for c in chunks
    )[:7_000]

# ----------------------------------
# 記事の Markdown を生成する関数
# ----------------------------------
def draft_to_markdown(draft: dict) -> str:
    """
    Convert a draft dictionary to a markdown string.
    
    Args:
        draft (dict): The draft object with title and sections.

    Returns:
        str: Markdown-formatted article.
    """
    lines = [f"# {draft['title']}", ""]  # 大見出し（タイトル）

    for section in draft["sections"]:
        lines.append(f"## {section['h2']}")  # 中見出し（H2）
        lines.append("")  # 空行
        lines.append(section["content"])  # 本文
        lines.append("")  # 空行（次のセクションとの間）

    return "\n".join(lines)
