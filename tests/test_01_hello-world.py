import unittest
import subprocess
from pathlib import Path


class TestHelloWorld(unittest.TestCase):

    def test_hello_world(self):
        script_dir = Path(__file__).parent.parent
        actual = subprocess.run(
            ["python", f"{script_dir}/01_hello-world.py"], capture_output=True, text=True).stdout
        expected = "Hello World!\n"
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
