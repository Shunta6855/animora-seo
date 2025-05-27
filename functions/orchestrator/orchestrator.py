# ---------------------------------------------------------------------------------  # 
# 　　　　          Durable Orchestrator: end-to-end article pipeline　　　         　 #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import azure.durable_functions as df
from pathlib import Path
import logging
from typing import Any, Generator
from function_app import app

# ----------------------------------------------------------------
# Logging
# ----------------------------------------------------------------
logger = logging.getLogger(__name__)


# ----------------------------------
# Orchestrator
# ----------------------------------
@app.orchestration_trigger(context_name="context")
def orchestrator(context: df.DurableOrchestrationContext) -> Generator[Any, Any, str]:
    """
    Orchestrator function for the article pipeline.

    Args:
        context: DurableOrchestrationContext

    Returns:
        str: The path to the published article
    """
    keyword: str = context.get_input()["keyword"]
    slug: str = context.get_input()["slug"]
    logger.info(f"[orchestrator] keyword:{keyword}")

    # 1. Google SERP
    _ = yield context.call_activity("ac_get_serp", keyword)

    # 2. Scrape articles (H2 chunks)
    titles, docs = yield context.call_activity("ac_scrape_articles", keyword)
    
    # 3. Upload chunks to Azure AI Search
    _ = yield context.call_activity("ac_upload_chunks", {
        "cache_path": str(Path("data/uploaded_ids") / f"{keyword}.json"),
        "titles": titles,
        "docs": docs,
    })

    # 4. Outline generation / validation
    outline = yield context.call_activity("ac_generate_outline", keyword)

    # 5. Draft generation (fan-out per H2)
    draft = yield context.call_activity("ac_generate_draft", {
        "keyword": keyword,
        "outline": outline,
        "title": outline["title"],
        "h2_list": outline["h2_list"],
    })

    # 6. Pick images
    images = yield context.call_activity("ac_pick_images", {
        "keyword": keyword,
        "max_images": 4,
    })

    # 7. SEO audit
    audited = yield context.call_activity("ac_audit_article", {
        "keyword": keyword,
        "markdown_text": draft,
        "outline": outline,
        "images": images,
    })
    
    # 8. Publish
    published_path = yield context.call_activity("ac_publish_article", {
        "slug": slug,
        "audited": audited,
    })

    return published_path


main = df.Orchestrator.create(orchestrator)

__all__ = ["app"]