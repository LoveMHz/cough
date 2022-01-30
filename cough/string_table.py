class StringTable:
    """
    Layout:
    +-----------------+
    |  Size of table  |
    +-----------------+
    |     Strings     |
    +-----------------+
    Size is in bytes and contains the 4 bytes required to write it.
    """
    def __init__(self):
        self._strings = bytearray()

    @staticmethod
    def _check(value):
        if not isinstance(value, bytes):
            raise ValueError('value must be an encoded string')

    def __len__(self):
        return len(self._strings)

    def __contains__(self, item):
        return item in self._strings

    def append(self, item):
        self._check(item)

        if not self.__contains__(item + b'\0'):
            self._strings += item + b'\0'

    def pack(self):
        sizeof_strtab_size  = 4
        total_size_in_bytes = sizeof_strtab_size + len(self._strings)

        buffer = bytearray()
        buffer += total_size_in_bytes.to_bytes(sizeof_strtab_size, 'little', signed=False)
        buffer += self._strings

        return bytes(buffer)
