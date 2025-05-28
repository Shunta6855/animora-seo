# ---------------------------------------------------------------------------------  # 
#     Thin wrappers that adapt each class method to Durable Functions Activity.  　   #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import logging
import azure.durable_functions as df
from typing import List, Dict, Any
from function_app import app

# ----- s01: SERP ------------------------------------------------- #
from activities.s01_web_crawler.get_serp import GoogleSearcher
from activities.s01_web_crawler.scraper import ArticleScraper

# ----- s02: RAG indexer ----------------------------------------- #
from utils.azure import title_search_client, h2_search_client
from activities.s02_rag_indexer.create_rag_indexer import SearchUploader

# ----- s03: Draft Generator ------------------------------------ #
from activities.s03_draft_generator.generator.generate_outline import validate_outline
from activities.s03_draft_generator.generator.generate_draft import generate_intro, generate_draft

# ----- s04: Image Picker --------------------------------------- #
from activities.s04_image_picker.core import ImagePicker

# ----- s05: SEO Auditor ---------------------------------------- #
from activities.s05_seo_auditor.auditor import SEOAuditor

# ----- s06: Publisher ------------------------------------------ #
from activities.s06_publisher.publisher import Publisher

# ----------------------------------------------------------------
# Logging
# ----------------------------------------------------------------
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------
# Individual Activity Functions
# ----------------------------------------------------------------

@app.activity_trigger(input_name="keyword", activity="ac_get_serp")
def ac_get_serp(keyword: str) -> str:
    searcher = GoogleSearcher()
    response = searcher.fetch(keyword)
    logger.info(
        f"[ac_get_serp] totalResults={response['searchInformation']['totalResults']} "
        f"items={len(response.get('items',[]))}"
    )
    searcher.save(keyword, response)
    return response
    

@app.activity_trigger(input_name="keyword", activity="ac_scrape_articles")
def ac_scrape_articles(keyword: str) -> List[Dict[str, Any]]:
    scraper = ArticleScraper()
    titles, docs = scraper.scrape(keyword)
    logger.info(f"[ac_scrape_articles] type(docs)={type(docs)}, "
                f"len(docs)={len(docs) if hasattr(docs, '__len__') else 'n/a'}")
    if docs:
        logger.info(f"[ac_scrape_articles] docs:{docs}")

    return titles, docs


@app.activity_trigger(input_name="payload", activity="ac_upload_chunks")
def ac_upload_chunks(payload: Dict[str, Any]):
    title_uploader = SearchUploader(title_search_client, payload["cache_path"])
    title_uploader.upload_titles(payload["titles"])

    h2_uploader = SearchUploader(h2_search_client, payload["cache_path"])
    h2_uploader.upload_h2_docs(payload["docs"])
    h2_uploader.upload_animora_docs()


@app.activity_trigger(input_name="keyword", activity="ac_generate_outline")
def ac_generate_outline(keyword: str) -> dict:
    return validate_outline(keyword)
    

@app.activity_trigger(input_name="payload", activity="ac_generate_draft")
def ac_generate_draft(payload: Dict[str, Any]) -> Dict[str, Any]:
    intro = generate_intro(payload["keyword"], payload["outline"])
    return generate_draft(payload["keyword"], intro, payload["title"], payload["h2_list"])


@app.activity_trigger(input_name="payload", activity="ac_pick_images")
def ac_pick_images(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    picker = ImagePicker()
    return picker.pick_images(payload["keyword"], payload["max_images"])


@app.activity_trigger(input_name="payload", activity="ac_audit_article")
def ac_audit_article(payload: Dict[str, Any]) -> Dict[str, Any]:
    auditor = SEOAuditor(payload["keyword"])
    return auditor.audit(payload["markdown_text"], payload["outline"], payload["images"])


@app.activity_trigger(input_name="payload", activity="ac_publish_article")
def ac_publish_article(payload: Dict[str, Any]) -> Dict[str, Any]:
    publisher = Publisher(payload["slug"])
    return publisher.publish(payload["audited"])


__all__ = ["app"]