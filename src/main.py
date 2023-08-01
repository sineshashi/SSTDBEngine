import os, json
from typing import Any

class Storage:
    def __init__(self, file_dir: str) -> None:
        self._seperator = ", "
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        self._write_file = file_dir+"/storage.txt"
        self._write_handler = open(self._write_file, "a")
        self._read_handler = open(self._write_file, "r")

    def set(self, key: str, value: Any) -> None:
        self._write_handler.write(f"{key}{self._seperator}{json.dumps(value)}\n")
        self._write_handler.flush()

    def get(self, key: str) -> Any | None:
        value = None
        for line in self._read_handler:
            if line.startswith(f"{key}{self._seperator}"):
                value = json.loads(line[len(f"{key}{self._seperator}"):-1])
        return value
    
    def __del__(self) -> None:
        self._write_handler.close()
        self._read_handler.close()