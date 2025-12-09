"""Vercel Serverless Function for password sheet generation."""

import sys
from datetime import date
from http.server import BaseHTTPRequestHandler
from pathlib import Path

# 親ディレクトリをパスに追加して共通モジュールをインポート
sys.path.insert(0, str(Path(__file__).parent.parent))
from password_paper import create_password_sheet_bytes


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        pdf_bytes = create_password_sheet_bytes()

        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header(
            "Content-Disposition",
            f"attachment; filename=password_sheet_{date.today()}.pdf",
        )
        self.send_header("Content-Length", str(len(pdf_bytes)))
        self.end_headers()
        self.wfile.write(pdf_bytes)
