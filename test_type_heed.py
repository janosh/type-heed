import importlib.metadata as md

import py
import pytest
from pytest import CaptureFixture

import type_heed


raw_txt = """
import os  # type: ignore

import unknown_lib  # type: ignore

foo = 5  # type: ignore

bar = "hi"  # type: ignore

bar = 42  # type: ignore
"""

clean_txt = """
import os

import unknown_lib  # type: ignore

foo = 5

bar = "hi"

bar = 42  # type: ignore
"""


def test_main(tmpdir: py.path.local, capsys: CaptureFixture[str]) -> None:
    # empty file to test we don't modify files without unused ignores
    file1 = tmpdir.join("file1.py").ensure()

    file2 = tmpdir.join("file2.py")
    file2.write(raw_txt)

    ret = type_heed.main((str(file1), str(file2)))

    assert ret == 1
    assert file2.read() == clean_txt

    out, _ = capsys.readouterr()
    assert out == f"Running mypy...\nRewriting {file2}\n"


def test_main_print_version(capsys: CaptureFixture[str]) -> None:

    with pytest.raises(SystemExit):
        ret_val = type_heed.main(["-v"])
        assert ret_val == 0

    stdout, stderr = capsys.readouterr()

    fic_version = md.version("type-heed")

    assert stdout == f"type-heed v{fic_version}\n"
    assert stderr == ""
