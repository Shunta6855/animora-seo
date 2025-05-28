# ライブラリのインポート
from .unsplash import Unsplash
from .pexels import Pexels
from .pixabay import Pixabay

# ----------------------------------
# 共通の画像メタデータ型
# ----------------------------------
class ImageMeta(dict):
    url: str
    alt: str
    credit: str

# ----------------------------------
# 全プロバイダを取得する関数
# ----------------------------------
def get_all_providers():
    return [Unsplash(), Pexels(), Pixabay()]