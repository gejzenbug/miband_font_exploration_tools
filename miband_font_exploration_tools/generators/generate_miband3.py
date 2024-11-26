import csv
import unicodedata
from argparse import ArgumentParser
from enum import Enum
from functools import partial
from math import ceil
from pathlib import Path
from typing import List, NamedTuple


class Size(NamedTuple):
    w: int
    h: int


def generate_ranges(symbol_codepoint: int, num_symbols: int) -> List[str]:
    counter = 0
    ranges: List[str] = []
    range_buffer = ""
    while counter < num_symbols:
        symbol = chr(symbol_codepoint)
        try:
            unicodedata.name(symbol)
        except ValueError:
            if range_buffer:
                ranges.append(range_buffer)
            range_buffer = ""
        else:
            range_buffer += symbol
            counter += 1
        symbol_codepoint += 1
    if range_buffer:
        ranges.append(range_buffer)
    return ranges


def bin_(num, bits, group):
    bits = "{{0:0>{0}}}".format(bits).format(bin(num)[2:])
    for idx in range(0, len(bits), group):
        print(bits[idx:idx+group])


def number_to_glyph(
    number: int,
    actual_size: Size,
    virtual_pixel_size: Size,
    max_width: int,
) -> bytes:
    virtual_width, rest_bits_count = divmod(max_width, virtual_pixel_size.w)
    rest_bits_count += actual_size.w - max_width
    virtual_height = ceil(actual_size.h / virtual_pixel_size.h)

    virtual_pixel_bits = 2 ** virtual_pixel_size.w - 1
    glyph: List[int] = []
    for virtual_line in range(virtual_height - 1, -1, -1):
        line_bits = 0
        for virtual_col in range(virtual_width - 1, -1, -1):
            bit = (number >> (virtual_col + virtual_line * virtual_width)) & 1
            line_bits = (line_bits << virtual_pixel_size.w) + bit * virtual_pixel_bits
        line_bits = line_bits << rest_bits_count
        glyph.extend([line_bits] * virtual_pixel_size.h)

    bytes_in_line = actual_size.w // 8
    glyph_bytes = b""
    for line in glyph[:actual_size.h]:
        glyph_bytes += line.to_bytes(bytes_in_line, "big", signed=False)
    return glyph_bytes


def generate_glyphs(
    ranges: List[str],
    actual_size: Size,
    virtual_pixel_size: Size,
    max_width: int,
    write_max_width: bool,
) -> bytes:
    start_index = 0
    ranges_bytes = len(ranges).to_bytes(2, "little", signed=False)
    glyphs_bytes = b""
    for symbol_range in ranges:
        ranges_bytes += symbol_range[0].encode("UTF-16LE")
        ranges_bytes += symbol_range[-1].encode("UTF-16LE")
        ranges_bytes += start_index.to_bytes(2, "little", signed=False)
        for glyph_number, s in enumerate(symbol_range, start_index):
            glyphs_bytes += number_to_glyph(
                glyph_number,
                actual_size,
                virtual_pixel_size,
                max_width,
            )
            if write_max_width:
                glyphs_bytes += max_width.to_bytes(1, "little", signed=False)
        start_index += len(symbol_range)
    return ranges_bytes + glyphs_bytes


def size(size_str: str) -> Size:
    width, height = size_str.split("x", maxsplit=1)
    return Size(int(width), int(height))


def get_argument_parser() -> ArgumentParser:
    aparser = ArgumentParser()
    aparser.add_argument("-r", "--output-range-file", type=Path, required=True)
    aparser.add_argument("-m", "--output-map-file", type=Path, required=True)
    aparser.add_argument(
        "--actual-size",
        type=size,
        required=True,
    )
    aparser.add_argument(
        "--virtual-pixel-size",
        type=size,
        required=True,
    )
    aparser.add_argument(
        "--max-width",
        type=int,
        required=True,
    )
    aparser.add_argument("--has-variable-width", action="store_true")
    aparser.add_argument(
        "--start-codepoint",
        type=partial(int, base=16),
        required=True,
    )
    aparser.add_argument(
        "--symbols-count",
        type=int,
        required=True,
    )
    return aparser


def main():
    args = get_argument_parser().parse_args()
    ranges = generate_ranges(args.start_codepoint, args.symbols_count)

    with args.output_range_file.open("wb") as output_range_file:
        output_range_file.write(
            generate_glyphs(
                ranges=ranges,
                actual_size=args.actual_size,
                virtual_pixel_size=args.virtual_pixel_size,
                max_width=args.max_width,
                write_max_width=args.has_variable_width,
            ),
        )
    with args.output_map_file.open("w", encoding="UTF-8") as output_map_file:
        output_map_file.write("".join(ranges))


if __name__ == "__main__":
    main()
