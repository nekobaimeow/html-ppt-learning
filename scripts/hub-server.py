#!/usr/bin/env python3
"""
html-ppt-hub — Secure courseware portal with auto-discovery.
Each deck has its own deck.json; server auto-scans decks/ at startup.
POST /reload triggers re-scan without restart.
"""
import http.server
import os
import json
import re
import mimetypes
import urllib.parse
import glob

HUB_ROOT = os.path.dirname(os.path.abspath(__file__))
DECKS_DIR = os.path.join(HUB_ROOT, 'decks')
SHARED_DIR = os.path.join(HUB_ROOT, 'shared')
CATALOG_PATH = os.path.join(HUB_ROOT, 'categories.json')
PORT = 9210

ALLOWED_EXT = {'.html', '.css', '.js', '.svg', '.png', '.jpg', '.webp',
               '.woff', '.woff2', '.ttf', '.json', '.ico', '.txt', '.xml'}

MIME_MAP = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.webp': 'image/webp',
    '.woff': 'font/woff',
    '.woff2': 'font/woff2',
    '.ttf': 'font/ttf',
    '.json': 'application/json',
    '.ico': 'image/x-icon',
    '.txt': 'text/plain; charset=utf-8',
}

# ─── Global catalog (mutable, rebuilt by load_catalog) ───
CATALOG = {"categories": [], "decks": []}
DECK_MAP = {}
CATEGORY_MAP = {}


def load_catalog():
    """Auto-scan decks/ for deck.json files; fall back to categories.json."""
    global CATALOG, DECK_MAP, CATEGORY_MAP

    deck_jsons = sorted(glob.glob(os.path.join(DECKS_DIR, '*', '*', 'deck.json')))

    if deck_jsons:
        # ─── Auto-discovery mode ───
        categories = {}  # slug → {name, icon}
        decks = []

        for dj_path in deck_jsons:
            try:
                with open(dj_path, 'r', encoding='utf-8') as f:
                    info = json.load(f)
            except Exception:
                continue

            # slug = directory name containing deck.json
            slug = os.path.basename(os.path.dirname(dj_path))
            category_slug = info.get('category', 'other')

            # Try category.json in the category directory
            cat_dir = os.path.join(DECKS_DIR, category_slug)
            cat_json = os.path.join(cat_dir, 'category.json')
            if category_slug not in categories:
                cat_info = {}
                if os.path.isfile(cat_json):
                    try:
                        with open(cat_json, 'r', encoding='utf-8') as f:
                            cat_info = json.load(f)
                    except Exception:
                        pass
                categories[category_slug] = {
                    'name': cat_info.get('name', category_slug),
                    'icon': cat_info.get('icon', '📚'),
                    'slug': category_slug,
                }

            decks.append({
                'title': info.get('title', slug),
                'slug': slug,
                'category': category_slug,
                'difficulty': info.get('difficulty', 2),
                'slides': info.get('slides', 0),
                'description': info.get('description', ''),
                'tags': info.get('tags', []),
            })

        CATALOG = {
            'categories': sorted(categories.values(), key=lambda c: c['slug']),
            'decks': sorted(decks, key=lambda d: d['category'] + d['slug']),
        }

    else:
        # ─── Fallback: use static categories.json ───
        if os.path.isfile(CATALOG_PATH):
            with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
                CATALOG = json.load(f)
        else:
            CATALOG = {"categories": [], "decks": []}

    # Rebuild lookups
    DECK_MAP = {}
    CATEGORY_MAP = {}
    for cat in CATALOG.get('categories', []):
        CATEGORY_MAP[cat['slug']] = cat
    for deck in CATALOG.get('decks', []):
        DECK_MAP[deck['slug']] = deck
        deck['_category'] = CATEGORY_MAP.get(deck['category'], {})

    print(f'[hub] catalog: {len(CATALOG["decks"])} decks, {len(CATALOG["categories"])} categories')


# ─── Load at startup ───
load_catalog()


def is_safe_path(requested: str) -> tuple:
    decoded = urllib.parse.unquote(requested)
    if '..' in decoded or decoded.startswith('/') or '//' in decoded:
        return False, 'path_traversal'
    if '\x00' in decoded:
        return False, 'null_byte'
    if re.search(r'[<>|;`$]', decoded):
        return False, 'suspicious_char'
    full = os.path.normpath(os.path.join(HUB_ROOT, decoded))
    if not full.startswith(HUB_ROOT + os.sep) and full != HUB_ROOT:
        return False, 'escape_root'
    return True, full


