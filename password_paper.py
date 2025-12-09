"""パスワード用紙生成の共通モジュール"""

import io
import secrets
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

# === 設定 ===
CELL_SIZE = 8 * mm
MARGIN = 15 * mm
FONT_SIZE = 14

# 誤読しやすい文字を除外した文字セット
LOWERCASE = "abcdefghijkmnpqrstuvwxyz"
UPPERCASE = "ABCDEFGHJKLMNPQRSTUVWXYZ"
DIGITS = "23456789"


def generate_random_char():
    """大文字・小文字・数字をバランスよく生成"""
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


def create_password_sheet(output):
    """パスワード用紙PDFを生成

    Args:
        output: ファイルパス(str)またはBytesIOオブジェクト
    """
    width, height = A4
    c = canvas.Canvas(output, pagesize=A4)

    # グリッドの計算（ヘッダー行・列1つ分を考慮）
    usable_width = width - 2 * MARGIN - CELL_SIZE  # 左側ヘッダー列分を引く
    usable_height = height - 2 * MARGIN - CELL_SIZE  # 上側ヘッダー行分を引く
    cols = min(int(usable_width // CELL_SIZE), 20)  # 最大20列
    rows = int(usable_height // CELL_SIZE)

    # グリッドを中央揃えにするためのオフセット（ヘッダー列を含む）
    grid_width = (cols + 1) * CELL_SIZE  # ヘッダー列を含む
    grid_height = rows * CELL_SIZE
    x_offset = (width - grid_width) / 2
    y_offset = (height - grid_height) / 2

    # フォント設定
    c.setFont("Courier", FONT_SIZE)

    # ヘッダー行（列番号）を描画
    header_y = y_offset + rows * CELL_SIZE
    for col in range(cols):
        x = x_offset + (col + 1) * CELL_SIZE  # ヘッダー列分ずらす

        c.setFillColorRGB(0.85, 0.85, 0.85)
        c.setStrokeColorRGB(0.7, 0.7, 0.7)
        c.setLineWidth(0.5)
        c.rect(x, header_y, CELL_SIZE, CELL_SIZE, fill=1, stroke=1)

        c.setFillColorRGB(0, 0, 0)
        col_num = str((col + 1) % 10)  # 下1桁のみ表示
        text_width = c.stringWidth(col_num, "Courier", FONT_SIZE)
        text_x = x + (CELL_SIZE - text_width) / 2
        text_y = header_y + (CELL_SIZE - FONT_SIZE) / 2 + 2
        c.drawString(text_x, text_y, col_num)

    # ヘッダー列（行番号）を描画
    for row in range(rows):
        x = x_offset
        y = y_offset + (rows - 1 - row) * CELL_SIZE

        c.setFillColorRGB(0.85, 0.85, 0.85)
        c.setStrokeColorRGB(0.7, 0.7, 0.7)
        c.setLineWidth(0.5)
        c.rect(x, y, CELL_SIZE, CELL_SIZE, fill=1, stroke=1)

        c.setFillColorRGB(0, 0, 0)
        row_num = str((row + 1) % 10)  # 下1桁のみ表示
        text_width = c.stringWidth(row_num, "Courier", FONT_SIZE)
        text_x = x + (CELL_SIZE - text_width) / 2
        text_y = y + (CELL_SIZE - FONT_SIZE) / 2 + 2
        c.drawString(text_x, text_y, row_num)

    for row in range(rows):
        for col in range(cols):
            x = x_offset + (col + 1) * CELL_SIZE  # ヘッダー列分ずらす
            y = y_offset + (rows - 1 - row) * CELL_SIZE

            c.setStrokeColorRGB(0.7, 0.7, 0.7)
            c.setLineWidth(0.5)
            c.rect(x, y, CELL_SIZE, CELL_SIZE)

            # 26行目以降は空のセル
            if row >= 25:
                continue

            char = generate_random_char()
            c.setFillColorRGB(0, 0, 0)

            text_width = c.stringWidth(char, "Courier", FONT_SIZE)
            text_x = x + (CELL_SIZE - text_width) / 2
            text_y = y + (CELL_SIZE - FONT_SIZE) / 2 + 2
            c.drawString(text_x, text_y, char)

    # フッター
    c.setFont("Helvetica", 8)
    c.setFillColorRGB(0.5, 0.5, 0.5)
    c.drawString(MARGIN, 10 * mm, f"Generated: {date.today()}")

    c.save()
    return cols, rows


def create_password_sheet_bytes():
    """パスワード用紙PDFをバイト列として生成"""
    buffer = io.BytesIO()
    create_password_sheet(buffer)
    buffer.seek(0)
    return buffer.getvalue()
