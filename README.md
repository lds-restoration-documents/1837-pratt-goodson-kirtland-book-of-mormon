# 1837 Pratt & Goodson Kirtland Book of Mormon
[Markdown](#what-is-markdown) & Plain Text extractions of the content of the 1837 (second) edition of the Book of Mormon, printed at Kirtland, Ohio, by O. Cowdery & Co. for P. P. Pratt and J. Goodson. Extracted using AI.

**Status: all 619 images are transcribed, audited once against the scan and then proofread blind by a separate agent. The owner has reviewed the unresolved close calls against the scan (colon versus semicolon and similar); a full human proofread has not been done yet.** Expect remaining errors, especially colon versus semicolon and comma versus period, which are hard to tell apart in this scan.

## Files
* `book-of-mormon-1837.md`: the whole text in a single [Markdown](#what-is-markdown) file. A `<!-- page NNN -->` comment marks where each image begins.
* `book-of-mormon-1837.txt`: the same text as plain text, with no [Markdown](#what-is-markdown).
* `book-of-mormon-1837-sparse.txt`: plain text of the Book of Mormon proper only, leaving out the imprint on the title page, the Preface and the testimonies.
* [book-of-mormon-1837-pages/](book-of-mormon-1837-pages/): one [Markdown](#what-is-markdown) file per image of the scan (`page-001.md` to `page-619.md`). File numbers are image numbers (printed page number = image + 2 in the main text). These are the source of truth; the files above are generated from them.
* `printer-typos.md`: a catalog of the printer's slips and misspellings in the 1837 print, with image, printed page and context (likely, not exhaustive).

## What is in the 1837 edition
* **No verse numbers**, no double columns, no footnotes and no cross-references; text in paragraphs on a single wide column, with italic chapter summaries.
* Spelling, capitalization, punctuation and grammar are kept exactly as printed, **printer's errors included**; nothing has been corrected from other editions.
* Punctuation is **ordinary** (commas, semicolons, colons and periods), much fuller than the sparse punctuation of the 1830 first edition. Quoted speech after a comma often still begins with a lowercase word ("saying, why do ye smite…"), as printed.
* Like the 1830 edition, it has **no later book divisions** (no 3 Nephi, 4 Nephi or Mormon). The books are named as printed: the First and Second Book of Nephi, the Book of Jacob, Enos, Jarom, Omni, the Words of Mormon, Mosiah, Alma, Helaman, then two successive books both headed "The Book of Nephi", then "Book of Mormon", Ether and Moroni.
* Chapters are numbered within each book, in Arabic (`CHAPTER 1.`) at the opening of 1 Nephi and in Roman numerals afterward, as printed. An ornament is printed between chapters.
* The Preface (images 3–4) is a short note from the publishers that refers to the 1830 edition.

## Source
Extracted from the 619 page images (JPG) of the scan hosted by the [Internet Archive](https://archive.org/details/BookOfMormon1837KirtlandEdition). The images are not included in this repository. Image 1 is the title page, 2 its verso, 3–4 the Preface, 5 the opening of 1 Nephi, and the last two images the testimonies of the Three and Eight Witnesses.

## What is Markdown?
Markdown is a simple way of writing formatted text using plain characters, such as `#` for headings and `*asterisks*` for *italics*. A Markdown file is still readable as ordinary text, and can also be displayed with formatting.
* Learn more at [markdown.org](https://markdown.org/).
* Tools for displaying, editing, or converting Markdown files: [https://markdown.org/tools/](https://markdown.org/tools/)

## Artificial Intelligence
Extracted with Claude Code from Anthropic using the Sonnet 5.5 model. Each page is transcribed from images of the scan (there is no text layer or OCR), then checked a second time against the scan by a separate AI agent. A third check by another agent working blind has been done, and the close calls it left open were then decided by the owner from the scan. The text is meant to show what the page shows, so printer's spellings and errors, punctuation, hyphenation and paragraphing are kept. A few things are deliberately **not** reproduced: the thin space the type may put before `;`, `:`, `?` and `!`, and ink specks, stains and bleed-through that are not letters or punctuation.

**This is an AI transcription and has not been proofread by a person.** For anything that matters, check the scan. See [transcription-notes.md](transcription-notes.md) for the details.

The file [uncertain-log.md](uncertain-log.md) lists every doubtful reading and layout note recorded in the transcription, by image.

## Rebuilding the combined files
```
python3 tools/compile_markdown.py   # book-of-mormon-1837.md
python3 tools/make_plaintext.py     # book-of-mormon-1837.txt
python3 tools/make_sparse.py        # book-of-mormon-1837-sparse.txt
python3 tools/make_typo_catalog.py  # printer-typos.md
python3 tools/make_uncertain_log.py # uncertain-log.md
python3 tools/check_structure.py     # mechanical checks of the page files
```
See [tools/README.md](tools/README.md) for the full pipeline.
