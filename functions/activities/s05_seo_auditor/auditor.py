# ---------------------------------------------------------------------------------  # 
#            生成された記事がSEO的に問題ないかをチェックし、自動で修正するアクティビティ          #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
from __future__ import annotations

import tempfile, markdown, json
from pathlib import Path
from typing import Optional, Sequence, Any
    # Sequence: リスト、タプル、文字列などのシーケンス型

from activities.s05_seo_auditor.keyword_density import ensure_keyword_density
from activities.s05_seo_auditor.meta_generator import gen_meta
from activities.s05_seo_auditor.lighthouse_runner import run_lighthouse


# ----------------------------------
# SEO監査クラス
# ----------------------------------
class SEOAuditor:
    MIN_DENSITY = 0.01
    MAX_DENSITY = 0.03

    def __init__(self, keyword: str, lighthouse_project_root: str | Path | None = None):
        self.keyword = keyword
        self.lh_root = Path(lighthouse_project_root or ".").expanduser().resolve() 
            # expanduser(): "~" -> ホームディレクトリに変換
            # resolve(): 絶対パスに変換
    
    # ----------------------------------
    # 記事の生成
    # ----------------------------------
    def audit(
        self,
        markdown_text: str,
        outline: dict[str, Any],
        images: Optional[Sequence[dict[str, str]]] = None,
        do_lighthouse: bool = True,
    ) -> dict[str, object]:
        """
        Audit the article.
        
        Args:
            markdown_text: The markdown of the article
            outline: The outline of the article
            images: The images of the article
            do_lighthouse: Whether to do the lighthouse audit

        Returns:
            The result of the audit
        """
        audit_file = Path("data/articles") / f"{self.keyword}.json"
        if audit_file.exists():
            print(f"Audit already exists: {audit_file}")
            with open(audit_file, "r", encoding="utf-8") as f:
                return json.load(f)
        
        markdown_text, density = ensure_keyword_density(markdown_text, self.keyword, self.MIN_DENSITY)
        title, description = gen_meta(outline, markdown_text)

        lighthouse_metrics: dict[str, float] | None = None
        if do_lighthouse:
            html_body = markdown.markdown(markdown_text)
            full_html = self.wrap_html(title, html_body)

            with tempfile.TemporaryDirectory() as tmpdir:
                html_path = Path(tmpdir) / "index.html"
                html_path.write_text(full_html, encoding="utf-8")
                lighthouse_metrics = run_lighthouse(html_path, self.lh_root)
        
        audit_data = {
            "markdown": markdown_text,
            "images": images or [],
            "meta": {"title": title, "description": description},
            "keyword_density": density,
            "lighthouse": lighthouse_metrics,
        }
        
        with open(audit_file, "w", encoding="utf-8") as f:
            json.dump(audit_data, f, ensure_ascii=False, indent=2)

        return audit_data
    
    # ----------------------------------
    # html形式でラップする関数
    # ----------------------------------
    def wrap_html(self, title: str, body: str) -> str:
        return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{title}">
    <title>{title}</title>

    <!-- ★ 1行追加: 空データURIの favicon で 404 を防止 -->
    <link rel="icon" href="data:,"> 

    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans JP', sans-serif;
            font-size: 16px;
            line-height: 1.6;
            padding: 2rem;
            max-width: 720px;
            margin: auto;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 1rem auto;
        }}
        details {{
            margin-top: 1rem;
        }}
    </style>
</head>
    <body>
    {body}
    </body>
</html>
"""
        