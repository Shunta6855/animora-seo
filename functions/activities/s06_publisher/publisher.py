# ---------------------------------------------------------------------------------  # 
#            生成された記事を .mdx + 画像ファイルに変換し、PRを作成するアクティビティ           #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
from __future__ import annotations

from PIL import Image
from io import BytesIO
from datetime import datetime
from pathlib import Path
from typing import Sequence

from config.settings import BLOG_SAVE_DIR, IMAGE_SAVE_DIR

# ----------------------------------
# メインクラス
# ----------------------------------
class Publisher:

    def __init__(self, slug: str) -> None:
        self.slug = slug

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
        mdx_path = self._materialize(audited)
        self._upload_images(audited["images"])
        return {
            "slug": self.slug,
            "mdx_path": str(mdx_path),
            "images": audited["images"],
        }
        

    # ----------------------------------
    # 記事を .mdx として Astro ディレクトリ配下に書き出す
    # ----------------------------------
    def _materialize(self, audited: dict[str, object]) -> Path:
        """
        Materialize the article into a .mdx file and save it to the Astro directory.

        Args:
            audited: The audited article
        """
        cover_img = Path(audited["images"][0]["url"]).name.split("?")[0]
        front_matter = f'---\n'
        front_matter += f'title: "{audited["meta"]["title"]}"\n'
        front_matter += f'description: "{audited["meta"]["description"]}"\n'
        front_matter += f'pubDate: {datetime.now().strftime("%Y-%m-%d")}\n'
        front_matter += f'slug: "{self.slug}"\n'
        front_matter += f'img: "/images/blog/{self.slug}/{cover_img}.jpeg"\n'
        front_matter += f'---\n'

        mdx_body = self._embed_images(audited["markdown"], audited["images"]) + "\n"
        mdx_path = BLOG_SAVE_DIR / f"{self.slug}.mdx"
        mdx_path.write_text(front_matter + mdx_body, encoding="utf-8")

        return mdx_path
    

    # ----------------------------------
    # 画像を Blob -> Astro ディレクトリ配下に書き出す
    # ----------------------------------
    def _upload_images(self, images: Sequence[dict[str, str]]) -> None:
        """
        Upload the images to the Astro directory.

        Args:
            slug: The slug of the article
            images: The images to upload
        """
        for img in images:
            name = Path(img["url"]).name.split("?")[0] or "image.png"

            image_dir = IMAGE_SAVE_DIR / self.slug
            image_dir.mkdir(parents=True, exist_ok=True)

            raw = self._download_raw(img["url"])
            image = Image.open(BytesIO(raw)).convert("RGB")
            
            jpeg_path = image_dir / f"{name}.jpeg"
            image.save(jpeg_path, "JPEG", quality=85)
            img["url"] = f"/images/blog/{self.slug}/{name}.jpeg"

    # ----------------------------------
    # 画像を記事 .mdx に埋め込む
    # ----------------------------------
    def _embed_images(self, markdown: str, images: Sequence[dict[str, str]]) -> str:
        """
        Embed the images into the markdown.
        """
        lines = markdown.splitlines()
        new_lines = []
        image_index = 1

        for line in lines:
            new_lines.append(line)
            if line.startswith("## ") and image_index < len(images):
                img = Path(images[image_index]["url"]).name.split("?")[0]
                alt = images[image_index]["alt"]
                new_lines.append(f"![{alt}](/images/blog/{self.slug}/{img}.jpeg)")
                image_index += 1
        return "\n".join(new_lines)
                

    # ----------------------------------
    # Helper Functions
    # ----------------------------------
    @staticmethod
    def _download_raw(url: str) -> bytes:
        import requests # lazy-import
        resp = requests.get(url, timeout=10)
        resp.raise_for_status() # HTTPリクエストが失敗していないか確認するためのメソッド
        return resp.content
