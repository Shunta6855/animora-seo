# ---------------------------------------------------------------------------------  # 
#                       markdown形式のコードで記事構成を保存する関数                       #
# ---------------------------------------------------------------------------------  #
# ライブラリのインポート
import textwrap
from IPython.display import Markdown


# ----------------------------------
# markdown形式のコードで記事構成を保存する関数
# ----------------------------------
def to_markdown(text):
    """
    Convert text to markdown format and display it.
    """
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)
