# ---------------------------------------------------------------------------------  # 
#            生成された記事がSEO的に問題ないかをチェックし、自動で修正するアクティビティ          #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
from __future__ import annotations

import json, re, shlex, subprocess, tempfile
from pathlib import Path
from typing import Optional, Sequence
    # Sequence: リスト、タプル、文字列などのシーケンス型

import janome.tokenizer as _jt
from functions.config.prompts import GEN_REGENERATE_PROMPT
from functions.utils.azure import call_gpt

tokenizer = _jt.Tokenizer()

# ----------------------------------
# キーワード密度の分析
# ----------------------------------
def _analyze_keyword_density(text: str, keyword: str) -> tuple[int, int, float]:
    """
    Analyze the keyword density of the text.
    
    Args:
        text: The text to analyze
        keyword: The keyword to analyze

    Returns:
        count: The number of times the keyword appears in the text
        total: The total number of tokens in the text
        ratio: The ratio of the keyword to the total number of tokens
    """
    tokens = list(token.surface for token in tokenizer.tokenize(text))
    keyword_tokens = keyword.split()
    total = len(tokens)
    count = sum(
        1 for i in range(total - len(keyword_tokens) + 1)
        if tokens[i:i+len(keyword_tokens)] == keyword_tokens
    )
    ratio = count / total if total else 0.0
    return count, total, ratio


# ----------------------------------
# キーワード不足の文章についてキーワードを含めつつ再生成
# ----------------------------------
async def _regenerate_with_keyword(text: str, keyword: str) -> str:
    """
    Regenerate the text with the keyword.
    
    Args:
        text: The text to regenerate
        keyword: The keyword to regenerate

    Returns:
        The regenerated text
    """
    messages = [
        GEN_REGENERATE_PROMPT,
        {
            "role": "user",
            "content": (
                f"# Keyword: {keyword}\n"
                f"# Text: {text}\n"
                "上記の情報をもとに、記事本文をJSON形式で生成してください"
            )
        }
    ]
    response = await call_gpt(messages, 0.7)
    return response["text"]


# ----------------------------------
# メインクラス
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
    # Lighthouse CIを使ってローカルのHTMLファイルに対するパフォーマンス監査を実行する関数
    # ----------------------------------
    def _run_lighthouse(self, html_path: Path) -> dict[str, float]:
        """
        Run Lighthouse on the HTML file.

        Args:
            html_path: The path to the HTML file

        Returns:
            The result of Lighthouse(dict of score)
        """
        manifest = {
            "ci": {
                "collect": {"staticDistDir": str(html_path.parent), "url": [html_path.name]},
                    # staticDistDir: HTMLが存在するディレクトリの絶対パス
                    # url: そのディレクトリ内のファイル名(相対パス)
                "assert": {"preset": "lighthouse:recommended"},
                    # preset: Lighthouseの推奨設定を使う
            }
        }
        # tempfile.NamedTemporaryFile(): 一時的な.jsonファイルを作成し、そこに設定manifestを書き込む
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as fp:
            json.dump(manifest, fp)
            manifest_path = Path(fp.name)

        # lhci autorun: Lighthouseの設定ファイルを読み込んで、パフォーマンス監査を実行
        cmd = f"lhci autorun --config={shlex.quote(str(manifest_path))} --upload.target=filesystem"
        proc = subprocess.run(shlex.split(cmd), capture_output=True, text=True) 
        if proc.returncode != 0:
            raise RuntimeError(f"Lighthouse CI failed: {proc.stderr}\n{proc.stdout}")
        report_dir = self.lh_root / ".lighthouseci"
        reportfiles = list(report_dir.glob("*.json"))
        if not reportfiles:
            raise RuntimeError("No report files found")
        with reportfiles[0].open() as fp:
            data = json.load(fp)
        return {
            "performance": data["categories"]["performance"]["score"],
            "accessibility": data["categories"]["accessibility"]["score"],
            "best-practices": data["categories"]["best-practices"]["score"],
            "seo": data["categories"]["seo"]["score"],
        }
        
    # ----------------------------------
    # キーワード密度の確認
    # ----------------------------------
    async def _ensure_keyword_density(self, text: str) -> tuple[str, float]:
        occurrences, total, ratio = _analyze_keyword_density(text, self.keyword)
        if ratio < self.MIN_DENSITY:
            text = await _regenerate_with_keyword(text, self.keyword)
            _, _, ratio = _analyze_keyword_density(text, self.keyword)
        return text, ratio
    
    # ----------------------------------
    # メタタグ(タイトル、ディスクリプション)の生成
    # ----------------------------------
    @staticmethod
    def _gen_meta(outline: dict[str, str | list[str]], first_section: str) -> tuple[str, str]:
        """
        Generate the meta tags(title, description) from the outline and the first section.
        
        Args:
            outline: The outline of the article
            first_section: The first section of the article

        Returns:
            The title and the description
        """
        title = str(outline.get("title", "")).strip()[:32]
        description = re.sub(r"\s+", " ", first_section)[:120].rstrip() + "..."
        return title, description
    
    # ----------------------------------
    # 記事の生成
    # ----------------------------------
    async def audit(
        self,
        markdown: str,
        outline: dict[str, str | list[str]],
        images: Optional[Sequence[dict[str, str]]] = None,
        do_lighthouse: bool = False,
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
        markdown, density = await self._ensure_keyword_density(markdown)
        first_section_text = next((s for s in markdown.split("\n\n") if s.strip()), "")
        title, description = self._gen_meta(outline, first_section_text)
        lighthouse_metrics: dict[str, float] | None = None
        if do_lighthouse:
            with tempfile.TemporaryDirectory() as tmpdir:
                html_path = Path(tmpdir) / "index.html"
                html_path.write_text(markdown, encoding="utf-8")
                lighthouse_metrics = self._run_lighthouse(html_path)
        return {
            "markdown": markdown,
            "images": images or [],
            "meta": {"title": title, "description": description},
            "keyword_density": density,
            "lighthouse": lighthouse_metrics,
        }
        