import os, json, bisect
from typing import Any, List, TextIO

MAX_TEMP_LINES = 3

class BlockOverFlow(Exception):
    ...

class NotWritable(Exception):
    ...

class Line:
    _seperator = ", "
    def __init__(self, line: str) -> None:
        self._line = line
    
    @property
    def key(self) -> str:
        return self._line.split(self._seperator)[0]
    
    @property
    def value(self) -> Any:
        return json.loads(("".join(self._line.split(self._seperator)[1:]))[:-1])
    
    @property
    def key_value(self) -> [str, Any]:
        return self.key, self.value
    
    def write(self, file: TextIO, flush: bool=True) -> None:
        file.write(self._line)
        if flush:
            file.flush()
    
    @classmethod
    def from_key_value(cls, key: str, value: Any) -> "Line":
        return cls(f"{key}{cls._seperator}{json.dumps(value)}\n")
    
    def __str__(self) -> str:
        return self._line
    
    def __repr__(self) -> str:
        return self._line
    
    def __eq__(self, other: "Line") -> bool:
        '''
        Two lines are considered equal when both have same keys but values are not mandatorily equal.
        '''
        return self.key == other.key
    
    def __lt__(self, other: "Line") -> bool:
        '''
        Comparision is based on keys but not values.
        '''
        return self.key < other.key
    
class SortedBlock:
    def __init__(self, lines: List[Line]=[]) -> None:
        '''
        Pass lines as sorted as it is not going to sort it.
        '''
        self._lines = lines

    @property
    def size(self) -> int:
        return len(self._lines)
    
    @property
    def lines(self) -> List[Line]:
        return self._lines

    def get_line_by_idx(self, idx: int) -> Line:
        if idx >= len(self._lines):
            raise IndexError()
        return self._lines[idx]
    
    def reset(self) -> None:
        self._lines = []

    def get(self, key: str) -> Any:
        dummy_line = Line.from_key_value(key, None)
        idx = bisect.bisect_right(self._lines, dummy_line)
        if idx == 0:
            return None
        possible_line = self.get_line_by_idx(idx-1)
        if possible_line == dummy_line:
            return possible_line.value
        return None
    
    def set(self, key: str, value: str) -> Line:
        '''This inserts line into block but do not update or delete.'''
        line = Line.from_key_value(key, value)
        idx = bisect.bisect_right(self._lines, line)
        self._lines.insert(idx, line)
        return line
    
    def write(self, file: TextIO) -> None:
        for line in self._lines:
            line.write(file, False)
        file.flush()

    def merge(self, other: "SortedBlock") -> None:
        '''
        This method merges the other one into self. If same keys are found then incoming key from other will prevail.
        '''
        merged_lines = []
        i = j = 0
        while i < self.size and j < other.size:
            f = self.get_line_by_idx(i)
            o = other.get_line_by_idx(j)
            if f == o:
                merged_lines.append(o)
                i += 1
                j += 1
            elif f < o:
                merged_lines.append(f)
                i += 1
            else:
                merged_lines.append(o)
                j += 1
        while i < self.size:
            merged_lines.append(self.get_line_by_idx(i))
            i += 1
        while j < other.size:
            merged_lines.append(other.get_line_by_idx(j))
            j += 1
        self._lines = merged_lines

    @classmethod
    def read_from_sorted_file(cls, file: TextIO) -> "SortedBlock":
        block = SortedBlock()
        for line in file:
            block._lines.append(Line(line))
        return block
    
    @classmethod
    def read_from_file(cls, file: TextIO) -> "SortedBlock":
        block = cls.read_from_sorted_file(file)
        block._lines.sort()
        return block
    
class TemporaryWrite:
    '''This class is intended to store incoming writes immediately.'''
    def __init__(self, file_dir: str, max_size: int) -> None:
        '''
        If immediate writes reach to max_size, all these writes will be transfered to persistent read and this store will be reset.
        '''
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        self._write_file = file_dir+"/storage.txt"
        self._write_handler = open(self._write_file, "a")
        with open(self._write_file, "r") as rf:
            self._block = SortedBlock.read_from_file(rf)
        self._size = max_size

    @property
    def block(self) -> SortedBlock:
        return self._block

    def set(self, key: str, value: Any) -> None:
        if self._block.size == self._size:
            raise BlockOverFlow()
        line = self._block.set(key, value)
        line.write(self._write_handler)

    def get(self, key: str) -> Any:
        return self._block.get(key)
    
    def reset(self) -> None:
        self._write_handler.close()
        with open(self._write_file, "w") as f:
            f.write("")
        self._block.reset()
        self._write_handler = open(self._write_file, "a")
    
    def __del__(self) -> None:
        self._write_handler.close()
    
class PersistentRead:
    def __init__(self, file_dir: str) -> None:
        read_dir = file_dir + "/read_files"
        self._read_dir = read_dir
        if not os.path.exists(read_dir):
            os.makedirs(read_dir)
        read_file = read_dir + "/read.txt"
        if not os.path.exists(read_file):
            open(read_file, "w").close()
        self._read_file = read_file
        with open(read_file, "r") as rf:
            self._block = SortedBlock.read_from_sorted_file(rf)
    
    def get(self, key: str) -> Any:
        return self._block.get(key)
    
    def merge(self, block: SortedBlock) -> None:
        self._block.merge(block)
        with open(self._read_file, "w") as f:
            self._block.write(f)

    def clear(self) -> None:
        with open(self._read_file, "w") as f:
            self._block.reset()
            f.write("")

class Storage:
    def __init__(self, file_dir: str) -> None:
        f'''
        All the data will be stored in given file_dir and after {MAX_TEMP_LINES} lines in temporary storage, it will be switched to Persistent one and temporary will be reset.
        '''
        self._temp_write = TemporaryWrite(file_dir, MAX_TEMP_LINES)
        self._persistent_read = PersistentRead(file_dir)

    def get(self, key: str) -> Any:
        value = self._temp_write.get(key)
        if value is None:
            value = self._persistent_read.get(key)
        return value
    
    def set(self, key: str, value: str) -> None:
        try:
            self._temp_write.set(key, value)
        except BlockOverFlow as e:
            self._persistent_read.merge(self._temp_write.block)
            self._temp_write.reset()

    def clear(self) -> None:
        self._temp_write.reset()
        self._persistent_read.clear()