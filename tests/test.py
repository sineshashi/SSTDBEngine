import unittest, json, random
from src.main import Line, SortedBlock, Storage, MAX_TEMP_LINES

class LineTest(unittest.TestCase):
    def test_from_key_value(self):
        key, value = "name", "shashikant"
        line = Line.from_key_value(key, value)
        self.assertEqual(str(line), f"{key}, {json.dumps(value)}\n")

    def test_key_value(self):
        key, value = "name", "shashikant"
        line = Line.from_key_value(key, value)
        self.assertEqual(line.key, key)
        self.assertEqual(line.value, value)

    def test_equality(self):
        key, val1, val2 = "name", "sk", "s"
        line1 = Line.from_key_value(key, val1)
        line2 = Line.from_key_value(key, val2)
        self.assertEqual(line1, line2)

    def test_not_equality(self):
        key1, key2 = "name", "roll"
        line1 = Line.from_key_value(key1, None)
        line2 = Line.from_key_value(key2, None)
        self.assertNotEqual(line1, line2)
        self.assertLess(line1, line2)
        self.assertGreater(line2, line1)

class BlockTest(unittest.TestCase):
    def default_block(self) -> SortedBlock:
        kvs = [("a", "x"), ("b", "y"), ("c", "z")]
        block = SortedBlock([Line.from_key_value(k, v) for k, v in kvs])
        return block
    
    def test_size(self):
        self.assertEqual(self.default_block().size, 3)

    def test_get_line_by_idx(self):
        block = self.default_block()
        line = block.get_line_by_idx(0)
        self.assertEqual(line.key, "a")
        self.assertEqual(line.value, "x")
    
    def test_get(self):
        block = self.default_block()
        self.assertEqual(block.get("a"), "x")
        self.assertIsNone(block.get("d"))
    
    def test_set(self):
        block = self.default_block()
        block.set("d", "zz")
        self.assertEqual(block.get("d"), "zz")

    def test_merge(self):
        block1 = self.default_block()
        block2 = SortedBlock([Line.from_key_value(k, v) for k, v in [('a', 'x1'), ('aa', 'xa')]])
        block1.merge(block2)
        self.assertEqual(block1.lines, ([Line.from_key_value(k, v) for k, v in[("a", "x1"), ("aa", "xa"), ("b", "y"), ("c", "z")]]))

class StorageTest(unittest.TestCase):
    def setUp(self) -> None:
        storage = Storage(file_dir="./test_files")
        storage.clear()
        self.storage = storage
        return super().setUp()
    
    def test_set_get_single_value(self):
        self.assertEqual(self.storage.get("a"), None)
        self.storage.set("a", "value")
        self.assertEqual(self.storage.get("a"), "value")

    def test_over_flow(self):
        self.storage.set("b", "val1")
        for _ in range(MAX_TEMP_LINES):
            self.storage.set(str(random.randint(999, 9999)), str(random.randint(999, 9999)))
        self.assertEqual(self.storage.get("b"), "val1")
        self.storage.set("b", "val2")
        self.assertEqual(self.storage.get("b"), "val2")

if __name__ == "__main__":
    unittest.main()