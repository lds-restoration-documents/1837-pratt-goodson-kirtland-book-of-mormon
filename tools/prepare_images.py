#!/usr/bin/env python3
"""Cut the scan JPGs in source/ into the inputs used for transcription.

The 1837 Book of Mormon scan is one page per JPG (source/NNN.jpg, about 1160x2200, grayscale),
printed in a single full-width column, so each page is cut into three overlapping horizontal bands.

For each image N this writes, under <out>/img/:
  pNNNN_0_overview.jpg   whole page at 1/3 size (layout only)
  pNNNN_1_top.jpg        top band (overlaps the middle band)
  pNNNN_2_middle.jpg     middle band
  pNNNN_3_bottom.jpg     bottom band
With --zoom Z the bands are upscaled by Z (Lanczos) and written under <out> as pNNNN_*_zN.jpg; this adds no
information to the scan, it only makes a doubtful spot easier to read.

There is no text layer or OCR: the scan is images only.

Disk space: a page's overview and bands take roughly 0.7 MB (about 450 MB for all 619), so work in batches and delete
each batch's images when its transcribe/audit/proofread steps are done:
  python3 tools/prepare_images.py --pages 17-32 --clean        # removes work/img files for those images (all zoom variants)
  python3 tools/prepare_images.py --pages 17-32 --clean --out work/proof   # the same for a proofread folder
Only work/img (or the --out folder's img/) is touched; logs elsewhere under work/ are kept.

Requires: Pillow (e.g. ~/.venvs/lds-transcribe/bin/python).

Usage:
  python3 tools/prepare_images.py                       # all images in source/ -> work/
  python3 tools/prepare_images.py --pages 1-16,302
  python3 tools/prepare_images.py --pages 40 --zoom 2 --out work/proof
"""
import argparse
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BANDS = 3
OVERLAP = 0.05  # fraction of page height shared by neighbouring bands


def parse_pages(spec, available):
    if not spec:
        return available
    pages = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            pages.extend(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))
    return pages


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", default=str(ROOT / "source"), help="directory of NNN.jpg scans (default: ./source)")
    ap.add_argument("--out", default=str(ROOT / "work"), help="output directory (default: ./work)")
    ap.add_argument("--pages", help="image numbers, e.g. 1-16,302 (default: all)")
    ap.add_argument("--zoom", type=float, default=1, help="upscale factor for the bands (default: 1, none)")
    ap.add_argument("--clean", action="store_true", help="delete the generated images for --pages (all of them if omitted) and exit")
    args = ap.parse_args()

    if args.clean:
        d = Path(args.out) / "img"
        pages = parse_pages(args.pages, sorted(int(f.name[1:5]) for f in d.glob("p[0-9][0-9][0-9][0-9]_*.jpg")))
        n = 0
        for p in pages:
            for f in d.glob(f"p{p:04d}_*.jpg"):
                f.unlink()
                n += 1
        print(f"removed {n} files from {d}")
        return

    src = Path(args.source)
    out = Path(args.out) / "img"
    out.mkdir(parents=True, exist_ok=True)
    available = sorted(int(p.stem) for p in src.glob("[0-9][0-9][0-9].jpg"))
    suffix = "" if args.zoom == 1 else f"_z{args.zoom:g}"

    for n in parse_pages(args.pages, available):
        f = src / f"{n:03d}.jpg"
        if not f.exists():
            print(f"missing {f}")
            continue
        im = Image.open(f).convert("RGB")
        w, h = im.size
        if args.zoom == 1:
            im.resize((w // 3, h // 3), Image.LANCZOS).save(out / f"p{n:04d}_0_overview.jpg", quality=70)
        step = h / BANDS
        pad = h * OVERLAP
        for i, name in enumerate(("1_top", "2_middle", "3_bottom")):
            top = max(0, int(i * step - pad))
            bot = min(h, int((i + 1) * step + pad))
            band = im.crop((0, top, w, bot))
            if args.zoom != 1:
                band = band.resize((int(band.width * args.zoom), int(band.height * args.zoom)), Image.LANCZOS)
            band.save(out / f"p{n:04d}_{name}{suffix}.jpg", quality=85)


if __name__ == "__main__":
    main()
