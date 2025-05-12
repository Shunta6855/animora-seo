# ---------------------------------------------------------------------------------  # 
# 　　　　　　                  記事本文を生成するアクティビティ　　　                  　　　 #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import json, asyncio, backoff
from openai import AzureOpenAI
from functions.config.settings import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_KEY,
    OPENAI_DEPLOYMENT_NAME
)
from functions.config.prompts import GEN_DRAFT_PROMPT
from functions.activities.s03_draft_generator.search.client import top_chunks
from functions.activities.s03_draft_generator.guardrail.schema import Draft, SectionAll
from functions.activities.s03_draft_generator.guardrail.safety import safe_text
from functions.activities.s03_draft_generator.guardrail.grounding import grounded


# ----------------------------------
# GPT呼び出し
# ----------------------------------
client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    azure_deployment=OPENAI_DEPLOYMENT_NAME
)

# ----------------------------------
# 各セクションの本文生成
# ----------------------------------
async def generate_section(h2: str, keyword: str) -> dict:
    """
    Generate a section of an article based on a keyword and a context.

    Args:
        h2 (str): The heading of the section.
        keyword (str): The keyword to generate the section for.

    Returns:
        dict: The generated section.
    """
    chunks = top_chunks(f"{keyword} {h2}", k=5)
    context_blocks = [
        f"<doc id='{c['id']}' src='{c['url']}'>{c['content']}</doc>"
        for c in chunks
    ]
    messages = [
        GEN_DRAFT_PROMPT,
        {
            "role": "user",
            "content": (
                f"# Keyword: {keyword}\n"
                f"# Context: {context_blocks}\n"
                f"# H2: {h2}\n"
                "上記の情報をもとに、記事本文をJSON形式で生成してください"
            )
        }
    ]

    # 文章生成
    @backoff.on_exception(backoff.expo, Exception, max_tries=3)
    async def _call():
        resp = await client.chat.completions.create(
            messages=messages,
            model=OPENAI_DEPLOYMENT_NAME,
            temperature=0.7,
            response_format={"type": "json_object"},
        )
        return resp.choices[0].message.content
    
    raw_json = await _call()
    section = json.loads(raw_json)

    # ---- Guardrail 1: Schema ---- # 
    SectionAll(**section)

    # ---- Guardrail 2: Safety ---- # 
    if not safe_text(section["content"]):
        raise ValueError("Unsafe content detected")
    
    # ---- Guardrail 3: Grounding ---- # 
    if not grounded(section["content"], [c["content"] for c in chunks]):
        raise ValueError("Ungrounded content")
    
    return section
    
# ----------------------------------
# 記事本文の生成
# ----------------------------------
async def generate_draft(keyword: str, outline: list[str]) -> dict:
    """
    Generate a draft of an article based on a keyword and outline.

    Args:
        keyword (str): The keyword to generate the article for.
        outline (list[str]): The outline of the article.

    Returns:
        dict: The generated draft.
    """
    tasks = [generate_section(h2, keyword) for h2 in outline]
    sections = await asyncio.gather(*tasks)
    draft = {"title": outline[0], "sections": sections}

    # Final Guardrail: Schema
    Draft(**draft)

    return draft