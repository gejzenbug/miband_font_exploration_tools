from argparse import ArgumentParser
from enum import Enum
from itertools import chain
from os import get_terminal_size
from pathlib import Path
from typing import List, NamedTuple, Iterable

from miband_font_exploration_tools.font_typing import Glyph, SymbolRange


BYTE_BIT_SIZE = 8


class SuperPixelParameters(NamedTuple):
    char_map: str
    width: int
    height: int


class PixelsRepresentation(Enum):
    ONE_TO_ONE = SuperPixelParameters(
        " █",
        1, 1,
    )
    HALF_BLOCKS = SuperPixelParameters(
        " ▄▀█",
        1, 2,
    )
    FOUR_BLOCKS = super_pixel = SuperPixelParameters(
        " ▗▖▄▝▐▞▟▘▚▌▙▀▜▛█",
        2, 2,
    )
    BRAILLE = SuperPixelParameters(
        (
            " ⢀⡀⣀⠠⢠⡠⣠⠄⢄⡄⣄⠤⢤⡤⣤⠐⢐⡐⣐⠰⢰⡰⣰⠔⢔⡔⣔⠴⢴⡴⣴⠂⢂⡂⣂⠢⢢⡢⣢⠆⢆⡆⣆⠦⢦⡦⣦⠒⢒⡒⣒⠲⢲⡲⣲⠖⢖⡖⣖⠶⢶⡶⣶⠈⢈"
            "⡈⣈⠨⢨⡨⣨⠌⢌⡌⣌⠬⢬⡬⣬⠘⢘⡘⣘⠸⢸⡸⣸⠜⢜⡜⣜⠼⢼⡼⣼⠊⢊⡊⣊⠪⢪⡪⣪⠎⢎⡎⣎⠮⢮⡮⣮⠚⢚⡚⣚⠺⢺⡺⣺⠞⢞⡞⣞⠾⢾⡾⣾⠁⢁⡁⣁"
            "⠡⢡⡡⣡⠅⢅⡅⣅⠥⢥⡥⣥⠑⢑⡑⣑⠱⢱⡱⣱⠕⢕⡕⣕⠵⢵⡵⣵⠃⢃⡃⣃⠣⢣⡣⣣⠇⢇⡇⣇⠧⢧⡧⣧⠓⢓⡓⣓⠳⢳⡳⣳⠗⢗⡗⣗⠷⢷⡷⣷⠉⢉⡉⣉⠩⢩"
            "⡩⣩⠍⢍⡍⣍⠭⢭⡭⣭⠙⢙⡙⣙⠹⢹⡹⣹⠝⢝⡝⣝⠽⢽⡽⣽⠋⢋⡋⣋⠫⢫⡫⣫⠏⢏⡏⣏⠯⢯⡯⣯⠛⢛⡛⣛⠻⢻⡻⣻⠟⢟⡟⣟⠿⢿⡿⣿"
        ),
        2, 4,
    )


def concatenate_bits(numbers: Iterable[int], shift_size: int = BYTE_BIT_SIZE) -> int:
    result = 0
    for num in numbers:
        result = (result << shift_size) + num
    return result


def pixel_rows_to_pseudographics(
    pixel_rows: List[int],
    glyph_width: int,
    super_pixel: SuperPixelParameters,
) -> str:
    result = ""
    bit_mask = 2 ** super_pixel.width - 1
    for shift_size in range(glyph_width - super_pixel.width, -1, -super_pixel.width):
        char_idx = 0
        for pixel_row in pixel_rows:
            char_idx = (char_idx << super_pixel.width)
            char_idx += (pixel_row >> shift_size) & bit_mask
        result += super_pixel.char_map[char_idx]
    return result


def glyph_to_pseudographics(
    glyph_body: List[int],
    glyph_width: int,
    super_pixel: SuperPixelParameters,
) -> List[str]:
    width_in_bytes = glyph_width // BYTE_BIT_SIZE
    pixel_rows: List[int] = []
    for idx in range(0, len(glyph_body), width_in_bytes):
        pixel_rows.append(
            concatenate_bits(
                glyph_body[idx:idx + width_in_bytes],
                shift_size=BYTE_BIT_SIZE,
            ),
        )

    glyph_char_rows: List[str] = []
    for pixel_row_idx in range(0, len(pixel_rows), super_pixel.height):
        row = pixel_rows_to_pseudographics(
            pixel_rows[pixel_row_idx:pixel_row_idx+super_pixel.height],
            glyph_width,
            super_pixel,
        )
        glyph_char_rows.append(row)
    return glyph_char_rows


def draw_line(glyph_strings: List[List[str]]) -> None:
    for term_line in zip(*glyph_strings):
        print("|".join(term_line) + "|")


def draw_symbol_range(
    symbol_range: SymbolRange,
    glyphs: List[Glyph],
    glyph_width: int,
    super_pixel: SuperPixelParameters,
    range_index: int,
) -> None:
    from_codepoint = ord(symbol_range.from_symbol)
    to_codepoint = ord(symbol_range.to_symbol)
    symbols = map(chr, range(from_codepoint, to_codepoint + 1))
    glyph_strings = []
    for offset, symbol in enumerate(symbols):
        glyph_strings.append(
            glyph_to_pseudographics(
                glyphs[symbol_range.glyph_index + offset].body,
                glyph_width,
                super_pixel,
            ),
        )
    term_size = get_terminal_size(0)
    g_in_line = term_size.columns // ((glyph_width // super_pixel.width) + 1)
    print("RANGE #{0}".format(range_index))
    print("FROM:  {0} ({1})".format(symbol_range.from_symbol, hex(from_codepoint)))
    print("TO:    {0} ({1})".format(symbol_range.to_symbol, hex(to_codepoint)))
    print("COUNT:", to_codepoint - from_codepoint + 1)
    print("-" * term_size.columns)
    for idx in range(0, len(glyph_strings), g_in_line):
        draw_line(glyph_strings[idx:idx+g_in_line])
        print("-" * term_size.columns)


def get_argument_parser() -> ArgumentParser:
    aparser = ArgumentParser()
    aparser.add_argument(
        "-r",
        "--pixel-representation",
        choices=[v.name for v in PixelsRepresentation],
        default=PixelsRepresentation.ONE_TO_ONE.name,
    )
    aparser.add_argument("font_file", type=Path)
    return aparser
