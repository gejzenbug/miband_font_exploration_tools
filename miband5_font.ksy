meta:
  id: miband5_font
  title: Mi Band 5 font file
  application: MiFit
  file-extension: ft
  encoding: UTF-16LE
  endian: le
doc: |
  Font container used by Mi Band 5.
seq:
  - id: signature
    contents: ["N", "E", "Z", "K"]
  - id: device_type
    type: u1
  - id: unknown01
    contents: [0xff, 0xff, 0xff, 0xff, 0xff]
  - id: font_flag
    type: u1
  - id: unknown02
    contents: [0x0, 0x0, 0x0, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]
  - id: font24x24_size
    type: u4le
  - id: font24x24
    type: font24x24
    size: font24x24_size
  - id: font16x20
    type: font16x20

types:
  glyph24x24:
    seq:
      - id: body
        size: 72
      - id: max_width
        type: u1
  glyph16x20:
    seq:
      - id: body
        size: 40
  symbol_range:
    seq:
      - id: from_symbol
        type: str
        size: 2
        encoding: UTF-16LE
      - id: to_symbol
        type: str
        size: 2
        encoding: UTF-16LE
      - id: glyph_index
        type: u2le
  font24x24:
    seq:
      - id: num_ranges
        type: u2le
      - id: ranges
        type: symbol_range
        repeat: expr
        repeat-expr: num_ranges
      - id: glyphs
        type: glyph24x24
        repeat: eos
  font16x20:
    seq:
      - id: num_ranges
        type: u2le
      - id: ranges
        type: symbol_range
        repeat: expr
        repeat-expr: num_ranges
      - id: glyphs
        type: glyph16x20
        repeat: eos
