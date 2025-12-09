# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "reportlab",
# ]
# ///
"""
パスワード用紙生成スクリプト
A4用紙にランダムな文字をグリッド状に配置し、
各文字を四角で囲んだPDFを生成します。
"""

from password_paper import create_password_sheet

OUTPUT_FILE = "password_sheet.pdf"

if __name__ == "__main__":
    cols, rows = create_password_sheet(OUTPUT_FILE)
    print(f"生成完了: {OUTPUT_FILE}")
    print(f"グリッドサイズ: {cols} x {rows} = {cols * rows} 文字")
