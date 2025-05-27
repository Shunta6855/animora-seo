
# ライブラリのインポート
import janome.tokenizer as _jt
from config.prompts import GEN_REGENERATE_PROMPT
from utils.azure import call_gpt

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
    count = text.count(keyword)
    total = len(text)
    ratio = count * len(keyword) / total if total else 0.0
    return count, total, ratio


# ----------------------------------
# キーワード不足の文章についてキーワードを含めつつ再生成
# ----------------------------------
def _regenerate_with_keyword(text: str, keyword: str) -> str:
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
    print(f"Regenerating with keyword: {keyword}")
    response = call_gpt(messages, 0.7)
    return response["text"]

# ----------------------------------
# キーワード密度の確認
# ----------------------------------
def ensure_keyword_density(text: str, keyword: str, min_density: float=0.01) -> tuple[str, float]:
    _, _, ratio = _analyze_keyword_density(text, keyword)
    if ratio < min_density:
        print(f"Keyword density is too low: {ratio}")
        text = _regenerate_with_keyword(text, keyword)
        _, _, ratio = _analyze_keyword_density(text, keyword)
    print(f"Keyword density: {ratio}")
    return text, ratio