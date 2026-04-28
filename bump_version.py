#!/usr/bin/env python3
"""index.html のバージョン番号をインクリメントするスクリプト
使い方: python3 bump_version.py
"""
import re, sys, os
from datetime import datetime

# スクリプトと同じディレクトリの index.html を対象にする
INDEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')

with open(INDEX, encoding='utf-8') as f:
    html = f.read()

m = re.search(r'const APP_VERSION = "v(\d{4}\.\d{2}\.\d{2})\.(\d+)"', html)
if not m:
    print("APP_VERSION not found"); sys.exit(1)

old_date, old_seq = m.group(1), int(m.group(2))
today = datetime.now().strftime('%Y.%m.%d')

new_seq = old_seq + 1 if old_date == today else 1
new_ver = f"v{today}.{new_seq:02d}"
old_ver = f"v{old_date}.{old_seq:02d}"

html = html.replace(f'const APP_VERSION = "{old_ver}"', f'const APP_VERSION = "{new_ver}"', 1)
with open(INDEX, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"{old_ver} → {new_ver}")
