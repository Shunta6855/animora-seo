# ---------------------------------------------------------------------------------  # 
# 　　　　　　                 記事生成における共通アクティビティ 　　                  　　　 #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import asyncio, json, backoff
from functions.config.settings import OPENAI_DEPLOYMENT_NAME

# ----------------------------------
# GPT呼び出し関数
# ----------------------------------
# backoff: 例外が発生したときに自動でリトライするデコレータ
@backoff.on_exception(backoff.expo, Exception, max_tries=3)
async def call_gpt(client, messages: list, temperature: float) -> dict:
    """
    Call GPT with the given messages.

    Args:
        messages (list): The messages to call GPT with.

    Returns:
        dict: The response from GPT.
    """
    response = await client.chat.completions.create(
        model=OPENAI_DEPLOYMENT_NAME,
        messages=messages,
        temperature=temperature,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

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

