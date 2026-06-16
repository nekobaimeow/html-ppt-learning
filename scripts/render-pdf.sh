#!/usr/bin/env bash
# html-ppt-learning :: render-pdf.sh
# Render any HTML learning deck to a single A4 PDF via headless Chrome.
# Works on WSL (via Windows Chrome) and native Linux.
#
# Usage:
#   ./scripts/render-pdf.sh examples/os-memory/index.html
#   ./scripts/render-pdf.sh examples/os-memory/index.html os-memory.pdf

set -euo pipefail

HTML="${1:?Usage: $0 <html-file> [output.pdf]}"
OUTPUT="${2:-${HTML%.html}.pdf}"

HTML_ABS="$(realpath "$HTML")"
OUTPUT_ABS="$(realpath -m "$OUTPUT")"

echo "📄 $HTML_ABS"
echo "📁 $OUTPUT_ABS"

if grep -qi microsoft /proc/version 2>/dev/null; then
  # WSL: use Windows Chrome via wsl.localhost paths
  HTML_URL="file://wsl.localhost/Ubuntu${HTML_ABS}"
  OUTPUT_WIN="$(wslpath -w "$OUTPUT_ABS")"

  powershell.exe -Command "Start-Process -FilePath 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList '--headless','--disable-gpu','--no-sandbox','--print-to-pdf=$OUTPUT_WIN','--no-pdf-header-footer','$HTML_URL' -Wait -WindowStyle Hidden" 2>/dev/null
else
  # Native Linux
  CHROME=$(command -v google-chrome || command -v chromium-browser || command -v chromium || echo "")
  [ -z "$CHROME" ] && { echo "❌ Chrome not found"; exit 1; }
  "$CHROME" --headless --disable-gpu --no-sandbox \
    --print-to-pdf="$OUTPUT_ABS" --no-pdf-header-footer \
    "file://$HTML_ABS" 2>/dev/null
fi

if [ -f "$OUTPUT_ABS" ] && [ -s "$OUTPUT_ABS" ]; then
  echo "✅ $(du -h "$OUTPUT_ABS" | cut -f1)"
else
  echo "❌ PDF generation failed"
  exit 1
fi
