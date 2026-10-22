# Transcription spec — 1837 P. P. Pratt & J. Goodson (Kirtland) Book of Mormon

These are the instructions for the transcribing agents, one batch of images at a time.
`<WORKDIR>` is the directory produced by `tools/prepare_images.py` (default `work/`). The scan is `source/NNN.jpg`, one printed page per image, 619 images, with no text layer and no OCR.

Inputs for image N (NNNN = 4-digit zero-padded) in `<WORKDIR>`:
- `img/pNNNN_0_overview.jpg`: whole page, low-res (layout only)
- `img/pNNNN_1_top.jpg`, `img/pNNNN_2_middle.jpg`, `img/pNNNN_3_bottom.jpg`: readable bands of the page
  (neighbouring bands overlap slightly; do not duplicate lines that appear in two bands)
- `source/NNN.jpg`: the original full-size image, which is authoritative.

Output: `book-of-mormon-1837-pages/page-NNN.md` (3-digit zero-padded image number, e.g. `page-021.md`).
File numbers are image numbers, not the printed folios (printed folio = image + 2 in the main text; see `transcription-notes.md` §1).

Procedure per page: read the overview, then the three bands; write the text.
Read carefully; accuracy matters more than speed. Transcribe exactly what is printed: 1837 spelling, punctuation,
capitalization, abbreviations (`&c.`), run-together or split words. The text is much more heavily punctuated than the 1830 edition and is set in
shorter paragraphs; record what is printed and never normalize it.
Words split across lines by a hyphen are JOINED into the whole word; words hyphenated in the original stay hyphenated.
The edition has no verse numbers and no marginal notes. Do not add either.

## Markdown format

```
<!-- image NNN -->
**Header:** BOOK OF ALMA. | 277        <- running head as printed, parts separated by " | " (omit line if none)

# THE FIRST BOOK OF NEPHI:                <- book titles as #, with any printed subtitle as plain or italic text as printed

## CHAPTER II.                           <- chapter headings as ## (numerals as printed: this edition has both `CHAPTER 1.` and `CHAPTER II.`)

AND it came to pass that ...             <- one paragraph per printed paragraph (blank line between)

---

Footer: B                                <- printer's signature mark, catchword or folio not already in the Header (omit if none)
```

