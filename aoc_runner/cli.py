import importlib
import os
import sys
import time
from inspect import isfunction
from typing import IO

import click
import dotenv
from click_option_group import MutuallyExclusiveOptionGroup, optgroup
from loguru import logger

# My template isn't updated with a good versioneer replacement for poetry yet. Maybe AOC2022 will be the thing
# that makes me find one.
__version__ = "0.1.0"


@click.group()
@optgroup.group(
    "Output Verbosity", cls=MutuallyExclusiveOptionGroup, help="(mutually exclusive)"
)
@optgroup.option(
    "--verbose",
    "-v",
    count=True,
    help="Enable verbose output. (Repeat multiple times to increase " "verbosity.)",
)
@optgroup.option("--quiet", "-q", count=True, help="Only print error output.")
@click.option(
    "--errorfile",
    "error_file",
    help="Also log errors to specified file",
    type=click.Path(dir_okay=False, writable=True),
)
@click.option(
    "--tracefile",
    "trace_file",
    help="Additionally log all messages to specified file",
    type=click.Path(dir_okay=False, writable=True),
)
def aoc(quiet: int, verbose: int, error_file: str = None, trace_file: str = None):
    level = "SUCCESS"
    if quiet > 0:
        level = "ERROR"
    elif verbose == 1:
        level = "INFO"
    elif verbose == 2:
        level = "DEBUG"
    elif verbose >= 3:
        level = "TRACE"
    logger.remove()
    logger.add(sys.stderr, level=level)
    if error_file:
        logger.add(error_file, level="ERROR")
    if trace_file:
        logger.add(trace_file, level="TRACE")
    session_id = os.getenv("AOC_SESSION")
    if session_id is None:
        logger.warning(
            f"AOC session is unavailable. Only cached info will work, and submission will fail."
        )


@aoc.command()
def version():
    logger.success(f"aoc2020 version {__version__}")


@aoc.command()
@click.option(
    "-y", "--year", default=2021, type=int, help="Which year's contest to run"
)
@click.option("-d", "--day", default=1, type=int, help="Which day's puzzle to solve")
@click.option(
    "-p", "--part", default=None, type=int, help="Which part of the puzzle to solve"
)
@click.option(
    "--submit/--no-submit",
    is_flag=True,
    default=True,
    help="Submit after solving if only one part was specified",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    default=False,
    help="Force submit even if nondefault input is used",
)
@click.argument(
    "_input", metavar="INPUT", default=None, required=False, type=click.File(), nargs=1
)
def run(year: int, day: int, part: int, submit: bool, force: bool, _input: IO):
    data = []
    do_submit = submit
    if _input is not None:
        data = _input.read().split("\n")
        logger.debug(f"Processing input from {_input.name}")
        if submit and not force:
            logger.error(
                f"Submit was specified even though input is read from {_input.name}. That is not normally "
                f"correct. Specify --force to submit anyway."
            )
            do_submit = False

    package = f"aoc_{year}"

    day_module = importlib.import_module(f".day{day:02}", package)
    if day_module is None:
        logger.error(f"No module could be loaded for year={year} day={day}")
        sys.exit(1)

    if isfunction(getattr(day_module, "preprocess", None)):
        logger.debug("Preprocessing data")
        data = day_module.preprocess(data)

    start = time.perf_counter()
    end = None
    if part is None or part == 1:
        subpart = "a"
        if not isfunction(getattr(day_module, "part1", None)):
            logger.error(
                f"part 1 was specified but is not a function in {day_module.__name__}"
            )
            sys.exit(1)

        answer = day_module.part1(data)
        logger.success(f"Part 1: {answer}")
        if do_submit and part == 1:
            end = time.perf_counter()
            logger.debug(
                f"submitting answer={answer}, day={day}, year={year}, part={subpart}"
            )
            import aocd

            aocd.submit(answer=answer, day=day, year=year, part=subpart)
            logger.success(f"done")
    if part is None or part == 2:
        subpart = "b"
        if not isfunction(getattr(day_module, "part2", None)):
            logger.error(
                f"part 2 was specified but is not a function in {day_module.__name__}"
            )
            sys.exit(1)
        answer = day_module.part2(data)
        logger.success(f"Part 2: {answer}")
        if do_submit and part == 2:
            end = time.perf_counter()
            logger.debug(
                f"submitting answer={answer}, day={day}, year={year}, part={subpart}"
            )
            import aocd

            aocd.submit(answer=answer, day=day, year=year, part=subpart)
            logger.success(f"done")
    if part == 0:
        if not isfunction(getattr(day_module, "test", None)):
            logger.error(
                f"part 0 was specified but there is no test function in {day_module.__name__}"
            )
            sys.exit(1)
        answer = day_module.test(data)
        logger.success(f"Test returns {answer}")
    if end is None:
        end = time.perf_counter()
    logger.success(f"Time elapsed: {end - start}s")


if __name__ == "__main__":
    aoc()
