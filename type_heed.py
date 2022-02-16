from __future__ import annotations

import re
from argparse import ArgumentParser
from collections import defaultdict
from importlib.metadata import version
from typing import Sequence

from mypy import api


MYPY_MSG = 'error: Unused "type: ignore" comment'
IGNORE_RE = re.compile(r"\s*#\s*type:\s*ignore\s*$", re.I)


def main(argv: Sequence[str] = []) -> int:
    """The type-heed CLI interface.

    Returns:
        int: 0 if type-heed exits successfully else returns an error code.
    """
    parser = ArgumentParser()

    pkg_name = "type-heed"
    fic_version = version(pkg_name)
    parser.add_argument(
        "-v", "--version", action="version", version=f"{pkg_name} v{fic_version}"
    )

    parser.add_argument("filenames", nargs="*", help="Files to process")

    args = parser.parse_args(argv)

    print("Running mypy...")
    stdout, stderr, exit_code = api.run(["--warn-unused-ignores", *args.filenames])

    if stderr:
        raise TypeError(f"mypy encountered an error: {stderr}")

    if exit_code == 0:
        return 0

    cases = [err for err in stdout.split("\n") if MYPY_MSG in err]

    file_line_map: dict[str, list[int]] = defaultdict(list)

    for case in cases:
        file_path, line_num, *_ = case.split(":")
        file_line_map[file_path].append(int(line_num))

    for file_path, lines_nums in file_line_map.items():
        print(f"Rewriting {file_path}")
        file = open(file_path, "r+")
        text = file.readlines()
        file.seek(0)  # rewind file pointer back to start of file

        for line in lines_nums:
            text[line - 1] = IGNORE_RE.sub("\n", text[line - 1])

        file.writelines(text)
        file.truncate()  # truncate file content to file handle's current length

        file.close()

    return exit_code


if __name__ == "__main__":
    raise SystemError(main())
