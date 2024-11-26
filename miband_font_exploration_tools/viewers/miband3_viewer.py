from miband_font_exploration_tools.parsers.miband3_font import Miband3Font
from miband_font_exploration_tools.viewers.common_stuff import draw_symbol_range, get_argument_parser, PixelsRepresentation


def main():
    args = get_argument_parser().parse_args()
    with args.font_file.open("rb") as font_file:
        font_data = Miband3Font.from_io(font_file)

    super_pixel = getattr(PixelsRepresentation, args.pixel_representation).value
    for idx, symbol_range in enumerate(font_data.font16x20.ranges):
        draw_symbol_range(
            symbol_range,
            font_data.font16x20.glyphs,
            16,
            super_pixel,
            idx,
        )

    for idx, symbol_range in enumerate(font_data.font24x20.ranges):
        draw_symbol_range(
            symbol_range,
            font_data.font24x20.glyphs,
            24,
            super_pixel,
            idx,
        )

if __name__ == "__main__":
    main()
