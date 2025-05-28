# ---------------------------------------------------------------------------------  # 
# 　　　　　　       　                  クエリの生成　　　  　　　　　　　　　　          　 #
# ---------------------------------------------------------------------------------  #

# ライブラリのインポート
import random
from janome.tokenizer import Tokenizer
from utils.azure import call_gpt
from config.prompts import TRANSLATE_PROMPT, EXPAND_SYNONYMS_PROMPT

tokenizer = Tokenizer()

# ----------------------------------
# 日本語を英語に翻訳する関数
# ----------------------------------
def translate_en(text: str) -> str:
    messages = [
        TRANSLATE_PROMPT,
        {
            "role": "user",
            "content": (
                f"# 日本語: {text}\n"
                f"# 英語: "
            )
        }
    ]
    response = call_gpt(messages, 0.2)
    return response["text"]


# ----------------------------------
# クエリを前処理する関数
# ----------------------------------
def preprocess_query(query: str) -> list[str]:
    """
    Preprocess the query.
    """
    nouns = [t.surface for t in tokenizer.tokenize(query) if t.part_of_speech.startswith("名詞")]
    base = " ".join(nouns) if nouns else query
    translated = translate_en(base)

    messages = [
        EXPAND_SYNONYMS_PROMPT,
        {
            "role": "user",
            "content": (
                f"# Query: {translated}\n"
                f"# Synonyms: "
            )
        }
    ]
    response = call_gpt(messages, 0.7)
    synonyms = response["synonyms"]
    return [translated] + synonyms