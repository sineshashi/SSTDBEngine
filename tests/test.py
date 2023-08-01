import unittest
from src.main import Storage

class DBTest(unittest.TestCase):
    def setUp(self) -> None:
        self.storage = Storage(file_dir="./test_files")
    
    def test_set_and_get(self):
        self.storage.set("name", "Shashikant")
        self.assertEqual(self.storage.get("name"), "Shashikant", "Test case 1 failed.")

    def test_get_if_not_exists(self):
        self.assertEqual(self.storage.get("roll"), None, "Test case 2 failed.")

    def test_get_after_multiset(self):
        self.storage.set("name", "shashikant")
        self.storage.set("name", "sk")
        self.assertEqual(self.storage.get("name"), "sk", "Test case 3 failed.")

if __name__ == "__main__":
    unittest.main()