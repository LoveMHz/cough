import enum
import struct

# Ref: https://github.com/llvm/llvm-project/blob/37293e69e6362e3559c1a4e1ac62b53f2b0edb0a/llvm/include/llvm/BinaryFormat/COFF.h#L420
class ComdatType(enum.IntEnum):
	IMAGE_COMDAT_SELECT_NODUPLICATES = 1
	IMAGE_COMDAT_SELECT_ANY          = 2
	IMAGE_COMDAT_SELECT_SAME_SIZE    = 3
	IMAGE_COMDAT_SELECT_EXACT_MATCH  = 4
	IMAGE_COMDAT_SELECT_ASSOCIATIVE  = 5
	IMAGE_COMDAT_SELECT_LARGEST      = 6
	IMAGE_COMDAT_SELECT_NEWEST       = 7

# Ref: https://github.com/llvm/llvm-project/blob/37293e69e6362e3559c1a4e1ac62b53f2b0edb0a/llvm/include/llvm/BinaryFormat/COFF.h#L453
class WeakExternalSearch(enum.IntEnum):
	IMAGE_WEAK_EXTERN_SEARCH_NOLIBRARY = 1
	IMAGE_WEAK_EXTERN_SEARCH_LIBRARY   = 2
	IMAGE_WEAK_EXTERN_SEARCH_ALIAS     = 3
	IMAGE_WEAK_EXTERN_ANTI_DEPENDENCY  = 4

class SymbolAuxRecordSectionDefinition:
	"""
	Represents an auxiliary section definition object.

	Attributes:
		length (int): The length of the section.
		number_of_relocations (int): The number of relocations for the section.
		number_of_linenumbers (int): The number of line numbers for the section.
		checksum (int): The checksum for the section.
		number (int): The number of the section.
		selection (int): The selection for the section.
	"""
	def __init__(self, length, number_of_relocations, number_of_linenumbers, checksum, number, selection):
		self.length                = length
		self.number_of_relocations = number_of_relocations
		self.number_of_linenumbers = number_of_linenumbers
		self.checksum              = checksum
		self.number                = number
		self.selection             = selection

	def pack(self):
		"""
		Packs the object into a binary format.

		Returns:
			bytes: The packed object.
		"""
		return struct.pack('<LHHLHBxxx', self.length, self.number_of_relocations, self.number_of_linenumbers, self.checksum, self.number, self.selection)

class SymbolAuxRecordWeakExternal:
	"""
	Represents an auxiliary weak external object.

	"Weak externals" are a mechanism for object files that allows flexibility at link time. A module can contain an
	unresolved external symbol (sym1), but it can also include an auxiliary record that indicates that if sym1 is not
	present at link time, another external symbol (sym2) is used to resolve references instead.

	If a definition of sym1 is linked, then an external reference to the symbol is resolved normally. If a definition
	of sym1 is not linked, then all references to the weak external for sym1 refer to sym2 instead. The external symbol,
	sym2, must always be linked; typically, it is defined in the module that contains the weak reference to sym1.

	Attributes:
		tag_index (int): The symbol-table index of sym2, the symbol to be linked if sym1 is not found.
		characteristics (int):
			A value of IMAGE_WEAK_EXTERN_SEARCH_NOLIBRARY indicates that no library search for sym1 should be performed.
			A value of IMAGE_WEAK_EXTERN_SEARCH_LIBRARY indicates that a library search for sym1 should be performed.
			A value of IMAGE_WEAK_EXTERN_SEARCH_ALIAS indicates that sym1 is an alias for sym2.
	"""
	def __init__(self, tag_index, characteristics):
		self.tag_index       = tag_index
		self.characteristics = characteristics

	def pack(self):
		"""
		Packs the object into a binary format.

		Returns:
			bytes: The packed object.
		"""
		return struct.pack('<LLxxxxxxxxxx', self.tag_index, self.characteristics)
