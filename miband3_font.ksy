meta:
  id: miband3_font
  title: Mi Band 3 font file
  application: MiFit
  file-extension: ft
  encoding: UTF-16LE
  endian: le
doc: |
  Font container used by Mi Band 3.
seq:
  - id: signature
    contents: ["H", "M", "Z", "K"]
  - id: unknown
    contents: [0x01, 0xff, 0xff, 0xff, 0xff, 0x04, 0xff, 0xff]
  - id: font24x20_size
    type: u4le
  - id: font24x20
    type: font24x20
    size: font24x20_size
  - id: font16x20
    type: font16x20

types:
  glyph24x20:
    seq:
      - id: body
        size: 60
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
  font24x20:
    seq:
      - id: num_ranges
        type: u2le
      - id: ranges
        type: symbol_range
        repeat: expr
        repeat-expr: num_ranges
      - id: glyphs
        type: glyph24x20
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
