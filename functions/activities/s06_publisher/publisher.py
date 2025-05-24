# ---------------------------------------------------------------------------------  # 
#            生成された記事を .mdx + 画像ファイルに変換し、PRを作成するアクティビティ           #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Sequence

from config.settings import BLOG_SAVE_DIR, IMAGE_SAVE_DIR

# ----------------------------------
# メインクラス
# ----------------------------------
class Publisher:

    def __init__(self) -> None:
        pass

    # ----------------------------------
    # エントリポイント
    # ----------------------------------
    def publish(self, audited: dict[str, object]) -> dict[str, str]:
        """
        Publish the article to the Astro directory.

        Args:
            audited: The audited article

        Returns:
            Information about the published article
        """
        slug = self._slugify(audited["meta"]["title"]) # ex: my-first-article
        mdx_path = self._materialize(audited, slug)
        self._upload_images(slug, audited["images"])
        return {
            "slug": slug,
            "mdx_path": str(mdx_path),
            "images": audited["images"],
        }
        

    # ----------------------------------
    # 記事を .mdx として Astro ディレクトリ配下に書き出す
    # ----------------------------------
    @staticmethod
    def _materialize(audited: dict[str, object], slug: str) -> Path:
        """
        Materialize the article into a .mdx file and save it to the Astro directory.

        Args:
            audited: The audited article
            slug: The slug of the article
        """
        front_matter = f'---\n'
        front_matter += f'title: "{audited["meta"]["title"]}"\n'
        front_matter += f'description: "{audited["meta"]["description"]}"\n'
        front_matter += f'pubDate: "{datetime.now().strftime("%Y-%m-%d")}"\n'
        front_matter += f'slug: "{slug}"\n'
        front_matter += f'---\n'

        mdx_body = audited["markdown"] + "\n"
        mdx_path = BLOG_SAVE_DIR / f"{slug}.mdx"
        mdx_path.write_text(front_matter + mdx_body, encoding="utf-8")

        return mdx_path
    

    # ----------------------------------
    # 画像を Blob -> Astro ディレクトリ配下に書き出す
    # ----------------------------------
    def _upload_images(self, slug: str, images: Sequence[dict[str, str]]) -> None:
        """
        Upload the images to the Astro directory.

        Args:
            slug: The slug of the article
            images: The images to upload
        """
        for img in images:
            name = Path(img["url"]).name.split("?")[0] or "image.png"
            img_path = IMAGE_SAVE_DIR / name
            raw = self._download_raw(img["url"])
            img_path.write_bytes(raw)
            img["url"] = f"/images/blog/{slug}/{name}"


    # ----------------------------------
    # Helper Functions
    # ----------------------------------
    @staticmethod
    def _slugify(title: str) -> str:
        return re.sub(r"[~\w\-]+", "-", title.lower()).strip("-")

    @staticmethod
    def _download_raw(url: str) -> bytes:
        import requests # lazy-import
        resp = requests.get(url, timeout=10)
        resp.raise_for_status() # HTTPリクエストが失敗していないか確認するためのメソッド
        return resp.content
