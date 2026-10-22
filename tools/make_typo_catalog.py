#!/usr/bin/env python3
"""Build printer-typos.md: a catalog of the likely printer's typos and misspellings in the 1837 text.

The list of forms is curated below (triaged from a dictionary scan of the compiled text plus the audit notes); this script
finds every occurrence of each form in book-of-mormon-1837.md, with its image and a snippet of context, so the page
numbers and contexts always come from the current text. Spellings that were normal or intentional for the period or the edition
(shew, sayeth, marvellous, ...) are deliberately NOT cataloged; see the NOT_INCLUDED notes at the end of the output.

Usage:  python3 tools/make_typo_catalog.py [--md FILE] [--out FILE]
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (printed, should be, note). `printed` is matched as a whole word, case-sensitive; a tuple (regex, label) matches a pattern.
SECTIONS = [
    ('Letters dropped, added or wrong (single-word slips)', [
        (w, sh, n) for w, sh, n in [
            ('abhorence', 'abhorrence', ''), ('abont', 'about', ''), ('accordidg', 'according', ''),
            ('aquainted', 'acquainted', ''), ('assension', 'ascension', ''), ('asssuredly', 'assuredly', 'three s\'s'),
            ('aud', 'and', ''), ('bablings', 'babblings', ''), ('beeause', 'because', 'worn type'),
            ('beginnig', 'beginning', ''), ('beleiveth', 'believeth', 'ei/ie'), ('blesseed', 'blessed', ''),
            ('bloodsheads', 'bloodsheds', ''), ('cannnot', 'cannot', ''), ('chatisement', 'chastisement', ''),
            ('chnrch', 'church', 'worn type'), ('ciy', 'city', ''), ('commannments', 'commandments', ''),
            ('concernig', 'concerning', ''), ('construotion', 'construction', 'worn c'), ('convenant', 'covenant', ''),
            ('deliever', 'deliver', ''), ('desecendant', 'descendant', ''), ('despersed', 'dispersed', ''),
            ('destry', 'destroy', ''), ('destsoyed', 'destroyed', ''), ('destructruction', 'destruction', 'printed "destruc-/truction"'),
            ('druken', 'drunken', ''), ('eatheth', 'eateth', ''), ('espistle', 'epistle', ''),
            ('exceding', 'exceeding', ''), ('exeeeding', 'exceeding', 'worn c'), ('exceeeding', 'exceeding', ''),
            ('eyss', 'eyes', ''), ('fiirst', 'first', ''), ('forgivenss', 'forgiveness', ''), ('fouud', 'found', 'worn n'),
            ('fufilling', 'fulfilling', ''), ('gnerations', 'generations', ''), ('hanhs', 'hands', ''),
            ('heaarken', 'hearken', ''), ('heheld', 'beheld', 'worn b'), ('hithero', 'hitherto', ''),
            ('immtorality', 'immortality', ''), ('kearken', 'hearken', ''), ('kinggom', 'kingdom', ''),
            ('knowldege', 'knowledge', ''), ('martydom', 'martyrdom', ''), ('mankid', 'mankind', ''),
            ('mght', 'might', ''), ('ministery', 'ministry', ''), ('nineteeth', 'nineteenth', ''),
            ('nnto', 'unto', 'worn u'), ('notwitstanding', 'notwithstanding', ''), ('notwsthstanding', 'notwithstanding', 'worn i'),
            ('oecame', 'became', 'worn b'), ('ootained', 'obtained', 'worn b'), ('ot', 'of', 'worn f'),
            ('passsed', 'passed', ''), ('peopel', 'people', ''), ('preceive', 'perceive', ''),
            ('proyhesy', 'prophesy', ''), ('recived', 'received', ''), ('rejcted', 'rejected', ''),
            ('rememember', 'remember', ''), ('rememher', 'remember', 'worn b'), ('rerurned', 'returned', ''),
            ('retaing', 'retaining', ''), ('returued', 'returned', 'worn n'), ('righteons', 'righteous', 'worn u'),
            ('sevant', 'servant', ''), ('shll', 'shall', ''), ('solldier', 'soldier', ''), ('sothward', 'southward', ''),
            ('spaee', 'space', 'worn c'), ('spreaking', 'speaking', ''), ('statagem', 'stratagem', ''),
            ('stubborness', 'stubbornness', ''), ('sufice', 'suffice', ''), ('suredly', 'assuredly', ''),
            ('tanslated', 'translated', ''), ('thands', 'thanks', ''), ('thay', 'they', ''), ('themelves', 'themselves', ''),
            ('thht', 'that', ''), ('thoudands', 'thousands', ''), ('thoughout', 'throughout', ''),
            ('tragressor', 'transgressor', ''), ('unbelif', 'unbelief', ''), ('warior', 'warrior', ''),
            ('weakneess', 'weakness', ''), ('wher', 'where', ''), ('wich', 'which', ''), ('wickednes', 'wickedness', ''),
            ('wildeness', 'wilderness', ''), ('wildernes', 'wilderness', ''), ('wildesness', 'wilderness', ''),
            ('emitten', 'smitten', 'judgment call'), ('hm', 'him', 'printed "hm", the i missing'),
            ('trampeleth', 'trampleth', ''), ('seige', 'siege', 'period spelling variant'),
        ]]),
    ('Words run together or split', [
        ('theNephites', 'the Nephites', 'no space printed'), ('untoyou', 'unto you', 'no space printed'),
        ('ofking', 'of king', 'no space printed'),
    ]),
    ('Wrong, missing or doubled words (grammar slips kept as printed)', [
        (('this it not the case', 'this it not'), 'this is not', ''),
        (('therefore us they were', 'therefore us they'), 'therefore as they', ''),
        (('had began', 'had began'), 'had begun', ''),
        (('ye had ought', 'ye had ought'), 'ye ought', ''),
        (('to not come', 'to not come'), 'not to come', ''),
        (('never was men', 'never was men'), 'never were men', ''),
        (('of the which we had retained', 'of the which'), 'of which', ''),
        (('there was but few', 'there was but few'), 'there were but few', ''),
        (('did care not for', 'did care not for'), 'did not care for', ''),
        (('they were died in blood', 'were died'), 'had died', ''),
        (('be fell', 'be fell'), 'befell', ''),
        (('partake or their spoils', 'partake or'), 'partake of', ''),
        (('a more part', 'a more part'), 'the more part', ''),
        (('for, for this intent', 'for, for'), 'for this intent', 'doubled word'),
        (('are are the merciful', 'are are'), 'are the merciful', 'doubled word'),
        (('who is heaven', 'who is heaven'), 'who is in heaven', ''),
        (('I say unto, he that', 'I say unto, he'), 'I say unto you, he that', ''),
        (('wo be unto because', 'wo be unto because'), 'wo be unto you because', ''),
        (('concerning this five', 'concerning this five'), 'concerning these five', ''),
        (('looking for of', 'looking for of'), 'looking for', ''),
        (('a a spokesman', 'a a spokesman'), 'a spokesman', 'doubled word'),
        (('of of mine enemy', 'of of mine'), 'of mine enemy', 'doubled word'),
        (('in the which Teancum', 'in the which'), 'in which', ''),
    ]),
]

# Misspellings that recur (the same slip printed several times): listed in their own section, with all pages.
RECURRING = [
    ('harrass', ['harrass'], 'harass', 'single r/ss; 389-391'),
    ('assunder', ['assunder'], 'asunder', 'doubled s; 47, 435, 442'),
    ('arriven', ['arriven'], 'arrived', 'ven for ved; 186, 297, 466'),
    ('dilligence', ['dilligence'], 'diligence', 'doubled l; 22, 490'),
    ('judgement(s)', ['judgement', 'judgements'], 'judgment(s)', 'period variant, 45-70'),
]

NOT_INCLUDED = """## Not included: spellings that were normal or intentional

