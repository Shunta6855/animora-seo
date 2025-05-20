# ライブラリのインポート
import pytest, uuid
from unittest.mock import patch, MagicMock, mock_open
from bs4 import BeautifulSoup
from functions.activities.s01_web_crawler.scraper import ArticleScraper


# ----------------------------------
# テストケースの定義
# ----------------------------------
@patch("functions.activities.s01_web_crawler.scraper.uuid.uuid4", return_value=uuid.UUID("12345678123456781234567812345678"))
@patch("functions.activities.s01_web_crawler.scraper.webdriver.Chrome")
@patch("builtins.open", new_callable=mock_open, read_data='{"items":[{"title":"タイトル","link":"https://example.com"}]}')
@patch("json.load")
def test_scrape(mock_json_load, mock_open_fn, mock_webdriver, mock_uuid):
    html = """
    <html>
      <body>
        <h2>特徴</h2>
        <p>このアプリはペットとの相性が良いです。</p>
      </body>
    </html>
    """

    # モックの設定
    mock_driver_instance = MagicMock()
    mock_driver_instance.page_source = html # HTMLを直接与える
    mock_webdriver.return_value = mock_driver_instance
    mock_json_load.return_value = {
        "items": [
            {"title": "タイトル", "link": "https://example.com"}
        ]
    }
       # 返り値を固定
    
    # テスト対象の実行
    scraper = ArticleScraper()
    with patch.object(ArticleScraper, "_chunk_h2_sections", return_value=[("特徴", "このアプリはペットとの相性が良いです。")]):
        docs = scraper.scrape("ペットSNS")

    # テスト結果の検証
    assert isinstance(docs, list)
    assert len(docs) == 1
    doc = docs[0]
    assert doc["id"] == "12345678-1234-5678-1234-567812345678"
    assert doc["keyword"] == "ペットSNS"
    assert doc["url"] == "https://example.com"
    assert doc["title"] == "タイトル"
    assert doc["heading"] == "特徴"
    assert doc["content"] == "このアプリはペットとの相性が良いです。"

    mock_driver_instance.get.assert_called_once_with("https://example.com")
    mock_driver_instance.quit.assert_called_once()
      # WebDriverの get() と quit() が1回ずつ呼ばれたことを確認