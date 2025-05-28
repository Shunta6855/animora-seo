# ---------------------------------------------------------------------------------  # 
# 　　　　　　                  記事構成を生成するアクティビティ　　　                  　　　 #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import json
from pathlib import Path
from pydantic import ValidationError
from config.prompts import GEN_CONSTRUCTION_PROMPT
from activities.s03_draft_generator.guardrail.schema import Outline
from activities.s03_draft_generator.generator.common import build_context
from activities.s03_draft_generator.search.client import top_title_chunks, top_h2_chunks
from utils.azure import call_gpt

# ----------------------------------
# 記事構成を生成する関数
# ----------------------------------
def generate_outline(keyword: str) -> dict:
    """
    Generate an outline for an article based on a keyword.
    
    Args:
        keyword (str): The keyword to search for.

    Returns:
        dict: The outline.
    """
    title_chunks = top_title_chunks(keyword)
    titles = [t["title"] for t in title_chunks]
    h2_chunks = top_h2_chunks(keyword)
    context = build_context(h2_chunks)
    messages = [
        GEN_CONSTRUCTION_PROMPT,
        {
            "role": "user", 
            "content": (
                f"# Titles: {json.dumps(titles, ensure_ascii=False)}\n"
                f"# Keyword: {keyword}\n"
                f"# Context: {context}\n"
                "上記の情報をもとに、記事本文をJSON形式で生成してください"
            ),
        },
    ]
    return call_gpt(messages, 0.3)


# ----------------------------------
# 記事構成を生成し、構文チェックを行う関数
# ----------------------------------
def validate_outline(keyword: str) -> dict:
    """
    Validate the outline of an article based on a keyword.
    Entry Point of Durable Functions Activity

    Args:
        keyword (str): The keyword to search for.

    Returns:
        dict: The outline.
    """
    outline_file = Path("data/outlines") / f"{keyword}.json"
    if outline_file.exists():
        print(f"Outline already exists: {outline_file}")
        print(f"Skipping ac_generate_outline process")
        with open(outline_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    for attempt in range(3): # 最大3回まで自力トライ
        draft = generate_outline(keyword) # GPT出力(dict形式)
        try:
            Outline(**draft) # 構文チェック
            with open(outline_file, "w", encoding="utf-8") as f:
                json.dump(draft, f, ensure_ascii=False, indent=2)
            return draft
        
        except ValidationError as e:
            err = e.errors()[0]["msg"]
            print(f"[validate_outline] attempt {attempt+1} failed: {err}")
            continue
    raise RuntimeError("Failed to generate a valid outline")