#!/usr/bin/env python3
"""
スライドパネル用ローカルサーバー
PDFをiframe内にインライン表示するために使用
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
import os, sys

PORT = 3478

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)

        # CORS プリフライト
        if parsed.path == '/file':
            params = parse_qs(parsed.query)
            file_path = unquote(params.get('path', [''])[0])
            page = params.get('page', ['1'])[0]

            if os.path.isfile(file_path) and file_path.lower().endswith('.pdf'):
                size = os.path.getsize(file_path)
                self.send_response(200)
                self.send_header('Content-Type', 'application/pdf')
                self.send_header('Content-Length', str(size))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Cache-Control', 'public, max-age=3600')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()

        elif parsed.path == '/ping':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'ok')

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, fmt, *args):
        pass  # ログ非表示

print(f'スライドサーバー起動中: http://localhost:{PORT}')
print('このウィンドウを開いたままにしてください。終了するには Ctrl+C')
try:
    HTTPServer(('localhost', PORT), Handler).serve_forever()
except KeyboardInterrupt:
    print('サーバーを停止しました')
