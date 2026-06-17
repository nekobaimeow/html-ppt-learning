# Image-Heavy Decks — Patterns & Pitfalls

When building html-ppt-learning decks around visual subjects (architecture, art, photography, design), the standard text-first blocks need augmentation.

## Photo Grid CSS Patterns

Add these to the deck's `<style>` block:

```css
/* === Photo Grids — responsive, mobile-friendly === */
.photo-2 { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin:12px 0; align-items:start; }
.photo-3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; margin:12px 0; align-items:start; }
.photo-4 { display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:10px; margin:12px 0; align-items:start; }
.photo-2x1 { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin:12px 0; align-items:start; }
.photo-img { width:100%; border-radius:8px; object-fit:cover; aspect-ratio:16/9; }
.photo-card { background:var(--surface); border-radius:8px; overflow:hidden; border:1px solid var(--border); }
.photo-card img { width:100%; aspect-ratio:16/9; object-fit:cover; display:block; }
.photo-card .cap { padding:6px 10px; font-size:11px; color:var(--text-2); text-align:center; }

/* Mobile: stack all grids */
@media (max-width: 768px) {
  .photo-2, .photo-2x1, .photo-3, .photo-4 {
    grid-template-columns: 1fr !important;
  }
  .photo-img { max-height: 220px; }
  .deck { padding: 0 8px; }
  .slide { padding: 12px 16px !important; }
  .slide h2 { font-size: 1.1em !important; }
  .slide .block { padding: 6px 10px !important; }
  .compare-table th, .compare-table td { padding: 3px 5px !important; font-size: 11px !important; }
}
```

**Key design decisions:**
- `photo-2x1` uses **1fr 1fr** (NOT 2fr 1fr) — equal columns avoid text squeezing and image dead space
- `align-items: start` — top-align content, no stretched empty gaps
- `@media (max-width: 768px)` — all grids collapse to single column on phones
- `photo-4` for 4-up breed cards / comparison grids

Usage:
```html
<div class="photo-2 mt-m">
  <div class="photo-card"><img src="images/image.jpg"><div class="cap">Caption</div></div>
  <div class="photo-card"><img src="images/image2.jpg"><div class="cap">Caption 2</div></div>
</div>
```

## Batch Image Generation with MiniMax

For decks needing 60+ images, use a Python script that:
1. Loads `MINIMAX_CN_API_KEY` from absolute path `/home/trade/.hermes/.env` (NOT `os.path.expanduser` — it resolves to profile home)
2. Calls `POST /v1/image_generation` with `model: image-01`, `aspect_ratio: 16:9`, `response_format: url`
3. Downloads OSS URL immediately (URLs expire in ~1 hour)
4. Skips existing files (check `os.path.getsize() > 10000` to skip failed partial downloads)
5. Sleeps 3s between calls for rate limiting
6. Run with `python3 -u` for unbuffered stdout in background mode

Template structure:
```python
prompts = [
    # Naming convention: NN_descriptive_name.jpg
    # NN = rough order matching slide order (helps audit captions)
    ("01_parthenon_ext.jpg", "English prompt, 20-200 chars..."),
    ("15_suzhou_museum.jpg", "..."),
    ...
]
for fname, prompt in prompts:
    out = os.path.join(OUT_DIR, fname)
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        skip; continue
    # ... API call ...
    time.sleep(3)
```

See `/home/trade/repos/architecture-art/gen_images.py` for a complete working example (62 architectural images).

## PDF Printing for Image-Heavy Decks

Image-heavy slides often overflow A4 landscape. After extensive testing (architecture-art deck, 30 slides with 62 images), the following approach produced the best results:

### Recommended Print CSS (tested, works)

```css
@media print {
  @page { size: A4 landscape; margin: 0; }
  html, body { margin: 0; padding: 0; width: 100%; height: 100%; }
  .sidebar { display: none !important; }
  .main { margin-left: 0; width: 100%; }
  .deck { max-width: 100%; margin: 0; padding: 0; }

  /* CRITICAL: use block flow, NOT display:grid — grid causes double-page issue */
  .slide { page-break-after: always; padding: 20px 32px; font-size: 10pt;
           max-height: 595pt; overflow: hidden !important; contain: layout paint; }
  .slide:last-child { page-break-after: auto; }

  /* Reduce to 1 image per slide in print */
  .slide .photo-2 .photo-card:nth-child(2),
  .slide .photo-3 .photo-card:nth-child(2),
  .slide .photo-3 .photo-card:nth-child(3),
  .slide .photo-2x1 > div { display: none !important; }
  .slide .photo-2 .photo-card:first-child,
  .slide .photo-3 .photo-card:first-child { grid-column: 1 / -1; }
  .slide .photo-img { max-height: 180pt; object-fit: cover; }

  /* Compress text aggressively */
  .slide h2 { font-size: 15pt !important; margin: 4px 0 !important; }
  .slide h1 { font-size: 20pt !important; }
  .slide .block { padding: 6px 10px !important; margin: 4px 0 !important; }
  .slide .compare-table th, .slide .compare-table td { padding: 2px 4px !important; font-size: 8pt !important; }
  .slide .summary-table th, .slide .summary-table td { padding: 2px 4px !important; font-size: 7pt !important; }
  .slide p { margin: 2px 0 !important; line-height: 1.3 !important; }
  .slide .kicker { font-size: 9pt !important; }
  .slide .block-label { font-size: 8pt !important; }

  /* Hide UI chrome and runtime.js overview clones */
  .progress-bar, .progress-dots, .notes-overlay, .slide-number { display: none !important; }
  .overview, .overview .slide, .overview * { display: none !important; }
}
```

### ❌ Don't use `display: grid !important` on slides for print

The `display: grid` + `align-content: center` approach causes every slide to split across exactly 2 pages — content centered on page 1, overflow on page 2. Chrome's PDF renderer creates a new grid context on each page, and `page-break-after: always` then fires for the *next* slide, resulting in a ghost page between every real slide.

Use regular block flow with `max-height: 595pt; overflow: hidden !important; contain: layout paint` instead.

### Known limitation

Even with `overflow: hidden` and `contain: layout paint`, Chrome's `--headless=new` print engine may still produce extra pages for content-heavy slides. The page-break algorithm in Chromium's PDF renderer doesn't fully respect CSS overflow clipping. **Expect 1.5-2× the page count of the slide count for image-heavy decks.** This is acceptable — the HTML is the primary output; PDF is a rough companion.

### ❌ Print CSS must live in deck HTML, not in learning-print.css

`learning-print.css` belongs to the default profile. From other profiles (like `yinlang`), cross-profile write guard blocks patches. Solution: put all print overrides directly in the deck's `<style>` block, and load `learning-print.css` as a base with `<link media="print">`. The deck's own `<style>` wins specificity.

### ❌ Never reuse an image with a misleading caption

When building image-heavy decks with limited image sets, it's tempting to reuse an image and change its caption to fit the context. **Don't.** An insulator string captioned as "串联补偿装置" or a distant tower captioned as "避雷器" is factually wrong and erodes credibility. If you don't have the right image:
1. Generate a new one (MiniMax takes ~10s per image)
2. Or leave that slide without an image rather than using a wrong one

## Image File Organization

- Deck-local images: `decks/<category>/<slug>/images/`
- HTML references: `<img src="images/filename.jpg">`
- Hub server needs `decks/` path fallback for static files (see deployment.md)
- Total image directory for 30-slide deck: ~20-25MB for 60 images at 200-600KB each
