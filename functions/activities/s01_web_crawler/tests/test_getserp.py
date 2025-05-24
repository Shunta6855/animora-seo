# ライブラリのインポート
import pytest, json
from unittest.mock import patch, MagicMock
from activities.s01_web_crawler.get_serp import GoogleSearcher

# ----------------------------------
# テストケースの定義
# ----------------------------------
@patch("functions.activities.s01_web_crawler.get_serp.build")
def test_fetch(mock_build):
    # モックの準備
    mock_service = MagicMock()
    mock_cse = MagicMock()
    mock_list = MagicMock()
    mock_list.execute.return_value = {
        "items": [
            {"title": "記事タイトル", "link": "https://example.com/article1"},
            {"title": "記事タイトル2", "link": "https://example.com/article2"},
        ]
    }
    mock_cse.list.return_value = mock_list
    mock_service.cse.return_value = mock_cse
    mock_build.return_value = mock_service

    # テスト対象の実行
    searcher = GoogleSearcher()
    result = searcher.fetch("ペットSNS")

    # テスト結果の検証
    assert "items" in result
    assert result["items"][0]["title"] == "記事タイトル"
    assert result["items"][0]["link"] == "https://example.com/article1"
    assert result["items"][1]["title"] == "記事タイトル2"
    assert result["items"][1]["link"] == "https://example.com/article2"

def test_save(tmp_path):
    # ダミーレスポンス
    dummy_data = {
        "items": [
            {"title": "記事タイトル", "link": "https://example.com/article1"},
            {"title": "記事タイトル2", "link": "https://example.com/article2"},
        ]
    }

    # テスト対象の実行
    searcher = GoogleSearcher()
    save_path = searcher.save("ペットSNS", dummy_data)

    # テスト結果の検証
    assert save_path.exists()
    assert save_path.name == "ペットSNS_response.json"
    with open(save_path, "r", encoding="utf-8") as f:
        saved_data = json.load(f)
        assert saved_data == dummy_data