Rules:
- One markdown paragraph per printed paragraph. A printed paragraph starts with an indented first line; text that merely wraps is the same paragraph.
- **Paragraphs across page breaks.** If the first paragraph on the page is the continuation of a paragraph begun on the previous page, start that line with `<!-- cont -->` (e.g. `<!-- cont --> ly went on ...`). `tools/compile_markdown.py` uses this marker to rejoin the paragraph. Do not put it on a paragraph that starts on the page. If the page ends mid-paragraph, write the fragment; the next page carries the marker.
- Keep the printed capitalization of paragraph openings, which often start with all-caps or a large initial ("AND it came to pass"). Write the full first word.
- Italic type is `*italic*`; check carefully for it. Small caps printed as capitals are written as capitals.
- Headings: write the book title, chapter heading and any subtitle as printed.
- **Decorative rules and ornaments.** Chapters are separated by a printed ornament (a small centred rule or flourish). Record it with a comment such as `<!-- decorative ornament printed above the chapter heading -->` on its own line directly above the `## CHAPTER` line (describe the ornament briefly the first time it appears, and keep the wording the same afterwards). Record it only where it is printed: a chapter heading at the very top of a page often has none. Other ornaments are noted briefly in a comment, not transcribed.
- **Chapter summaries.** Chapters open with a printed summary ("An account of Lehi and his wife Sariah…"). Check whether each is set in italics (the 1 Nephi summary is): write it as one italic paragraph (`*…*`) directly under the chapter heading, keeping its spelling and punctuation.
- **Running heads.** Most pages have a running head with the book name (small caps, write as capitals) and the printed page number, the number on the left on even-numbered pages and on the right on odd ones: `**Header:** 6 | FIRST BOOK OF NEPHI.` / `**Header:** FIRST BOOK OF NEPHI. | 7`. Pages that open a book (title, subtitle, chapter heading) have no running head and no `Header:` line.
- **Printed page number = image + 2** in the main text (image 10 prints "12", image 300 prints "302", image 617 prints "619"; the Preface runs on images 3–4, printed v and vi, and 1 Nephi opens on image 5 = printed p. 7, where no number is shown). This is only a cross-check: always record the number as it appears in the scan.
- **Spacing before punctuation.** The type has a thin space before `;`, `:`, `?` and `!` in many places, but it is typesetting, not text, and it cannot be judged reliably at this size. Write NO space before `; : ? !` (`life; and`, `saying: Blessed`). All the punctuation marks themselves, their order, and the capital after a colon are kept exactly as printed.
- **Text cut off by the scan edge.** If the scan itself trims the page, write the visible fragment of each line exactly as it appears (for example `the`, `get t`), never complete it from memory of the text, and say so in a comment at the top of the page. Do not use `[illegible]` for text that is simply cut off. Keep a clipped letter if about half or more of it is visible and drop a mere sliver; a word that is only partly clipped but still readable is written whole. Put a comment at the top of the page saying which edge is trimmed.
- **A new book opening mid-page.** Put the ornament comment above the book title, then the `# THE SECOND BOOK OF NEPHI.`-style title, `## CHAPTER I.` and the italic summary. The page keeps the running head of the book it started in; note that in a comment. A rule is recorded only where it is actually printed: a chapter heading at the very top of a page often has none, so write no ornament comment there.
- **Front and back matter (title page, verso, Preface, testimonies, notices).** Transcribe in full, as plain lines or paragraphs as printed, with an HTML comment noting layout (centering, type sizes, rules). Any handwritten annotation or stamp is described in a comment only, not transcribed as text. A page with nothing to read is just the page comment and a one-line description. The title page is written as stacked lines in the printed order and capitalization, with a layout comment (centering, type sizes, rules); a display word split at a line end is joined (`MOR-/MON` becomes `MORMON`).
- **Hyphens at a line end that split an already hyphenated word or compound.** Let the printing decide: if the same word appears mid-line elsewhere in the page files (grep for it), follow that; names keep their own hyphens (`Maher-shalal-hash-baz`). If nothing settles it, close the word up and add a one-line comment only when the break is truly ambiguous.
- **Small caps versus ordinary type.** Opening words in small caps (`AND`, `THE`) are written in capitals; a word that is merely capitalized in ordinary type is written with its printed case (`And now`). Check the scan before choosing.
- **Specks, bleed-through and blemishes.** This is a low-resolution bitonal scan with noise. Ink specks, dotted lines of dirt, mirror-image text bleeding through from the reverse side of the leaf (often at the bottom or in the margins), worn or filled-in type and stray dots near the trim edge are not text. A mark that does not read as a deliberate punctuation mark or letter is ignored: do not transcribe it and do not add a comment (e.g. a speck after a comma, "seen,."). Use `<!-- uncertain: … -->` only when a real mark or letter is in doubt (is it a comma or a period? an e or an o?).
- **Comma versus period when the mark is uncertain.** Use the gap after the mark and the case of the next word: more space and a capitalized word = period; less space and a lowercase word = comma (an educated guess for uncertain marks only; a mark that is plainly one or the other is written as it is). See `tools/proofread-spec.md` for the full rule.
- **Flush-left versus indented.** Decide whether the first line of the page is indented (new paragraph) or flush-left (continuation of the previous page's paragraph, which may begin a new sentence). Mark a flush-left first line with `<!-- cont -->` even when the previous page ended with a full stop.
- **Hyphens at the end of a page.** If the last line ends in a hyphenated word break, keep the hyphen (`vis-`) on this page and begin the next page with `<!-- cont --> ions …`; `compile_markdown.py` closes the word up. Hyphens at the end of a line inside the page are joined by the transcriber.
- Preliminary and closing matter (title page, preface, testimonies of the witnesses, contents, errata, endpapers): transcribe as printed with sensible markdown; center or layout-only features are noted in an HTML comment.
- Footer items (signature marks, catchwords, printed page numbers if not in the Header) go on a `Footer:` line after a `---` rule.
- Blank pages, notices, stamps, marginalia and pencil notes: describe briefly in an HTML comment and transcribe any legible text.
- Do not add commentary, summaries, or modern corrections. If a word is truly illegible write `[illegible]`.

## Addenda

Never silently "correct" a reading to what you think it should be, whether from knowledge of the 1830 or later editions of the Book of Mormon,
the King James Bible, or the Original or Printer's Manuscript. Write what the scan shows. Printer's errors, odd spellings,
missing or doubled words, damaged type and wrong running heads are all kept as printed. If a reading is doubtful, keep your best
reading and add an HTML comment right after it, e.g. `Zarahemla <!-- uncertain: maybe Zarahenla -->`.

Do not "fix" the 1837 punctuation or paragraphing to match the 1830 or modern editions: this is the 1837 text, as printed, with its own punctuation and paragraph divisions.

## How the agents are run (not part of the spec they see)

- The agent must view the band images for every page. If the image tool fails, it stops and reports the page as failed; transcribing without viewing the images is not allowed.
- Images are processed in batches of 16, one page at a time, writing each file right after reading it; a batch skips pages whose output file already exists, so an interrupted batch can resume.

## Disk space

The disk is nearly full. Create band images only for your own batch, and when you finish (or stop), delete them: `python3 tools/prepare_images.py --pages A-B --clean` (add `--out <dir>` if you used one). Make zoom images only for a doubtful spot and delete them right after.
