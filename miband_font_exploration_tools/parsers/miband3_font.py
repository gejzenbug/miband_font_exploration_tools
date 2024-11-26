# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Miband3Font(KaitaiStruct):
    """Font container used by Mi Band 3.
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.signature = self._io.read_bytes(4)
        if not self.signature == b"\x48\x4D\x5A\x4B":
            raise kaitaistruct.ValidationNotEqualError(b"\x48\x4D\x5A\x4B", self.signature, self._io, u"/seq/0")
        self.unknown = self._io.read_bytes(8)
        if not self.unknown == b"\x01\xFF\xFF\xFF\xFF\x04\xFF\xFF":
            raise kaitaistruct.ValidationNotEqualError(b"\x01\xFF\xFF\xFF\xFF\x04\xFF\xFF", self.unknown, self._io, u"/seq/1")
        self.font24x20_size = self._io.read_u4le()
        self._raw_font24x20 = self._io.read_bytes(self.font24x20_size)
        _io__raw_font24x20 = KaitaiStream(BytesIO(self._raw_font24x20))
        self.font24x20 = Miband3Font.Font24x20(_io__raw_font24x20, self, self._root)
        self.font16x20 = Miband3Font.Font16x20(self._io, self, self._root)

    class Glyph24x20(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.body = self._io.read_bytes(60)
            self.max_width = self._io.read_u1()


    class Font24x20(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_ranges = self._io.read_u2le()
            self.ranges = []
            for i in range(self.num_ranges):
                self.ranges.append(Miband3Font.SymbolRange(self._io, self, self._root))

            self.glyphs = []
            i = 0
            while not self._io.is_eof():
                self.glyphs.append(Miband3Font.Glyph24x20(self._io, self, self._root))
                i += 1



    class Glyph16x20(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.body = self._io.read_bytes(40)


    class Font16x20(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_ranges = self._io.read_u2le()
            self.ranges = []
            for i in range(self.num_ranges):
                self.ranges.append(Miband3Font.SymbolRange(self._io, self, self._root))

            self.glyphs = []
            i = 0
            while not self._io.is_eof():
                self.glyphs.append(Miband3Font.Glyph16x20(self._io, self, self._root))
                i += 1



    class SymbolRange(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.from_symbol = (self._io.read_bytes(2)).decode(u"UTF-16LE")
            self.to_symbol = (self._io.read_bytes(2)).decode(u"UTF-16LE")
            self.glyph_index = self._io.read_u2le()



