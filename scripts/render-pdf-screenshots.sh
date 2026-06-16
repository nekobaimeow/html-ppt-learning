#!/usr/bin/env bash
# html-ppt-learning :: render-pdf-screenshots.sh
# Render each slide as a screenshot via headless Chrome, combine with img2pdf.
# Avoids all --print-to-pdf KaTeX layout issues.
set -euo pipefail
HTML="${1:?Usage: $0 <html-file> [output.pdf]}"
OUTPUT="${2:-${HTML%.html}.pdf}"
HTML_ABS="$(realpath "$HTML")"
OUTPUT_ABS="$(realpath -m "$OUTPUT")"
SCRATCH="/mnt/c/Users/trade/Downloads/_htmlppt_$$"
mkdir -p "$SCRATCH"
trap "rm -rf $SCRATCH" EXIT

echo "📄 Screenshot PDF: $HTML → $OUTPUT"

# Count slides
SLIDE_COUNT=$(grep -c '<section class="slide' "$HTML_ABS" || echo "0")
echo "  Found $SLIDE_COUNT slides"

# Start HTTP server
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SCRIPT_DIR"
python3 -m http.server 9877 &
SERVER_PID=$!
sleep 1

REL_PATH="$(realpath --relative-to="$SCRIPT_DIR" "$HTML_ABS")"

for i in $(seq 1 $SLIDE_COUNT); do
  echo "  Slide $i/$SLIDE_COUNT..."
  "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe" \
    --headless=new \
    --screenshot="C:\\Users\\trade\\Downloads\\_htmlppt_$$\\slide-$(printf '%03d' $i).png" \
    --window-size=1920,1080 \
    "http://localhost:9877/${REL_PATH}#/${i}" 2>/dev/null
done

# Kill server
kill $SERVER_PID 2>/dev/null || true
sleep 0.5

# Combine with img2pdf (handles PNG→PDF better than PIL)
echo "  Combining into PDF..."
python3 -c "
import img2pdf, glob, os
files = sorted(glob.glob('$SCRATCH/slide-*.png'))
if not files:
    print('❌ No screenshots found')
    exit(1)
with open('$OUTPUT_ABS', 'wb') as f:
    f.write(img2pdf.convert(files))
size_kb = os.path.getsize('$OUTPUT_ABS') / 1024
print(f'✅ {size_kb:.0f}KB, {len(files)} pages')
"
echo "✅ $(du -h "$OUTPUT_ABS" | cut -f1)"
