import io
import os
import pathlib
import shutil
import string
import subprocess

from babel.messages.pofile import read_po, write_po
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


def remove_nonprintables(text):
    nps = "".join(sorted(set(chr(i) for i in range(128)) - set(string.printable)))
    table = str.maketrans(nps, nps[0] * len(nps))
    text = text.translate(table).replace(nps[0], "")
    return text.lstrip()


class Command:
    def init(self):
        """Initialize .pdk."""
        os.chdir(MSG_DIR / "..")
        if pathlib.Path("cpython").exists():
            shutil.rmtree("cpython")
        sh(
            f"git clone --single-branch -b {os.environ['PDK_BRANCH']} https://github.com/python/cpython"
        )
        sh(f"git checkout {os.environ['PDK_REVISION']}", chdir="cpython")
        LC_MESSAGES = pathlib.Path("cpython/Doc/locales/ko/LC_MESSAGES").absolute()
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
        """Extract translatable messages into .pot files."""
        chdir_Doc()
        sh("make gettext")

    def update(self):
        """Apply the updates from pot files to .po files."""
        chdir_Doc()
        sh("sphinx-intl update -p build/gettext -l ko")

    def format(self, pofile):
        """Format a .po file."""
        with open(pofile) as f:
            idata = f.read()
        f = io.StringIO(idata)
        catalog = read_po(f, abort_invalid=True)

        for msg in catalog:
            if not msg.id or not msg.string or msg.fuzzy:
                continue
            msg.string = remove_nonprintables(msg.string)

        f = io.BytesIO()
        write_po(f, catalog)
        odata = f.getvalue()
        if idata.encode() != odata:
            with open(pofile, "wb") as f:
                f.write(odata)
        else:
            print("already formatted")
        fuzzy_count = empty_count = 0
        for msg in catalog:
            if not msg.id:
                continue
            if msg.fuzzy:
                fuzzy_count += 1
            elif not msg.string:
                empty_count += 1
        if fuzzy_count:
            print(f"{fuzzy_count} fuzzy messages found")
        if empty_count:
            print(f"{empty_count} untranslated messages found")

    def find_obsoletes(self, *, delete=False):
        """Find obsolete .po files."""
        os.chdir(MSG_DIR)
        potroot = pathlib.Path("../cpython/Doc/build/gettext")
        for root, _, files in os.walk("."):
            for filename in files:
                if not filename.endswith(".po"):
                    continue
                relpath = pathlib.Path(root, filename)
                potpath = potroot / relpath.with_suffix(".pot")
                if not potpath.exists():
                    print(relpath)
                    if delete:
                        relpath.unlink()
                        relpath.with_suffix(".mo").unlink(missing_ok=True)

    def coverage(self):
        """Calculate translation coverage."""
        os.chdir(MSG_DIR)
        total = translated = fuzzy = 0
        items = []
        for root, _, files in os.walk("."):
            for filename in files:
                if not filename.endswith(".po"):
                    continue
                path = pathlib.Path(root, filename)
                if str(path) == "whatsnew/changelog.po":
                    continue
                with path.open() as f:
                    catalog = read_po(f, abort_invalid=True)
                file_total = file_translated = file_fuzzy = 0
                for msg in catalog:
                    if not msg.id:
                        continue
                    file_total += len(msg.id)
                    if not msg.fuzzy and msg.string:
                        file_translated += len(msg.id)
                    elif msg.fuzzy:
                        file_fuzzy += len(msg.id)
                total += file_total
                translated += file_translated
                fuzzy += file_fuzzy
                items.append((file_total - file_translated, path))
        for remaining, path in sorted(items):
            if remaining:
                print(f"{remaining:7d} {path}")
        print(f"{total - translated:7d} Remaining")
        print(f"{fuzzy:7d} Fuzzy")
        print(f"{total:7d} Total")
        print(f"{translated * 100.0 / total:.2f}%")

    def glean(self, filename, *, revision=None, verbose=False):
        """Try to resolve fuzzy entries."""
        from .gleaner import glean

        glean(filename, revision=revision, verbose=verbose)


def main():
    fire.Fire(Command)
