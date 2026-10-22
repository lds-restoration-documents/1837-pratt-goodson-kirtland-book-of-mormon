# Audit spec — restoring silent corrections in an existing transcription

Used when a batch of pages needs a second pass against the scan. `<WORKDIR>` is the directory produced by `tools/prepare_images.py`.

Context: `book-of-mormon-1837-pages/page-NNN.md` are transcriptions of the 1837 Pratt & Goodson (Kirtland) second edition of the Book of Mormon (public domain), from the page images in `source/NNN.jpg`.
A model transcribing this text is likely to SILENTLY CORRECT what the scan shows toward what it remembers of later editions
(modern punctuation, versification, "corrected" grammar, spellings, names, or wording, or toward the 1830 or modern text). The rule is: the file
must show EXACTLY what is printed on the page image, including printer's errors, odd spellings, odd punctuation and capitalization,
and the 1837 paragraphing. See `tools/transcription-spec.md` for the file format.

Inputs per image N (NNNN = 4-digit, NNN = 3-digit) in `<WORKDIR>`: `img/pNNNN_1_top.jpg`, `img/pNNNN_2_middle.jpg`, `img/pNNNN_3_bottom.jpg` (three bands, slight overlap
at the joins), `img/pNNNN_0_overview.jpg` (layout only). There is no OCR. The original is `source/NNN.jpg`.
If the bands are too small to settle a doubtful spot, make upscaled bands: `python3 tools/prepare_images.py --pages N --zoom 3 --out work/zoom` (an upscale adds no information, but helps the eye).

## Per-page procedure

1. View all three bands (overview only if layout unclear). Read the existing `page-NNN.md`.
2. Compare line by line. Look especially for:
   - words, spellings, names, capitalization and punctuation changed from print (printer's typos silently fixed, modern spellings substituted);
   - punctuation added, removed or "normalized" (the 1837 text has ordinary punctuation of its time; record it as printed); the thin space the type puts before `; : ? !` is NOT checked: the files have none;
   - paragraph breaks added or removed, or a paragraph split/merged at a page break without the correct `<!-- cont -->` marker;
   - words dropped, repeated or added, whole lines missing, lines out of order;
   - headings, chapter numbers, running heads, signature marks and folios changed from what is printed;
   - specks and blemishes transcribed as if they were text (ignore marks that do not read as a deliberate mark or letter; see the transcription spec);
   - italics missing/added;
   - line-end hyphenations not joined, or compound hyphens wrongly joined.
3. For every discrepancy, edit the page file (minimal change, never rewrite the whole file) so it matches the scan exactly.
   If the scan is genuinely unreadable at that spot, leave the existing reading and make sure it carries an
   `<!-- uncertain: ... -->` comment (add one if missing). Do not add uncertain comments to readings you can read clearly.
   Do NOT fix real errors by "improving" them: if the scan prints "assemby", the file must say "assemby".
   Keep existing uncertain/layout comments unless you verified them and they are now wrong.
4. If a change log was requested, append an entry after each page: `## Image NNN`, then either `- no changes` or one line per
   change: `- <where>: was "<old>" -> now "<new>" (<reason>)`. A log also lets an interrupted run resume by skipping logged pages.

CRITICAL: if the image tool fails or errors for a page, do not guess; skip that page, do not record it as audited,
and list it as failed. If you hit an API/usage-limit error, just stop. Final reply: images audited, total changes, pages failed (brief).

## Disk space

The disk is nearly full. Create band images only for your own batch, and when you finish (or stop), delete them: `python3 tools/prepare_images.py --pages A-B --clean` (add `--out <dir>` if you used one). Make zoom images only for a doubtful spot and delete them right after.
