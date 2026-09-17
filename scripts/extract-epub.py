#!/usr/bin/env python3
# extract-epub.py — Extract readable text from an EPUB file
# Usage: python3 extract-epub.py <path-to-epub> [output-dir]
# Requires: Python 3 standard library only (no pip packages)
#
# Outputs one .txt file per chapter into output-dir (default: ./extracted/)
# Also prints chapter list with character counts to stdout.
#
# Gotchas:
# - EPUB is just a zip file with XHTML inside. No special libraries needed.
# - Chapter order comes from the OPF spine, not filesystem order.
# - Some EPUBs use .html not .xhtml — this handles both.
# - Images are skipped (we're after text only).

import sys
import os
import re
import html
import zipfile
from xml.etree import ElementTree as ET

def strip_html(text):
    """Remove HTML tags and decode entities."""
    text = re.sub(r'<[^>]+>', '\n', text)
    text = html.unescape(text)
    lines = [l.strip() for l in text.split('\n')]
    text = '\n'.join(lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def extract_epub(epub_path, output_dir='extracted'):
    if not os.path.exists(epub_path):
        print(f"Error: {epub_path} not found")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(epub_path, 'r') as zf:
        # Find the OPF file via container.xml
        container = zf.read('META-INF/container.xml').decode('utf-8')
        opf_match = re.search(r'full-path="([^"]+)"', container)
        if not opf_match:
            print("Error: Can't find OPF file in container.xml")
            sys.exit(1)

        opf_path = opf_match.group(1)
        opf_dir = os.path.dirname(opf_path)
        opf_content = zf.read(opf_path).decode('utf-8')

        # Parse OPF to get spine order
        # Remove namespace for easier parsing
        opf_clean = re.sub(r'\sxmlns="[^"]+"', '', opf_content, count=1)
        root = ET.fromstring(opf_clean)

        # Build id -> href map from manifest
        manifest = {}
        for item in root.findall('.//manifest/item'):
            item_id = item.get('id')
            href = item.get('href')
            media = item.get('media-type', '')
            if 'html' in media or 'xhtml' in media:
                manifest[item_id] = href

        # Get reading order from spine
        spine_ids = [ref.get('idref') for ref in root.findall('.//spine/itemref')]

        chapters = []
        for i, sid in enumerate(spine_ids):
            if sid not in manifest:
                continue
            href = manifest[sid]
            full_path = os.path.join(opf_dir, href) if opf_dir else href
            full_path = full_path.replace('\\', '/')

            try:
                raw = zf.read(full_path).decode('utf-8')
            except KeyError:
                print(f"  Warning: {full_path} not found in archive, skipping")
                continue

            text = strip_html(raw)
            if len(text) < 50:
                continue

            # Determine chapter name from content or filename
            first_line = text.split('\n')[0][:80] if text else os.path.basename(href)
            chapter_name = f"chapter-{i:02d}"

            out_file = os.path.join(output_dir, f"{chapter_name}.txt")
            with open(out_file, 'w') as f:
                f.write(text)

            chapters.append({
                'index': i,
                'name': chapter_name,
                'file': out_file,
                'chars': len(text),
                'preview': first_line
            })

        print(f"\nExtracted {len(chapters)} chapters from: {os.path.basename(epub_path)}\n")
        for ch in chapters:
            print(f"  {ch['name']}: {ch['chars']:,} chars — {ch['preview']}")
        print(f"\nOutput: {os.path.abspath(output_dir)}/")

        return chapters

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 extract-epub.py <path-to-epub> [output-dir]")
        sys.exit(1)

    epub = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else 'extracted'
    extract_epub(epub, outdir)
