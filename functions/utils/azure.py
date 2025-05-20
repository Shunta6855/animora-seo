# ライブラリのインポート
import asyncio, json, backoff
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.ai.contentsafety import ContentSafetyClient
from functions.config.settings import OPENAI_DEPLOYMENT_NAME
from functions.config.settings import (
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_ENDPOINT,
    TEXT_EMBEDDING_DEPLOYMENT_NAME,
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_KEY,
    H2_INDEX_NAME,
    AZURE_VISION_ENDPOINT,
    AZURE_VISION_KEY
)

# ----------------------------------
# クライアントの初期化
# ----------------------------------

gpt_client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=OPENAI_DEPLOYMENT_NAME
)

embedding_client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=TEXT_EMBEDDING_DEPLOYMENT_NAME
)

h2_search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=H2_INDEX_NAME,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)
)

content_safety_client = ContentSafetyClient(
    endpoint=AZURE_VISION_ENDPOINT,
    credential=AzureKeyCredential(AZURE_VISION_KEY)
)


# ----------------------------------
# GPT呼び出し関数
# ----------------------------------
# backoff: 例外が発生したときに自動でリトライするデコレータ
@backoff.on_exception(backoff.expo, Exception, max_tries=3)
async def call_gpt(messages: list, temperature: float) -> dict:
    """
    Call GPT with the given messages.

    Args:
        messages (list): The messages to call GPT with.

    Returns:
        dict: The response from GPT.
    """
    response = await gpt_client.chat.completions.create(
        model=OPENAI_DEPLOYMENT_NAME,
        messages=messages,
        temperature=temperature,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# ----------------------------------
# テキスト埋め込みベクトルを生成する関数
# ----------------------------------
async def embedding(text: str) -> list[float]:
    emb = await embedding_client.embeddings.create(
        model=TEXT_EMBEDDING_DEPLOYMENT_NAME,
        input=text
    )
    return emb.data[0].embedding # unit-normalized -> コサイン類似度において絶対値で割る必要がない