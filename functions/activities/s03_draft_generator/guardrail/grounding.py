# ---------------------------------------------------------------------------------  # 
# 　　　　　　           生成された文章が引用ソースに基づいているかをチェック　　　        　　　 #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import requests
from config.settings import GROUND_ENDPOINT, CS_KEY

# ----------------------------------
# 引用ソースに基づいているかをチェックする関数
# ----------------------------------
def grounded(text: str, citations: list[str]) -> bool:
    """
    Check if the text is grounded in the citations.
    
    Args:
        text (str): The text to check.
        citations (list[str]): The citations to check against.

    Returns:
        bool: True if the text is grounded in the citations, False otherwise.
    """
    url = f"{GROUND_ENDPOINT}contentsafety/text:detectGroundedness?api-version=2024-09-15-preview"
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": CS_KEY
    }
    body = {
        "text": text,
        "groundingSources": citations
    }
    res = requests.post(url, headers=headers, json=body, timeout=30)
    res.raise_for_status()
    return not res.json()["ungroundedDetected"] 

