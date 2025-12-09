"""Vercel Serverless Function for index page."""

from http.server import BaseHTTPRequestHandler


HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Paper Generator</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1 { color: #333; }
        .button {
            display: inline-block;
            background: #0070f3;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 6px;
            font-size: 16px;
            margin-top: 20px;
        }
        .button:hover { background: #0051a8; }
        .features {
            background: #f5f5f5;
            padding: 15px 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .features li { margin: 8px 0; }
    </style>
</head>
<body>
    <h1>Password Paper Generator</h1>
    <p>パスワード用紙を生成します。A4用紙にランダムな文字をグリッド状に配置したPDFをダウンロードできます。</p>

    <div class="features">
        <strong>特徴:</strong>
        <ul>
            <li>各文字が四角で囲まれており、ハサミで切りやすい</li>
            <li>誤読しやすい文字（l, 1, I, O, 0, o）を除外</li>
            <li>大文字・小文字・数字をバランスよく配置</li>
            <li>暗号学的に安全な乱数生成器を使用</li>
        </ul>
    </div>

    <a href="/api/generate" class="button">PDFをダウンロード</a>

    <p style="margin-top: 40px; color: #666; font-size: 14px;">
        <a href="https://github.com/kangaechu/password-paper">GitHub</a>
    </p>
</body>
</html>
"""


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))
