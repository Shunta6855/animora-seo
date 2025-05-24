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

    for h2 in draft["h2_list"]:
        lines.append(f"## {h2['h2']}")  # 中見出し（H2）
        lines.append("")  # 空行
        for h3, content in zip(h2["h3_list"], h2["content_list"]):
            lines.append(f"### {h3}")
            lines.append("")
            lines.append(content)
            lines.append("")
        lines.append("")  # セクション間の余白

    return "\n".join(lines)
