import shutil
import sys
from pathlib import Path
from typing import Union

import nox

THIS_DIR = Path(__file__).parent
WINDOWS = sys.platform.startswith("win")
SUPPORTED_PYTHONS = ["3.6", "3.7", "3.8", "3.9", "3.10", "pypy3.7", "pypy3.8"]


nox.needs_version = ">=2021.10.1"
nox.options.error_on_external_run = True


def wipe(session: nox.Session, path: Union[str, Path]) -> None:
    if "--install-only" in sys.argv:
        return

    if isinstance(path, str):
        path = Path.cwd() / path
    normalized = path.relative_to(Path.cwd())

    if not path.exists():
        return

    if path.is_file():
        session.log(f"Deleting '{normalized}' file.")
        path.unlink()
    elif path.is_dir():
        session.log(f"Deleting '{normalized}' directory.")
        shutil.rmtree(path)


def get_flag(session: nox.Session, flag: str) -> bool:
    if flag in session.posargs:
        index = session.posargs.index(flag)
        del session.posargs[index]
        return True

    return False


@nox.session(name="lint")
def lint(session: nox.Session) -> None:
    """Run pre-commit."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", "--show-diff-on-failure")


@nox.session(name="tests", python=SUPPORTED_PYTHONS)
def tests(session: nox.Session) -> None:
    """Run test suite."""
    coverage = not get_flag(session, "--no-cov")
    session.install("black")
    session.install("-e", ".[test]")

    cmd = ["pytest", "tests"]
    if coverage:
        wipe(session, "htmlcov")
        cmd += ["--cov", "--cov-context", "test"]
    session.run(*cmd, *session.posargs)
    if coverage:
        session.run("coverage", "html")
