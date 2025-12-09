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

import secrets
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# === 設定 ===
OUTPUT_FILE = "password_sheet.pdf"
CELL_SIZE = 8 * mm      # 各マスのサイズ
MARGIN = 15 * mm        # 余白
FONT_SIZE = 14          # フォントサイズ

# 誤読しやすい文字を除外した文字セット
# 除外: l, 1, I, O, 0, o
LOWERCASE = "abcdefghijkmnpqrstuvwxyz"
UPPERCASE = "ABCDEFGHJKLMNPQRSTUVWXYZ"
DIGITS = "23456789"

def generate_random_char():
    """大文字・小文字・数字をバランスよく生成"""
    # 出現比率 40:40:20 を再現するための重み付き選択
    weights = [40, 40, 20]
    categories = [LOWERCASE, UPPERCASE, DIGITS]
    total = sum(weights)
    r = secrets.randbelow(total)
    cumulative = 0
    for category, weight in zip(categories, weights):
        cumulative += weight
        if r < cumulative:
            return secrets.choice(category)
    return secrets.choice(categories[-1])

def create_password_sheet(filename):
    """パスワード用紙PDFを生成"""
    width, height = A4
    c = canvas.Canvas(filename, pagesize=A4)
    
    # グリッドの計算（ヘッダー行1行分を考慮）
    usable_width = width - 2 * MARGIN
    usable_height = height - 2 * MARGIN - CELL_SIZE  # ヘッダー行分を引く
    cols = int(usable_width // CELL_SIZE)
    rows = int(usable_height // CELL_SIZE)
    
    # グリッドを中央揃えにするためのオフセット
    grid_width = cols * CELL_SIZE
    grid_height = rows * CELL_SIZE
    x_offset = (width - grid_width) / 2
    y_offset = (height - grid_height) / 2
    
    # フォント設定
    c.setFont("Courier", FONT_SIZE)

    # ヘッダー行（列番号）を描画
    header_y = y_offset + rows * CELL_SIZE
    for col in range(cols):
        x = x_offset + col * CELL_SIZE

        # 灰色の背景
        c.setFillColorRGB(0.85, 0.85, 0.85)
        c.setStrokeColorRGB(0.7, 0.7, 0.7)
        c.setLineWidth(0.5)
        c.rect(x, header_y, CELL_SIZE, CELL_SIZE, fill=1, stroke=1)

        # 列番号を描画
        c.setFillColorRGB(0, 0, 0)
        col_num = str(col + 1)
        text_width = c.stringWidth(col_num, "Courier", FONT_SIZE)
        text_x = x + (CELL_SIZE - text_width) / 2
        text_y = header_y + (CELL_SIZE - FONT_SIZE) / 2 + 2
        c.drawString(text_x, text_y, col_num)

    for row in range(rows):
        for col in range(cols):
            x = x_offset + col * CELL_SIZE
            y = y_offset + (rows - 1 - row) * CELL_SIZE
            
            # 四角を描画
            c.setStrokeColorRGB(0.7, 0.7, 0.7)  # 薄いグレー
            c.setLineWidth(0.5)
            c.rect(x, y, CELL_SIZE, CELL_SIZE)
            
            # ランダム文字を描画
            char = generate_random_char()
            c.setFillColorRGB(0, 0, 0)
            
            # 文字を中央に配置
            text_width = c.stringWidth(char, "Courier", FONT_SIZE)
            text_x = x + (CELL_SIZE - text_width) / 2
            text_y = y + (CELL_SIZE - FONT_SIZE) / 2 + 2
            c.drawString(text_x, text_y, char)
    
    # フッター
    c.setFont("Helvetica", 8)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(MARGIN, 10 * mm, f"Generated: {date.today()}")
    
    c.save()
    print(f"生成完了: {filename}")
    print(f"グリッドサイズ: {cols} x {rows} = {cols * rows} 文字")

if __name__ == "__main__":
    create_password_sheet(OUTPUT_FILE)