def get_mime(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    return MIME_MAP.get(ext, 'application/octet-stream')


class HubHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        path = self.path.split('?')[0].lstrip('/')

        if path == '' or path == 'index.html':
            self.serve_home()
            return

        if path.startswith('api/catalog'):
            self.send_json(CATALOG)
            return

        if path.endswith('/') and not path.startswith('shared/'):
            self.serve_deck_page(path)
            return

        ok, result = is_safe_path(path)
        if not ok:
            self.send_error(403, f'Forbidden: {result}')
            return
        if os.path.isdir(result):
            self.send_error(403, 'Directory listing not allowed')
            return

        ext = os.path.splitext(result)[1].lower()
        if ext not in ALLOWED_EXT:
            self.send_error(403, f'File type not allowed: {ext}')
            return

        if not os.path.isfile(result):
            fallback = os.path.normpath(os.path.join(HUB_ROOT, "decks", path))
            if fallback.startswith(HUB_ROOT + os.sep) and os.path.isfile(fallback):
                result = fallback
            else:
                self.send_error(404, 'Not found')
                return

        try:
            with open(result, 'rb') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-Type', get_mime(result))
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'public, max-age=3600')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('X-Frame-Options', 'SAMEORIGIN')
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_error(500, str(e))

    def do_POST(self):
        """POST /reload — re-scan decks directory."""
        path = self.path.split('?')[0].rstrip('/')
        if path == '/reload':
            load_catalog()
            self.send_json({"status": "ok", "decks": len(CATALOG["decks"])})
        else:
            self.send_error(404)

    def serve_home(self):
        html = self._render_home()
        data = html.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(data)

    def serve_deck_page(self, path: str):
        deck_dir = path.rstrip('/')
        deck_path = os.path.join('decks', deck_dir)
        index_path = os.path.join(HUB_ROOT, deck_path, 'index.html')
        ok, result = is_safe_path(f'{deck_path}/index.html')
        if not ok:
            self.send_error(403, 'Forbidden')
            return
        if not os.path.isfile(index_path):
            self.send_error(404, 'Deck not found')
            return
        with open(index_path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = re.sub(r'(src|href)="(?:\.\.\/)*assets/', r'\1="/shared/assets/', html)
        data = html.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, data):
        payload = json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(payload)

    def _render_home(self) -> str:
        grouped = {}
        for deck in CATALOG['decks']:
            cs = deck['category']
            if cs not in grouped:
                grouped[cs] = {
                    'name': deck['_category'].get('name', cs),
                    'icon': deck['_category'].get('icon', '📚'),
                    'decks': []
                }
            grouped[cs]['decks'].append(deck)

        def stars(n):
            return ''.join(['★' if i < n else '☆' for i in range(3)])

        sections = []
        for cat_slug, cd in grouped.items():
            cards = []
            for d in cd['decks']:
                cards.append(f'''
                <a href="/{d['category']}/{d['slug']}/" class="deck-card">
                    <div class="card-header">
                        <span class="card-difficulty">{stars(d.get('difficulty', 1))}</span>
                        <span class="card-slides">{d.get('slides', '?')} 页</span>
                    </div>
                    <h3>{d['title']}</h3>
                    <p>{d.get('description', '')}</p>
                    <div class="card-tags">
                        {''.join(f'<span class="tag">{t}</span>' for t in d.get('tags', []))}
                    </div>
                </a>''')
            sections.append(f'''
            <section class="category">
                <h2 class="cat-title">{cd['icon']} {cd['name']}</h2>
                <div class="deck-grid">{''.join(cards)}</div>
            </section>''')

        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>html-ppt-hub · 知识课件中心</title>