Spellings that were normal or intentional for 1837 are not printer's slips and are left out of the catalog: `shew`/`shewed`/`shewn`/`sheweth`, `annoint(ed)`, `burthen(s)`, `centre`, `sepulchre`, `vapour`, `armour`, `lustre`, `mouldering`, `moulten`, `travelling`, `counselled`/`counsellor`, `quarrellings`, `offence`, `wilfully`/`wilfulness`, `baptise(d)`, `judgement(s)` (listed above only as a recurring variant), `journied`, `phrensied`, `stiffnecked(ness)`, `to-day`/`to-morrow`, `dependant`, `dissention`, `existance`, `desirious`, `unchangable`/`changable`, `befal`, `wrapt`, `cymeter`/`cimeter` and the like. Names are not catalogued either; the transcription keeps the printed form of every name (e.g. `Gidgiddoni`, `Lachoneus`, `Sherrizah`, `Amalickhiah`, `Amalcikiah`).
"""


def load(md):
    raw = md.read_text(encoding='utf-8')
    parts = re.split(r'<!-- page (\d+) -->', raw)
    segs, cur = [], 0
    for i, t in enumerate(parts):
        if i % 2 == 1:
            cur = int(t)
            continue
        t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
        segs.append((cur, re.sub(r'\s+', ' ', t)))
    return segs


def find(segs, spec):
    """Yield (page, snippet) for each occurrence."""
    if isinstance(spec, tuple):
        pat, hit = spec
        rx = re.compile(re.escape(pat))
        hl = hit
    else:
        rx = re.compile(r'(?<![A-Za-z])' + re.escape(spec) + r'(?![A-Za-z])')
        hl = spec
    for pg, t in segs:
        if pg < 1 or pg > 619:
            continue
        for m in rx.finditer(t):
            a = max(0, m.start() - 38)
            b = min(len(t), m.end() + 30)
            s = t[a:b]
            i = s.find(hl) if hl in s else 0
            s = s[:i] + '**' + s[i:i + len(hl)] + '**' + s[i + len(hl):]
            yield pg, ('…' if a else '') + s.strip() + ('…' if b < len(t) else '')


def printed(pg):
    return str(pg + 2) if 5 <= pg <= 619 else '—'  # printed folio = image + 2 (image 5 shows none)


def row(spec, should, note, segs):
    out = []
    for pg, snip in find(segs, spec):
        label = spec[1] if isinstance(spec, tuple) else spec
        out.append((pg, '| `%s` | %s | %d | %s | %s%s |' % (label, should, pg, printed(pg), snip.replace('|', '\\|'),
                                                           (' (' + note + ')') if note else '')))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--md', default=str(ROOT / 'book-of-mormon-1837.md'))
    ap.add_argument('--out', default=str(ROOT / 'printer-typos.md'))
    args = ap.parse_args()
    segs = load(Path(args.md))
    out, total, missing = [], 0, []
    header = '| Printed | Should be | Image | Printed p. | In context |\n|---|---|---|---|---|'
    body = []
    for title, items in SECTIONS:
        rows = []
        for spec, should, note in items:
            r = row(spec, should, note, segs)
            if not r:
                missing.append(spec)
            rows += r
        rows.sort(key=lambda x: x[0])
        total += len(rows)
        body.append('\n## %s (%d)\n\n%s\n%s' % (title, len(rows), header, '\n'.join(r for _, r in rows)))
    rec = []
    for label, forms, should, why in RECURRING:
        hits = [h for f in forms for h in find(segs, f)]
        hits.sort()
        total += len(hits)
        pages = ', '.join(str(p) for p, _ in hits)
        rec.append('| `%s` | %s | %d | %s | %s |' % (label, should, len(hits), why, pages))
    intro = f"""# Printer's typos and misspellings in the 1837 Book of Mormon

