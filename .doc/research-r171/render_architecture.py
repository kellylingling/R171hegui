from pathlib import Path
import argparse
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET


def main():
    parser = argparse.ArgumentParser(description='Render the R171 SVG architecture with an installed browser.')
    parser.add_argument('--browser', type=Path, default=Path('C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'))
    args = parser.parse_args()
    if not args.browser.is_file():
        parser.error('Browser not found; pass its executable path with --browser.')

    root = Path(__file__).resolve().parents[2]
    out = root / 'diagrams' / '2026-10-11T145500'
    svg = out / 'diagram.svg'
    ET.parse(svg)
    png = out / 'diagram.png'
    html = out / 'preview.html'
    html.write_text('<!doctype html><meta charset="utf-8"><style>html,body{margin:0;width:1440px;height:1020px;overflow:hidden}</style>'+svg.read_text(encoding='utf-8'),encoding='utf-8')
    with tempfile.TemporaryDirectory(prefix='r171-browser-') as profile:
        result = subprocess.run(
            [str(args.browser), '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
             '--disable-extensions', '--allow-file-access-from-files', '--user-data-dir='+profile,
             '--window-size=1440,1020', '--screenshot='+str(png), html.as_uri()],
            timeout=45, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0), capture_output=True,
        )
    if result.returncode or not png.is_file():
        print('Architecture rendering failed.', file=sys.stderr)
        return result.returncode or 1
    print('SVG XML: valid')
    print('PNG:', png.relative_to(root))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
