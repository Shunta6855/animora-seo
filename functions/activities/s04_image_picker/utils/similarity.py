# ---------------------------------------------------------------------------------  # 
# 　　　　　　       　                  類似度を計算　　　  　　　　　　　　　　          　 #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import numpy as np
from utils.azure import embedding

def get_embedding(text: str) -> list[float]:
    """
    Get the embedding of the text.
    """
    return embedding(text)

def cosine_similarity(u: list[float], v: list[float]) -> float:
    """
    Calculate the cosine similarity between two vectors.
    """
    return float(np.dot(u, v))