A catalog of the places where the 1837 print itself has a slip of the type, a misspelling, or a doubled word, as the transcription records
it. {total} occurrences, grouped by the kind of slip, each with its image, printed page (image + 2 in the text) and context.

**What is and is not here.** The transcription keeps every printed error exactly as printed (nothing was corrected from later editions), so
all of these are in the page files as printed. This list leaves out spellings that were normal or intentional for the period or the edition
(`shew`, `sayeth`, `marvellous`, `wilfully` and the like; see the end of the file). It was built from a dictionary scan of the whole text,
triaged by hand, so it is **likely, not exhaustive**: a slip that happens to produce another real word (`he` for `be`) is only caught where it was noticed, and a few
entries are judgment calls (marked in the notes). Some rows are worn-type readings (`wouid`, `wben`): the scan shows a letter that looks like the printed one, which the
audits kept as printed. Names are listed only where a variant sits next to a much more frequent spelling of the same name; whether such a variant is a typo or a deliberate spelling is not always certain.

**Where to see the original.** Image numbers are the page images of the Internet Archive scan, https://archive.org/details/BookOfMormon1837KirtlandEdition (619 JPGs, numbered 001-619 in order; printed page = image + 2 in the main text). No images are included in this repository.

Generated by `tools/make_typo_catalog.py` from the live text, so page numbers and contexts stay current if the pages are edited.
"""
    recsec = '\n## Misspellings that recur\n\nThe same slip printed more than once (compositor habits rather than one-off slips).\n\n| Printed | Should be | Times | Slip | images |\n|---|---|---|---|---|\n' + '\n'.join(rec)
    Path(args.out).write_text(intro + '\n'.join(body) + '\n' + recsec + '\n\n' + NOT_INCLUDED, encoding='utf-8')
    print(f'{total} occurrences -> {args.out}')
    if missing:
        print('NOT FOUND in the text:', missing)


if __name__ == '__main__':
    main()
