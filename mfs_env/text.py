"""Text helpers for Bangla, Banglish and English content."""

from __future__ import annotations

import re
import unicodedata

# Bangla digits ০ to ৯ map to 0 to 9
_BN_DIGITS = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")

_PHONE_RE = re.compile(r"(?:\+?88)?0?1[3-9]\d{8}")


def to_ascii_digits(text: str) -> str:
    """Convert Bangla digits to ASCII digits."""
    return text.translate(_BN_DIGITS)


def normalise_number(value: str) -> str:
    """Normalise a phone or account number.

    Handles Bangla digits, spaces, dashes and the +88 country prefix,
    so "+৮৮ ০১৮৯৯-৯৯৯৯৯৯" becomes "01899999999".
    """
    s = to_ascii_digits(str(value)).strip()
    s = re.sub(r"[\s\-()]", "", s)
    if s.startswith("+88"):
        s = s[3:]
    elif s.startswith("88") and len(s) == 13:
        s = s[2:]
    return s


def normalise_text(text: str) -> str:
    """Unicode NFC, ASCII digits, lower case, collapsed whitespace."""
    s = unicodedata.normalize("NFC", text)
    s = to_ascii_digits(s).lower()
    return re.sub(r"\s+", " ", s).strip()


def extract_numbers(text: str) -> set[str]:
    """Find Bangladeshi style phone numbers in any script."""
    s = normalise_text(text)
    s = re.sub(r"(?<=\d)[\s\-](?=\d)", "", s)
    return {normalise_number(m) for m in _PHONE_RE.findall(s)}
