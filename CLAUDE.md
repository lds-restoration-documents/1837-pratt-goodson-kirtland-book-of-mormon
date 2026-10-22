# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A text corpus, not software: AI-assisted transcriptions of the 1837 second edition of the Book of Mormon (Kirtland, Ohio: printed by O. Cowdery & Co. for P. P. Pratt and J. Goodson), extracted from the Internet Archive scan https://archive.org/details/BookOfMormon1837KirtlandEdition. The scan is **619 JPG page images** (`source/001.jpg` … `619.jpg`, about 1160x2200, grayscale, bitonal-looking, one printed page per image) with **no text layer and no OCR**. `source/` is gitignored and not part of the repo (the redundant `_AllFiles.zip` download has been deleted). There is no build, lint, or test tooling. The methodology and tooling are adapted from the sibling projects `../1830-grandin-palmyra-book-of-mormon` (process; the most mature) and `../1833-phelps-zion-book-of-commandments` (OCR-free, `check_structure.py`). Read their `transcription-notes.md` "gotchas" before changing the method.

**Status:** project set up; all 619 images (1–619) transcribed, audited once and blind-proofread once (finished 2026-10-22; see `transcription-notes.md` §6b). The owner review of the close calls (§6c, a list of unresolved colon/semicolon marks), the typo catalog and a full human proofread are NOT done. Layout (see `transcription-notes.md` §1): image 1 title page; 2 title-page verso (copyright notice); 3–4 Preface (printed v–vi); 5 opening of 1 Nephi (no folio shown); Book of Mormon text through image 617 (confirmed); 618 testimony of the Three Witnesses; 619 testimony of the Eight Witnesses and "To the Reader". **Printed folio = image number + 2** throughout the main text (image 10 = p. 12, 617 = p. 619); image 5 is p. 7 with no number shown.

## How the files relate

`book-of-mormon-1837-pages/page-001.md` … are the **source of truth**: one file per image, named by *image number* (3 digits), not the printed folio. Everything else is derived:

- `book-of-mormon-1837.md`: all pages, main text only, joined into one file.
- `book-of-mormon-1837.txt`: the same, with all Markdown removed.
- `printer-typos.md`, `uncertain-log.md`: generated catalogs of the printer's slips and of every `uncertain`/layout comment, by image.
- `book-of-mormon-1837-sparse.txt`: Book of Mormon text only (title page, books, chapters, paragraphs; image ranges in `PAGE_RANGES` of `tools/make_sparse.py`: image 1 and images 5–617).
- `transcription-notes.md`: method, conventions, residual-risk notes, and a per-page log of every `uncertain` / `[illegible]` / layout comment.

Rebuild after changing any page file (Python 3 standard library only, run from anywhere):

```
python3 tools/compile_markdown.py   # book-of-mormon-1837.md
python3 tools/make_plaintext.py     # book-of-mormon-1837.txt
python3 tools/make_sparse.py        # book-of-mormon-1837-sparse.txt
python3 tools/check_structure.py [--allow-gaps]   # mechanical page-file checks
```

`tools/prepare_images.py` (needs Pillow: `~/.venvs/lds-transcribe/bin/python`) cuts each `source/NNN.jpg` into an overview and three overlapping bands under `work/img/` (gitignored); `tools/transcription-spec.md`, `tools/audit-spec.md` and `tools/proofread-spec.md` are the instructions the agents follow. See `tools/README.md`.

## Page file format

Each page file starts `<!-- image NNN -->`, then: an optional `**Header:**` running-head line (parts separated by ` | `), headings (`#` book title, `## CHAPTER X.`), and one paragraph per printed paragraph. A paragraph that continues from the previous page starts with `<!-- cont -->`; the compile script uses it to rejoin paragraphs. After a `---` rule, an optional `Footer:` line holds signature marks / catchwords. Full details are in `tools/transcription-spec.md`.

This edition has **no verse numbers, no marginal notes, one wide column**, shorter paragraphs and ordinary punctuation (unlike the sparse 1830 text), italic chapter summaries, chapter headings numbered both `CHAPTER 1.` and `CHAPTER II.` (record as printed), and an ornament between chapters. The type may put a thin space before `; : ? !`, which we do NOT transcribe (write none). Page-top paragraph continuations may be flush-left: a flush-left first line gets `<!-- cont -->`. Do not add verse numbers, modern punctuation or paragraph breaks, and do not bring in readings from the 1830 or later editions.

## Rules when editing

- **Write what the scan shows, never what you think it should say.** Printer's errors, odd spellings, names, grammar, missing or doubled words, damaged type and wrong running heads are kept as printed. Do not "fix" them from knowledge of the 1830 or later editions, the King James Bible, or the manuscripts.
- Doubtful readings stay in place with `<!-- uncertain: … -->`; unreadable text is `[illegible]`.
- The scan is low-resolution and noisy: specks, dotted dirt lines and mirror-image bleed-through from the reverse of the leaf are not text. Upscaling a crop adds no information; it only helps the eye.
- Never transcribe without viewing the image. If the image tool fails for a page, stop and report that page as failed.
- Work in batches of 16 images, writing each file right after reading its page; skip pages whose output file already exists so interrupted runs can resume.
- Record the model that wrote each range, and which ranges have been audited or proofread, in `transcription-notes.md` §1 and §6. Do not claim a page was audited or proofread when it was not.
- Page files are keyed to image numbers (3-digit, zero-padded). Keep the first-line page comment in sync with the filename.
- **Keep disk use low.** The disk is nearly full. Prepare one batch of images at a time and delete it when done (`python3 tools/prepare_images.py --pages A-B --clean`; also `--out work/proof` after a proofread). Do not leave upscaled/zoom images behind, and write temporary files to the scratchpad, not the repo.
- **Disk watch (found Oct 15):** each 48-image group of subagent work adds ~270 MB to `~/.claude/projects/<this project>/<session>/subagents/` (transcripts that embed the viewed images), far more than the 40 MB of `work/img`. Check `df -h .` before every group; if less than ~600 MB is free, stop and tell the owner rather than starting a group. Do not delete anything under `~/.claude` or the owner's files without asking.
- **No images in tracked files.** The scan images are not committed; generated Markdown (catalogs, notes) must refer to images by number (and the Internet Archive link) and never embed them. Image crops exist only in gitignored `work/` (e.g. `work/review/checklist.html`).
- **Never run `git commit` or `git push`** (the owner does); leave changes uncommitted.
- Front matter and back matter are transcribed in full (title page, verso, Preface, testimonies, "To the Reader").

## Open items

- `README.md` is hand-edited by the owner after drafting: change it in place with small edits.
- Comma versus period (owner's rule, in `tools/proofread-spec.md`): for an uncertain mark, more space + a capitalized next word = period; less space + a lowercase next word = comma.
- `printer-typos.md` (from `tools/make_typo_catalog.py`, curated form list in the script) and `uncertain-log.md` (from `tools/make_uncertain_log.py`) are generated catalogs; rebuild them after page edits. `tools/make_review_checklist.py` (HTML checklist of the unresolved close calls, with image crops) replaces the siblings' review app, which is not ported.
