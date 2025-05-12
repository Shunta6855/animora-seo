# ---------------------------------------------------------------------------------  # 
#        生成した記事にNSFW(性的/暴力的)、OCRable text（読めない文字列)がないかをチェック      #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from functions.config.settings import CS_ENDPOINT, CS_KEY

client = ContentSafetyClient(
    endpoint=CS_ENDPOINT,
    credential=AzureKeyCredential(CS_KEY)
)

# ----------------------------------
# NSFW(性的/暴力的)、OCRable text（読めない文字列)がないかをチェックする関数
# ----------------------------------
def safe_text(text: str) -> bool:
    """
    Check if the text contains NSFW or OCRable text
    
    Args:
        text: The text to check
    
    Returns:
        bool: True if the text is safe, False otherwise
    """
    result = client.analyze_text({"text": text})
    max_score = max(c.severity for c in result.categories_analysis) # 0-7
    return max_score <= 3 # 3以下なら安全