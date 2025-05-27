# ---------------------------------------------------------------------------------  # 
# 　　　　　　                  記事本文を生成するアクティビティ　　　                  　　　 #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import json
from config.prompts import GEN_INTRO_PROMPT, GEN_DRAFT_PROMPT
from activities.s03_draft_generator.search.client import top_h2_chunks
from activities.s03_draft_generator.guardrail.schema import Draft, SectionAll, Section
from activities.s03_draft_generator.guardrail.safety import safe_text
from activities.s03_draft_generator.guardrail.grounding import grounded
from activities.s03_draft_generator.generator.common import build_context, draft_to_markdown
from utils.azure import call_gpt


# ----------------------------------
# 各セクションの本文生成
# ----------------------------------
def generate_section(h2: str, h3_list: list[str], keyword: str) -> dict:
    """
    Generate a section of an article based on a keyword and a context.

    Args:
        h2 (str): The heading of the section.
        h3_list (list[str]): The list of subheadings for the section.
        keyword (str): The keyword to generate the section for.

    Returns:
        dict: The generated section.
    """
    chunks = top_h2_chunks(f"{keyword} {h2}")
    context = build_context(chunks)
    messages = [
        GEN_DRAFT_PROMPT,
        {
            "role": "user",
            "content": (
                f"# Keyword: {keyword}\n"
                f"# Context: {context}\n"
                f"# H2: {h2}\n"
                f"# H3_list: {json.dumps(h3_list, ensure_ascii=False)}\n"
                "上記の情報をもとに、記事本文をJSON形式で生成してください"
            )
        }
    ]

    # 文章生成
    section = call_gpt(messages, 0.7)

    # ---- Guardrail 1: Schema ---- # 
    SectionAll(**section)

    # ---- Guardrail 2: Safety ---- # 
    for content in section["content_list"]:
        if not safe_text(content):
            raise ValueError("Unsafe content detected")
    
    # # ---- Guardrail 3: Grounding ---- # 
    # if not grounded(section["content"], [c["content"] for c in chunks]):
    #     raise ValueError("Ungrounded content")
    
    return section

# ----------------------------------
# 導入文の生成
# ----------------------------------
def generate_intro(keyword: str, outline: dict) -> str:
    """
    Generate an introduction for an article based on a keyword and outline.

    Args:
        keyword (str): The keyword to generate the introduction for.
        outline (dict): The outline of the article.

    Returns:
        str: The generated introduction.
    """
    lines = [f"■ {outline['title']}"]  # 記事タイトルを最初に

    for section in outline["h2_list"]:
        lines.append(f"\n● {section['h2']}")
        for h3 in section["h3_list"]:
            lines.append(f"- {h3}")
    outline = "\n".join(lines)

    messages = [
        GEN_INTRO_PROMPT,
        {
            "role": "user",
            "content": (
                f"# Keyword: {keyword}\n"
                f"# Outline: {outline}\n\n"
                "上記の情報をもとに、導入文を生成してください"
            )
        }
    ]
    return call_gpt(messages, 0.7)["text"]
    
# ----------------------------------
# 記事本文の生成
# ----------------------------------
def generate_draft(keyword: str, intro: str, title: str, h2_list: list[Section]) -> dict:
    """
    Generate a draft of an article based on a keyword and outline.

    Args:
        keyword (str): The keyword to generate the article for.
        intro (str): The introduction of the article.
        title (str): The title of the article.
        h2_list (list[Section]): The list of sections for the article.

    Returns:
        str(markdown): The generated draft.
    """
    # dict -> Section オブジェクトに変換
    h2_list = [Section(**section_dict) for section_dict in h2_list]

    sections = []
    for section in h2_list:
        sec = generate_section(section.h2, section.h3_list, keyword)
        sections.append(sec)

    draft_dict = {"title": title, "h2_list": sections}
    print(f"Draft: {draft_dict}")

    # Final Guardrail: Schema
    Draft(**draft_dict)

    # Convert to Markdown
    draft = draft_to_markdown(draft_dict, intro)

    return draft