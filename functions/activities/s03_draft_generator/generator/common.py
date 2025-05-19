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
        keyword (str): The keyword to search for.

    Returns:
        str: The concatenated string.
    """
    return "\n".join(
        f"<doc id='{c['id']}'><h2>{c['heading']}</h2>{c['content']}</doc>"
        for c in chunks
    )[:7_000]

