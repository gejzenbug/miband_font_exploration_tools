from argparse import ArgumentParser
from pathlib import Path
from typing import Dict, List, Tuple, NamedTuple, Optional, Union

from miband_font_exploration_tools.font_typing import FontData, Glyph, GlyphVariableWidth, SymbolRange, RangeWithGlyphs


def glyphs_to_bytes(glyphs: List[Glyph]) -> bytes:
    glyphs_bytes = b""
    for glyph in glyphs:
        glyphs_bytes += bytes(glyph.body)
        if isinstance(glyph, GlyphVariableWidth):
            glyphs_bytes += glyph.max_width.to_bytes(1, "little", signed=False)
    return glyphs_bytes


def ranges_to_bytes(ranges_with_glyphs: List[RangeWithGlyphs]) -> bytes:
    result_bytes = b""
    result_bytes += len(ranges_with_glyphs).to_bytes(2, "little", signed=False)
    glyphs_bytes = b""
    start_index = 0
    for symbol_range, glyphs in ranges_with_glyphs:
        result_bytes += symbol_range.from_symbol.encode("UTF-16LE")
        result_bytes += symbol_range.to_symbol.encode("UTF-16LE")
        result_bytes += start_index.to_bytes(2, "little", signed=False)
        start_index += len(glyphs)
        glyphs_bytes += glyphs_to_bytes(glyphs)
    result_bytes += glyphs_bytes
    return result_bytes


def range_in_rm_list(
    symbol_range: SymbolRange,
    ranges_for_rm: List[Tuple[str, str]],
) -> bool:
    for from_, to_ in ranges_for_rm:
        condition = (
            symbol_range.from_symbol <= from_ <= symbol_range.to_symbol or
            symbol_range.from_symbol <= to_ <= symbol_range.to_symbol or
            (symbol_range.from_symbol >= from_ and symbol_range.to_symbol <= to_)
        )
        if condition:
            return True
    return False


def remove_ranges(
    ranges: List[RangeWithGlyphs],
    indexes_for_rm: List[int],
    ranges_for_rm: List[Tuple[str, str]],
) -> List[RangeWithGlyphs]:
    indexes_for_rm.sort(reverse=True)
    result_ranges = ranges.copy()
    for idx in indexes_for_rm:
        all_ranges.pop(idx)

    if not ranges_for_rm:
        return result_ranges

    return [r for r in result_ranges if not range_in_rm_list(r.symbol_range, ranges_for_rm)]


def insert_ranges(
    ranges: List[RangeWithGlyphs],
    for_insert: List[RangeWithGlyphs],
) -> List[RangeWithGlyphs]:
    result_ranges = ranges.copy()
    result_ranges.extend(for_insert)
    result_ranges.sort(key=lambda r: r.symbol_range.from_symbol)
    return result_ranges


def group_glyphs_by_range(
    font_data: FontData,
) -> List[RangeWithGlyphs]:
    result: List[RangeWithGlyphs] = []
    for symbol_range in font_data.ranges:
        symbols_count = ord(symbol_range.to_symbol) - ord(symbol_range.from_symbol) + 1
        result.append(
            RangeWithGlyphs(
                symbol_range,
                font_data.glyphs[symbol_range.glyph_index:symbol_range.glyph_index + symbols_count],
            ),
        )
    return result


def parse_range(range_codes: str) -> Tuple[str, str]:
    from_, to_ = range_codes.split("-", maxsplit=1)
    return (
        chr(int(from_, base=16)),
        chr(int(to_, base=16)),
    )


def get_argument_parser() -> ArgumentParser:
    aparser = ArgumentParser()
    aparser.add_argument("--rm-wide-indexes", nargs="+", type=int, default=[])
    aparser.add_argument("--rm-narrow-indexes", nargs="+", type=int, default=[])
    aparser.add_argument("--rm-wide-ranges", nargs="+", type=parse_range, default=[])
    aparser.add_argument("--rm-narrow-ranges", nargs="+", type=parse_range, default=[])
    aparser.add_argument("--insert-narrow-file", type=Path)
    aparser.add_argument("--insert-wide-file", type=Path)
    aparser.add_argument("-i", "--input-font-file", type=Path, required=True)
    aparser.add_argument("-o", "--output-font-file", type=Path, required=True)
    return aparser
