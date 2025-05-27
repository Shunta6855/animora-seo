# ライブラリのインストール
import json, shlex, subprocess, tempfile
from pathlib import Path

# ----------------------------------
# Lighthouse CIを使ってローカルのHTMLファイルに対するパフォーマンス監査を実行する関数
# ----------------------------------
def run_lighthouse(html_path: Path, lh_root: Path) -> dict[str, float]:
    """
    Run Lighthouse on the HTML file.

    Args:
        html_path: The path to the HTML file
        lh_root: The directory where the Lighthouse project is created

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
    report_dir = lh_root / ".lighthouseci"
    report_dir.mkdir(exist_ok=True)
    cmd = (
        f"lhci autorun "
        f"--config={shlex.quote(str(manifest_path))} "
        f"--upload.target=filesystem "
        f"--upload.outputDir={shlex.quote(str(report_dir))}"
    )
    proc = subprocess.run(shlex.split(cmd), capture_output=True, text=True) 

    if proc.returncode != 0:
        raise RuntimeError(f"Lighthouse CI failed: {proc.stderr}\n{proc.stdout}")
    
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