from __future__ import annotations

import re
from argparse import ArgumentParser
from collections import defaultdict
from importlib.metadata import version
from typing import Sequence

from mypy import api


MYPY_MSG = 'error: Unused "type: ignore" comment'
IGNORE_RE = re.compile(r"\s*#\s*type:\s*ignore\s*$", re.I)


def main(argv: Sequence[str] = None) -> int:
    """The type-heed CLI interface.

    Returns:
        int: 0 if no files were changed, else returns mypy's exit code.
    """
    parser = ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Files to process")

    fic_version = version(pkg_name := "type-heed")
    parser.add_argument(
        "-v", "--version", action="version", version=f"{pkg_name} v{fic_version}"
    )

    args = parser.parse_args(argv)

    print("Running mypy...")
    stdout, stderr, exit_code = api.run(["--warn-unused-ignores", *args.filenames])

    if stderr:
        raise TypeError(f"mypy encountered an error: {stderr}")

    if exit_code == 0:
        return 0

    file_line_map: dict[str, list[int]] = defaultdict(list)

    for line in stdout.split("\n"):  # loop over mypy log
        if MYPY_MSG not in line:
            continue
        file_path, line_num, *_ = line.split(":")
        file_line_map[file_path].append(int(line_num))

    for file_path, line_nums in file_line_map.items():
        print(f"Rewriting {file_path}")
        file = open(file_path, "r+")
        text = file.readlines()
        file.seek(0)  # rewind file pointer back to start of file

        for line_idx in line_nums:
            text[line_idx - 1] = IGNORE_RE.sub("\n", text[line_idx - 1])

        file.writelines(text)
        file.truncate()  # truncate file content to file handle's current length

        file.close()

    return exit_code


if __name__ == "__main__":
    raise SystemError(main())
