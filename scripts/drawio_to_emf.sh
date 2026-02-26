#!/usr/bin/env bash
# drawio_to_emf.sh — Convert .drawio files to EMF via PDF → SVG → EMF pipeline
#
# Dependencies: drawio CLI, pdftocairo (poppler), inkscape
#
# Usage:
#   drawio_to_emf.sh <input.drawio> <output_dir>
#   drawio_to_emf.sh <diagrams_dir> <output_dir>          # batch mode
#   drawio_to_emf.sh <diagrams_dir> <output_dir> [filter]  # selective
#
# Examples:
#   drawio_to_emf.sh diagram.drawio build/
#   drawio_to_emf.sh diagrams/ build/
#   drawio_to_emf.sh diagrams/ build/ p4    # only files matching "p4"
set -euo pipefail

convert_one() {
    local drawio="$1"
    local out_dir="$2"
    local name
    name="$(basename "$drawio" .drawio)"
    local pdf="$out_dir/${name}.pdf"
    local svg="$out_dir/${name}.svg"
    local emf="$out_dir/${name}.emf"

    echo "[$name] drawio → PDF"
    drawio --export --format pdf --crop --output "$pdf" "$drawio" 2>/dev/null

    echo "[$name] PDF → SVG"
    pdftocairo -svg "$pdf" "$svg"

    echo "[$name] SVG → EMF"
    inkscape "$svg" --export-type=emf --export-filename="$emf" 2>/dev/null

    echo "[$name] done ($(du -h "$emf" | cut -f1))"
}

if [[ $# -lt 2 ]]; then
    echo "Usage: drawio_to_emf.sh <input.drawio|diagrams_dir> <output_dir> [filter]"
    exit 1
fi

INPUT="$1"
OUT_DIR="$2"
FILTER="${3:-}"
mkdir -p "$OUT_DIR"

if [[ -f "$INPUT" ]]; then
    # Single file mode
    convert_one "$INPUT" "$OUT_DIR"
else
    # Batch mode
    count=0
    for f in "$INPUT"/*.drawio; do
        [[ ! -f "$f" ]] && continue
        name="$(basename "$f" .drawio)"
        [[ -n "$FILTER" && "$name" != *"$FILTER"* ]] && continue
        convert_one "$f" "$OUT_DIR" &
        count=$((count + 1))
        # Limit concurrency to avoid inkscape DBus conflicts
        (( count % 3 == 0 )) && wait
    done
    wait
    echo "Converted $count diagram(s)"
fi