<style>
  *,*::before,*::after{{box-sizing:border-box}}
  :root {{
    --bg: #0d1117; --bg-card: #161b22; --bg-hover: #1c2333;
    --border: #30363d; --text: #e6edf3; --text-dim: #8b949e;
    --accent: #58a6ff; --accent2: #3fb950; --accent3: #f0883e;
    --radius: 12px;
    font-family: -apple-system,BlinkMacSystemFont,'Noto Sans SC','Segoe UI',sans-serif;
  }}
  html,body{{margin:0;padding:0;background:var(--bg);color:var(--text)}}
  body{{min-height:100vh}}
  .hero{{
    padding:60px 40px 40px;text-align:center;
    background:linear-gradient(180deg,rgba(88,166,255,0.06)0%,transparent 100%);
    border-bottom:1px solid var(--border);
  }}
  .hero h1{{font-size:2.6em;margin:0 0 8px;letter-spacing:-.03em}}
  .hero .sub{{color:var(--text-dim);font-size:1.1em}}
  .hero .stats{{margin-top:16px;display:flex;gap:32px;justify-content:center;flex-wrap:wrap}}
  .hero .stat{{color:var(--text-dim);font-size:.9em}}
  .hero .stat strong{{color:var(--accent)}}
  .container{{max-width:1100px;margin:0 auto;padding:30px 40px 60px}}
  .category{{margin-bottom:48px}}
  .cat-title{{font-size:1.5em;margin:0 0 20px;padding-bottom:10px;border-bottom:1px solid var(--border)}}
  .deck-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}}
  .deck-card{{
    display:block;text-decoration:none;color:inherit;
    background:var(--bg-card);border:1px solid var(--border);
    border-radius:var(--radius);padding:24px;
    transition:border-color .2s,transform .2s,box-shadow .2s;
  }}
  .deck-card:hover{{
    border-color:var(--accent);transform:translateY(-2px);
    box-shadow:0 8px 24px rgba(88,166,255,0.08);
  }}
  .card-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}}
  .card-difficulty{{color:var(--accent3);font-size:.85em;letter-spacing:.05em}}
  .card-slides{{color:var(--text-dim);font-size:.8em}}
  .deck-card h3{{margin:0 0 10px;font-size:1.15em;line-height:1.3}}
  .deck-card p{{margin:0 0 14px;color:var(--text-dim);font-size:.9em;line-height:1.5}}
  .card-tags{{display:flex;gap:6px;flex-wrap:wrap}}
  .tag{{font-size:.75em;padding:2px 8px;border-radius:99px;background:rgba(88,166,255,0.1);color:var(--accent)}}
  .footer{{text-align:center;padding:30px;color:var(--text-dim);font-size:.8em;border-top:1px solid var(--border)}}
  @media(max-width:640px){{
    .hero{{padding:40px 20px 30px}}.hero h1{{font-size:1.8em}}
    .container{{padding:20px}}.deck-grid{{grid-template-columns:1fr}}
  }}
</style>
</head>
<body>
  <header class="hero">
    <h1>📚 html-ppt-hub</h1>
    <p class="sub">高信息密度知识课件 · 分类浏览 · 自动发现</p>
    <div class="stats">
      <span class="stat"><strong>{len(CATALOG["decks"])}</strong> 门课程</span>
      <span class="stat"><strong>{len(grouped)}</strong> 个分类</span>
      <span class="stat">按 <strong>T</strong> 切换主题 · <strong>j/k</strong> 翻页</span>
    </div>
  </header>
  <div class="container">
    {''.join(sections)}
  </div>
  <footer class="footer">
    html-ppt-hub · MIT · Powered by html-ppt-learning · Auto-discovery mode
  </footer>
</body>
</html>'''

    def log_message(self, *a):
        pass


if __name__ == '__main__':
    import socketserver, threading, time
    print(f'[html-ppt-hub] serving on 0.0.0.0:{PORT}')
    print(f'[html-ppt-hub] root: {HUB_ROOT}')
    print(f'[html-ppt-hub] mode: {"auto-discovery" if any(glob.glob(os.path.join(DECKS_DIR, "*", "*", "deck.json"))) else "static catalog"}')
    print(f'[html-ppt-hub] {len(CATALOG["decks"])} decks, {len(CATALOG["categories"])} categories')

    # Auto-reload thread: re-scan every 60s for new decks
    def auto_reloader():
        while True:
            time.sleep(60)
            try:
                old_count = len(CATALOG['decks'])
                load_catalog()
                new_count = len(CATALOG['decks'])
                if new_count != old_count:
                    print(f'[hub] auto-reload: {old_count} → {new_count} decks')
            except Exception:
                pass
    threading.Thread(target=auto_reloader, daemon=True).start()

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('0.0.0.0', PORT), HubHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\n[html-ppt-hub] shutting down')
