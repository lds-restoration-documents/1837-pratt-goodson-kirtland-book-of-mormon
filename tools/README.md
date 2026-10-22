# tools

The scripts and instructions used to produce the files in this repository. The page files in
`../book-of-mormon-1837-pages/` are the source of truth; the combined text files are generated from them.
(Adapted from the sibling `1830-grandin-palmyra-book-of-mormon` and `1833-phelps-zion-book-of-commandments` tooling.)

## Pipeline

1. **Prepare the images** (the scan is `source/NNN.jpg`, not in git; needs Pillow, e.g. `~/.venvs/lds-transcribe/bin/python`):
   `python3 tools/prepare_images.py [--pages 1-16,302] [--zoom 2] [--out work]`
   writes an overview and three overlapping bands per image into `work/img/` (about 0.7 MB per image, so prepare one batch at a time and delete it afterwards with `--clean`, see below). There is no PDF, text layer or OCR; `--zoom` is only an upscale for legibility.
2. **Transcribe**: AI agents (Claude) read the bands and write one `page-NNN.md` per image following
   [transcription-spec.md](transcription-spec.md). Pages are then audited per [audit-spec.md](audit-spec.md) and proofread blind per
   [proofread-spec.md](proofread-spec.md). This step is done by agents, not by a script.
3. **Check**: `python3 tools/check_structure.py [--allow-gaps]` (page comment, `cont` markers, spacing before `; : ? !`, italics, chapter sequence per book, folio = image + 2).
4. **Rebuild the combined files** (standard library only; run in this order; each writes to the repo root, `--out` redirects):
   ```
   python3 tools/compile_markdown.py     # -> book-of-mormon-1837.md
   python3 tools/make_plaintext.py       # -> book-of-mormon-1837.txt
   python3 tools/make_sparse.py          # -> book-of-mormon-1837-sparse.txt
   ```

## Disk space

The disk this repo lives on is nearly full. `work/` is scratch and is gitignored: for each 16-image batch run `prepare_images.py --pages A-B`, transcribe and audit, then `prepare_images.py --pages A-B --clean` (and the same with `--out work/proof` after the proofread). Never prepare all 619 images at once. Keep audit/proofread logs outside `work/img`.

## Notes on the scripts

- `compile_markdown.py` strips comments, running heads, footers and any marginal-notes section, and rejoins paragraphs that run across a page break using the `<!-- cont -->` marker. It aborts if a `<!-- cont -->` has no paragraph to continue.
- `make_sparse.py` keeps only the image ranges in `PAGE_RANGES` (image 1 and images 5–617, confirmed once the text was transcribed) and drops the title-page imprint paragraphs (`IMPRINT_PREFIXES`). Revisit both after the survey in `transcription-notes.md` §1.
- `make_typo_catalog.py` builds `../printer-typos.md` from a curated list in the script (about 100 forms plus recurring and wrong-word sections); `make_uncertain_log.py` builds `../uncertain-log.md` from the comments in the page files.
- `make_review_checklist.py` builds `work/review/checklist.html` (gitignored) from `review_items.json`, the list of unresolved close calls from `transcription-notes.md` §6c: a crop of the scan at each doubtful mark, with keep/change/can't-tell buttons and an export button. Run with `~/.venvs/lds-transcribe/bin/python`. Crops are centred on an estimate, so the mark may be a few lines off centre.
- Not ported: the full review app from the 1830 repo (`review/review_app.py`, which used pypdfium2).
