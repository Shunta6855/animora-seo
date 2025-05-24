# ---------------------------------------------------------------------------------  # 
#            生成された記事がSEO的に問題ないかをチェックし、自動で修正するアクティビティ          #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
from __future__ import annotations

import tempfile
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
        markdown: str,
        outline: dict[str, Any],
        images: Optional[Sequence[dict[str, str]]] = None,
        do_lighthouse: bool = True,
    ) -> dict[str, object]:
        """
        Audit the article.
        
        Args:
            markdown: The markdown of the article
            outline: The outline of the article
            images: The images of the article
            do_lighthouse: Whether to do the lighthouse audit

        Returns:
            The result of the audit
        """
        markdown, density = ensure_keyword_density(markdown, self.keyword, self.MIN_DENSITY)
        title, description = gen_meta(outline, markdown)

        lighthouse_metrics: dict[str, float] | None = None
        if do_lighthouse:
            with tempfile.TemporaryDirectory() as tmpdir:
                html_path = Path(tmpdir) / "index.html"
                html_path.write_text(markdown, encoding="utf-8")
                lighthouse_metrics = run_lighthouse(html_path, self.lh_root)

        return {
            "markdown": markdown,
            "images": images or [],
            "meta": {"title": title, "description": description},
            "keyword_density": density,
            "lighthouse": lighthouse_metrics,
        }
        