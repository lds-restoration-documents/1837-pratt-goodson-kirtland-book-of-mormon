"""Helper for scripts that read book-of-mormon-1837.md: remove its YAML frontmatter."""


def strip_frontmatter(t):
    """Remove the YAML frontmatter block that compile_markdown.py puts at the top of book-of-mormon-1837.md."""
    if t.startswith('---\n'):
        end = t.find('\n---\n', 4)
        if end != -1:
            return t[end + 5:].lstrip('\n')
    return t


REPO = 'https://github.com/lds-restoration-documents/1837-pratt-goodson-kirtland-book-of-mormon'


def txt_header(sparse=False):
    """The single header line (plus blank line) at the top of the .txt outputs."""
    kind = 'sparse, ' if sparse else ''
    return f'# The Book of Mormon, Kirtland 1837 edition ({kind}AI draft, no full human proofread) - {REPO}\n\n'
