from __future__ import annotations

import argparse
import logging
import sys
from typing import TextIO


class Problem:
    def __init__(
        self, c: int, times: tuple[int, ...], successors: tuple[tuple[int, ...], ...]
    ) -> None:
        self.c = c
        self.times = times
        self.successors = successors

    @classmethod
    def from_textio(cls, f: TextIO) -> Problem:
        """
        Create a problem instance from a text I/O source `f` in .alb format
        See: https://assembly-line-balancing.de/wp-content/uploads/2017/01/format-ALB.pdf
        """
        readfile = True
        n = -1
        c = -1
        times: list[int] = []
        successors: list[list[int]] = []
        while readfile:
            line = f.readline().strip()
            if line == "" or line[0] != "<":
                continue

            tag = line[1:-1].lower()
            if tag == "number of tasks":
                n = int(f.readline())
                successors: list[list[int]] = [[] for _ in range(n)]
            elif tag == "cycle time":
                c = int(f.readline())
            elif tag == "task times":
                assert n != -1, "'number of tasks' tag not detected in the file"
                for i in range(1, n + 1):
                    idx, time = map(int, f.readline().split())
                    assert idx == i
                    times.append(time)
            elif tag == "precedence relations":
                assert n != -1, "'number of tasks' tag not detected in the file"
                assert len(successors) == n, "successors list not initialised correctly"
                line = f.readline().strip()
                while line:
                    pre, suc = map(int, line.split(","))
                    successors[pre - 1].append(suc - 1)
                    line = f.readline().strip()
            elif tag == "end":
                readfile = False

        assert c != -1, "'cycle time' tag not detected in the file"
        assert times, "'task times' tag not detected in the file"

        return Problem(c, tuple(times), tuple(tuple(suc) for suc in successors))


def main():
    logging.basicConfig(
        stream=sys.stderr, level="INFO", format="%(levelname)s;%(asctime)s;%(message)s"
    )

    argparser = argparse.ArgumentParser(description="Solve SALBP-1 Instance")
    argparser.add_argument(
        "input_file", type=str, help="Path to the input instance file"
    )
    args = argparser.parse_args()

    with open(args.input_file) as f:
        problem = Problem.from_textio(f)
        print(problem.times)
        print(problem.successors)


if __name__ == "__main__":
    main()
