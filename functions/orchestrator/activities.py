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
from utils.azure import h2_search_client
from activities.s02_rag_indexer.create_rag_indexer import SearchUploader

# ----- s03: Draft Generator ------------------------------------ #
from activities.s03_draft_generator.generator.generate_outline import validate_outline
from activities.s03_draft_generator.generator.generate_draft import generate_draft

# ----- s04: Image Picker --------------------------------------- #
from utils.azure import embedding_client, content_safety_client
from activities.s04_image_picker.obtain_picture import ImagePicker

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
    docs = scraper.scrape(keyword)
    logger.info(f"[ac_scrape_articles] type(docs)={type(docs)}, "
                f"len(docs)={len(docs) if hasattr(docs, '__len__') else 'n/a'}")
    if docs:
        logger.info(f"[ac_scrape_articles] docs:{docs}")

    return docs


@app.activity_trigger(input_name="docs", activity="ac_upload_chunks")
def ac_upload_chunks(docs: List[Dict[str, Any]]):
    uploader = SearchUploader(h2_search_client)
    uploader.upload_h2_docs(docs)
    uploader.upload_animora_docs()


@app.activity_trigger(input_name="keyword", activity="ac_generate_outline")
def ac_generate_outline(keyword: str) -> dict:
    return validate_outline(keyword)
    

@app.activity_trigger(input_name="payload", activity="ac_generate_draft")
def ac_generate_draft(payload: Dict[str, Any]) -> Dict[str, Any]:
    return generate_draft(payload["keyword"], payload["title"], payload["h2_list"])


@app.activity_trigger(input_name="payload", activity="ac_pick_images")
def ac_pick_images(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    picker = ImagePicker(embedding_client, content_safety_client)
    return picker.pick_images(payload["keyword"], payload["max_images"])


@app.activity_trigger(input_name="payload", activity="ac_audit_article")
def ac_audit_article(payload: Dict[str, Any]) -> Dict[str, Any]:
    auditor = SEOAuditor(payload["keyword"])
    return auditor.audit(payload["markdown"], payload["outline"], payload["images"])


@app.activity_trigger(input_name="audited", activity="ac_publish_article")
def ac_publish_article(audited: Dict[str, Any]) -> Dict[str, Any]:
    publisher = Publisher()
    return publisher.publish(audited)


__all__ = ["app"]