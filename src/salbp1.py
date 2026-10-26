from __future__ import annotations

import argparse
import logging
import sys
from typing import TextIO


class Solution:
    def __init__(
        self,
        problem: Problem,
        station_tasks: list[list[int]],
        remaining_preds: list[int],
        remaining_times: list[int],
        ready_tasks: list[int],
        lb: float,
    ) -> None:
        self.problem = problem

        # station_tasks[i] is the list of tasks assigned to station i
        self.station_tasks = station_tasks

        # Number of remaining predecessors for each task
        self.remaining_preds = remaining_preds

        # Amount of cycle time available in each station
        self.remaining_times = remaining_times

        # Tasks that are ready to be in a station (for constructive search)
        # Task i must have remaining_preds[i] = 0 and to be ready
        self.ready_tasks = ready_tasks

        self.lb = lb

    def __str__(self) -> str:
        s = f"Station tasks: {self.station_tasks}"
        s += f"\nRemaining task predecessors: {self.remaining_preds}"
        s += f"\nRemaining station times: {self.remaining_times}"
        s += f"\nReady tasks: {self.ready_tasks}"
        return s

    def objective_value(self) -> int | None:
        if (
            self.ready_tasks
        ):  # Partial solution, not all tasks were assigned to a station
            return None
        return len(self.station_tasks)

    def lower_bound(self) -> float:
        return self.lb


class Problem:
    def __init__(
        self, cycle: int, times: tuple[int, ...], succ: tuple[tuple[int, ...], ...]
    ) -> None:
        self.n = len(times)
        self.cycle = cycle
        self.times = times
        self.succ = succ

    @classmethod
    def from_textio(cls, f: TextIO) -> Problem:
        """
        Create a problem instance from a text I/O source `f` in .alb format
        See: https://assembly-line-balancing.de/wp-content/uploads/2017/01/format-ALB.pdf
        """
        readfile = True
        n = -1
        cycle = -1
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
                cycle = int(f.readline())
            elif tag == "task times":
                assert n != -1, "'number of tasks' tag not detected in the file"
                for i in range(1, n + 1):
                    idx, time = map(int, f.readline().split())
                    assert idx == i
                    assert time <= cycle, "task time greater than cycle time"
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

        assert cycle != -1, "'cycle time' tag not detected in the file"
        assert times, "'task times' tag not detected in the file"

        return Problem(cycle, tuple(times), tuple(tuple(succ) for succ in successors))

    def empty_solution(self) -> Solution:
        station_tasks: list[list[int]] = []

        remaining_preds: list[int] = [0] * self.n
        for i in range(self.n):
            for j in self.succ[i]:
                remaining_preds[j] += 1

        remaining_times: list[int] = []

        ready_tasks = [i for i, n_preds in enumerate(remaining_preds) if n_preds == 0]

        lb = sum(self.times) / self.cycle

        return Solution(
            self, station_tasks, remaining_preds, remaining_times, ready_tasks, lb
        )


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

    solution = problem.empty_solution()
    print(solution)


if __name__ == "__main__":
    main()
