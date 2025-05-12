# ---------------------------------------------------------------------------------  # 
# 　　　　　　                  記事構成を生成するアクティビティ　　　                  　　　 #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import asyncio
from openai import AzureOpenAI
from functions.config.settings import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_KEY,
    OPENAI_DEPLOYMENT_NAME
)
from pydantic import ValidationError
from functions.config.prompts import GEN_CONSTRUCTION_PROMPT
from functions.activities.s03_draft_generator.guardrail.schema import Outline
from functions.activities.s03_draft_generator.generator.common import build_context, call_gpt
from functions.activities.s03_draft_generator.search.client import top_chunks

# ----------------------------------
# GPTクライアントの初期化
# ----------------------------------
client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=OPENAI_DEPLOYMENT_NAME
)

# ----------------------------------
# 記事構成を生成
# ----------------------------------
async def generate_outline(keyword: str) -> dict:
    """
    Generate an outline for an article based on a keyword.
    
    Args:
        keyword (str): The keyword to search for.

    Returns:
        dict: The outline.
    """
    chunks = top_chunks(keyword)
    context = build_context(chunks)
    messages = [
        GEN_CONSTRUCTION_PROMPT,
        {
            "role": "user", 
            "content": (
                f"# Keyword: {keyword}\n"
                f"# Context: {context}\n"
                "上記の情報をもとに、記事本文をJSON形式で生成してください"
            ),
        },
    ]
    return await call_gpt(client, messages, 0.3)


# ----------------------------------
# 記事構成を生成し、構文チェックを行う関数
# ----------------------------------
async def validate_outline(keyword: str) -> dict:
    """
    Validate the outline of an article based on a keyword.
    Entry Point of Durable Functions Activity

    Args:
        keyword (str): The keyword to search for.

    Returns:
        dict: The outline.
    """
    for attempt in range(3): # 最大3回まで自力トライ
        draft = await generate_outline(keyword) # GPT出力(dict形式)
        try:
            Outline(**draft) # 構文チェック
            return draft
        except ValidationError as e:
            err = e.errors()[0]["msg"]
            print(f"[validate_outline] attempt {attempt+1} failed: {err}")
            continue
    raise RuntimeError("Failed to generate a valid outline")