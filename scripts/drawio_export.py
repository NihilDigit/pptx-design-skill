#!/usr/bin/env python3
"""Cross-platform drawio export script.

Supports: Linux, macOS, Windows.
Formats: png (all platforms), emf (Linux only, requires pdftocairo + inkscape), svg, pdf.

Usage:
    python drawio_export.py <input> <output_dir> [--format png|emf|svg|pdf] [--scale N] [--filter PATTERN]

Examples:
    python drawio_export.py diagram.drawio build/
    python drawio_export.py diagrams/ build/ --format png --scale 2
    python drawio_export.py diagrams/ build/ --format emf
    python drawio_export.py diagrams/ build/ --filter p4
"""
import argparse
import os
import platform
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def find_drawio_cli() -> str | None:
    """Auto-detect drawio CLI path based on platform."""
    system = platform.system()
    candidates = []
    if system == "Linux":
        candidates = ["drawio", "/usr/bin/drawio", "/opt/drawio/drawio",
                       "/snap/bin/drawio", "/usr/local/bin/drawio"]
    elif system == "Darwin":
        candidates = [
            "/Applications/draw.io.app/Contents/MacOS/draw.io",
            os.path.expanduser("~/Applications/draw.io.app/Contents/MacOS/draw.io"),
            "drawio",
        ]
    elif system == "Windows":
        candidates = [
            r"C:\Program Files\draw.io\draw.io.exe",
            r"C:\Program Files (x86)\draw.io\draw.io.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\draw.io\draw.io.exe"),
            "draw.io.exe",
        ]
    for c in candidates:
        if shutil.which(c) or os.path.isfile(c):
            return c
    return None


def convert_to_png(drawio_cli: str, src: Path, dst_dir: Path, scale: int = 2) -> Path:
    out = dst_dir / f"{src.stem}.png"
    subprocess.run(
        [drawio_cli, "--export", "--format", "png", "--scale", str(scale),
         "--crop", "--output", str(out), str(src)],
        capture_output=True, check=True,
    )
    return out


def convert_to_svg(drawio_cli: str, src: Path, dst_dir: Path) -> Path:
    out = dst_dir / f"{src.stem}.svg"
    subprocess.run(
        [drawio_cli, "--export", "--format", "svg", "--crop",
         "--output", str(out), str(src)],
        capture_output=True, check=True,
    )
    return out


def convert_to_pdf(drawio_cli: str, src: Path, dst_dir: Path) -> Path:
    out = dst_dir / f"{src.stem}.pdf"
    subprocess.run(
        [drawio_cli, "--export", "--format", "pdf", "--crop",
         "--output", str(out), str(src)],
        capture_output=True, check=True,
    )
    return out


def convert_to_emf(drawio_cli: str, src: Path, dst_dir: Path) -> Path:
    """EMF conversion: drawio → PDF → SVG → EMF. Linux only."""
    if platform.system() != "Linux":
        print(f"  [{src.stem}] EMF export requires Linux (pdftocairo + inkscape). Use --format png instead.")
        sys.exit(1)
    for tool in ("pdftocairo", "inkscape"):
        if not shutil.which(tool):
            print(f"  [{src.stem}] Missing dependency: {tool}")
            sys.exit(1)

    pdf = dst_dir / f"{src.stem}.pdf"
    svg = dst_dir / f"{src.stem}.svg"
    emf = dst_dir / f"{src.stem}.emf"

    subprocess.run(
        [drawio_cli, "--export", "--format", "pdf", "--crop",
         "--output", str(pdf), str(src)],
        capture_output=True, check=True,
    )
    subprocess.run(["pdftocairo", "-svg", str(pdf), str(svg)], check=True)
    subprocess.run(
        ["inkscape", str(svg), "--export-type=emf", f"--export-filename={emf}"],
        capture_output=True, check=True,
    )
    return emf


CONVERTERS = {
    "png": convert_to_png,
    "svg": convert_to_svg,
    "pdf": convert_to_pdf,
    "emf": convert_to_emf,
}


def main():
    parser = argparse.ArgumentParser(description="Cross-platform drawio export")
    parser.add_argument("input", help="Single .drawio file or directory of .drawio files")
    parser.add_argument("output_dir", help="Output directory for exported files")
    parser.add_argument("--format", choices=CONVERTERS.keys(), default="png")
    parser.add_argument("--scale", type=int, default=2, help="Scale factor for PNG export")
    parser.add_argument("--filter", default="", help="Only process files matching this substring")
    parser.add_argument("--jobs", type=int, default=3, help="Max parallel conversions")
    args = parser.parse_args()

    cli = find_drawio_cli()
    if not cli:
        print("drawio CLI not found. Install draw.io Desktop from https://github.com/jgraph/drawio-desktop/releases")
        sys.exit(1)
    print(f"Using drawio: {cli}")

    dst = Path(args.output_dir)
    dst.mkdir(parents=True, exist_ok=True)

    inp = Path(args.input)
    if inp.is_file():
        sources = [inp]
    else:
        sources = sorted(inp.glob("*.drawio"))

    if args.filter:
        sources = [s for s in sources if args.filter in s.stem]

    if not sources:
        print("No .drawio files found.")
        return

    converter = CONVERTERS[args.format]
    print(f"Converting {len(sources)} file(s) to {args.format.upper()}")

    def do_convert(src: Path) -> tuple[str, str]:
        try:
            if args.format == "png":
                out = converter(cli, src, dst, args.scale)
            else:
                out = converter(cli, src, dst)
            size = out.stat().st_size
            return src.stem, f"ok ({size // 1024}KB)"
        except subprocess.CalledProcessError as e:
            return src.stem, f"FAILED: {e}"

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(do_convert, s): s for s in sources}
        for f in as_completed(futures):
            name, status = f.result()
            print(f"  [{name}] {status}")

    print(f"Done. Output: {dst}")


if __name__ == "__main__":
    main()
