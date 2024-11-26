from typing import List, NamedTuple, Protocol, runtime_checkable, Union


class SymbolRange(Protocol):
    from_symbol: str
    to_symbol: str
    glyph_index: int


@runtime_checkable
class GlyphFixedWidth(Protocol):
    body: List[int]


@runtime_checkable
class GlyphVariableWidth(Protocol):
    body: List[int]
    max_width: int


Glyph = Union[GlyphFixedWidth, GlyphVariableWidth]


class FontData(Protocol):
    num_ranges: int
    ranges: List[SymbolRange]
    glyphs: List[Glyph]


class RangeWithGlyphs(NamedTuple):
    symbol_range: SymbolRange
    glyphs: List[Glyph]
