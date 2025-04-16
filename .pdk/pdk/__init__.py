import os
import pathlib
import shutil
import subprocess

import fire

MSG_DIR = pathlib.Path(__file__).parent.parent.parent


def sh(cmd, capture=False, chdir=None):
    opts = {
        "shell": True,
        "stdin": subprocess.PIPE,
    }
    cwd = os.getcwd() if chdir else None
    if chdir:
        os.chdir(chdir)
    try:
        if capture:
            opts["stderr"] = subprocess.STDOUT
            opts["universal_newlines"] = True
            return subprocess.check_output(cmd, **opts)
        else:
            return subprocess.check_call(cmd, **opts)
    finally:
        if cwd:
            os.chdir(cwd)


def create_symlink(symlink, to):
    np = len(pathlib.Path(os.path.commonpath([symlink, to])).parts)
    parts = ("..",) * (len(symlink.parts) - np - 1) + to.parts[np:]
    relpath = os.path.sep.join(parts)
    symlink.parent.mkdir(parents=True, exist_ok=True)
    symlink.symlink_to(relpath, target_is_directory=to.is_dir())


def chdir_Doc():
    os.chdir(MSG_DIR / "../cpython/Doc")


class Command:
    def init(self):
        """Initialize .pdk."""
        os.chdir(MSG_DIR / "..")
        if pathlib.Path("cpython").exists():
            shutil.rmtree("cpython")
        sh(f"git clone --single-branch -b {os.environ['PDK_BRANCH']} https://github.com/python/cpython")
        sh(f"git checkout {os.environ['PDK_REVISION']}", chdir="cpython")
        LC_MESSAGES = pathlib.Path(
            "cpython/Doc/locales/ko/LC_MESSAGES").absolute()
        create_symlink(LC_MESSAGES, MSG_DIR)

    def build(self):
        """Build translated document."""
        chdir_Doc()
        sh("make -e SPHINXOPTS=\"-D language='ko'\" html")

    def watch(self):
        """Rebuild translated document on changes, with hot reloading in the browser."""
        chdir_Doc()
        sh("make -e SPHINXOPTS=\"-D language='ko'\" htmllive")

    def extract(self):
        """Extract translatable messages into pot files."""
        chdir_Doc()
        sh("make gettext")

    def update(self):
        """Apply the updates from pot files to po files."""
        chdir_Doc()
        sh("sphinx-intl update -p build/gettext -l ko")


def main():
    fire.Fire(Command)
