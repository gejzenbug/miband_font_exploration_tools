from miband_font_exploration_tools.parsers.miband5_font import Miband5Font
from miband_font_exploration_tools.modifiers.common_stuff import get_argument_parser, group_glyphs_by_range, remove_ranges, insert_ranges, ranges_to_bytes


def main():
    args = get_argument_parser().parse_args()
    font = Miband5Font.from_file(args.input_font_file)

    wide_ranges = group_glyphs_by_range(font.font24x24)
    narrow_ranges = group_glyphs_by_range(font.font16x20)

    wide_ranges = remove_ranges(wide_ranges, args.rm_wide_indexes, args.rm_wide_ranges)
    narrow_ranges = remove_ranges(narrow_ranges, args.rm_narrow_indexes, args.rm_narrow_ranges)

    if args.insert_narrow_file:
        for_insert = Miband5Font.Font16x20.from_file(args.insert_narrow_file)
        narrow_ranges = insert_ranges(narrow_ranges, group_glyphs_by_range(for_insert))

    if args.insert_wide_file:
        for_insert = Miband5Font.Font24x24.from_file(args.insert_wide_file)
        wide_ranges = insert_ranges(wide_ranges, group_glyphs_by_range(for_insert))

    new_font_body = b""
    new_font_body += font.signature
    new_font_body += font.device_type.to_bytes(1, "little", signed=False)
    new_font_body += font.unknown01
    new_font_body += font.font_flag.to_bytes(1, "little", signed=False)
    new_font_body += font.unknown02
    wide_bytes = ranges_to_bytes(wide_ranges)
    new_font_body += len(wide_bytes).to_bytes(4, "little", signed=False)
    new_font_body += wide_bytes
    new_font_body += ranges_to_bytes(narrow_ranges)

    with args.output_font_file.open("wb") as output_font_file:
        output_font_file.write(new_font_body)


if __name__ == "__main__":
    main()
