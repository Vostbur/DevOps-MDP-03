import subprocess
from pathlib import Path


def test_hello_world():
    script_dir = Path(__file__).parent.parent
    actual = subprocess.run(
        ["python", f"{script_dir}/01_hello-world.py"], capture_output=True, text=True).stdout
    expected = "Hello World!\n"
    assert actual == expected
