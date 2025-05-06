import difflib
import io
import itertools
import re

from babel.messages.pofile import read_po, write_po
import git


P_INVARIANT = re.compile(
    "|".join(
        [
            r"``[^`]+``",  # ``None``
            r"\*[a-zA-Z_]+\*",  # *arg*
            r"\|[^|]+\|_?",  # |version|, |tzdata|_
            r":[a-z\-:]+:`[^`<]+`",  # :mod:`os`
            r"<[^>]+>`_{0,2}",  # <...>`, <...>`_, <...>`__
            r"`[^`<:]+`__?",  # `Sphinx`_,
        ]
    )
)


def find_invariant(immutables, i1, i2):
    for k1, k2 in immutables:
        if k1 > i1:
            break
        # flowdas: k2 > i1 조건을 넣지 않으면 오른쪽 이어붙이기를 허용하게된다.
        #   왼쪽 이어붙이기도 막아야할까?
        if k2 >= i2 and k2 > i1:
            return k1, k2


def locations(msg):
    locations = ["#:"]
    for fn, ln in msg.locations:
        locations.append(f"{fn}:{ln}")
    return " ".join(locations)


def patch_message(old, new, *, verbose=False):
    print(locations(new))
    changed = False
    invariants = [m.span() for m in P_INVARIANT.finditer(old.id)]
    if invariants:
        s = difflib.SequenceMatcher(None, old.id, new.id, autojunk=False)
        blocks = {}
        count = 0
        for tag, i1, i2, j1, j2 in reversed(s.get_opcodes()):
            if tag == "equal":
                continue
            count += 1
            if verbose:
                print(
                    f"{tag:7}   a[{i1}:{i2}] --> b[{j1}:{j2}] {old.id[i1:i2]!r:>8} --> {new.id[j1:j2]!r}"
                )

            idx = find_invariant(invariants, i1, i2)
            if not idx:
                continue
            k1, k2 = idx
            old_block = old.id[k1:k2]
            if verbose:
                print(f"\tblock a[{k1}:{k2}] {old_block}")
            if old.id.count(old_block) != 1 or old.string.count(old_block) != 1:
                continue
            template = blocks.get(old_block, old_block)
            blocks[old_block] = (
                template[: i1 - k1] + new.id[j1:j2] + template[i2 - k1 :]
            )
            count -= 1
        for old_block, new_block in blocks.items():
            # flowdas: 변경 후에도 P_INVARIANT 패턴을 유지하지 못한다면 안전하지 않다.
            if P_INVARIANT.match(new_block):
                print(f"{old_block} --> {new_block}")
                new.string = new.string.replace(old_block, new_block)
                changed = True
            else:
                count += 1
        if count == 0:
            # flowdas: 조사가 달라질 수 있기 때문에 fuzzy 를 제거하는 것이 100% 안전하지는 않다.
            #   하지만 위험보다 효용이 크다고 본다.
            new.flags.discard("fuzzy")
            print("clear fuzzy")
    return changed


def print_diff(old, new):
    s = difflib.SequenceMatcher(None, old.id, new.id, autojunk=False)
    INS = "\x1b[38;5;16;48;5;2m"
    DEL = "\x1b[38;5;16;48;5;1m"
    END = "\x1b[0m"
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == "equal":
            print(old.id[i1:i2], end="")
        if tag in {"delete", "replace"}:
            print(DEL + old.id[i1:i2] + END, end="")
        if tag in {"insert", "replace"}:
            print(INS + new.id[j1:j2] + END, end="")
    print("\n")


def glean(filename, *, revision=None, verbose=False):
    # update 전후의 .po 파일을 before 와 after 로 읽어들인다
    with open(filename) as f:
        after = read_po(f, abort_invalid=True)

    repo = git.Repo()
    if revision:
        commit = repo.commit(revision)
    else:
        commits = list(itertools.islice(repo.iter_commits(paths=filename), 0, 2))
        commit = commits[1]
    data = (commit.tree / filename).data_stream.read().decode()
    f = io.StringIO(data)
    before = read_po(f, abort_invalid=True)

    # before 로 msgstr -> msg 매핑을 만든다
    str2msg = {}
    for msg in before:
        if msg.string:
            if msg.string in str2msg:
                print("WARNING: msgstr confict:")
                print(f"\tmsgstr {msg.string!r}")
                print(f"\tmsgid {str2msg[msg.string].id!r}")
                print(f"\tmsgid {msg.id!r}")
            else:
                str2msg[msg.string] = msg

    # after 의 fuzzy 메시지들의 msgstr 과 같은 메시지를 before 에서 찾아서 쌍을 만든다
    pairs = []
    for msg in after:
        if msg.id and msg.fuzzy:
            pairs.append((str2msg[msg.string], msg))

    # 패치를 수행하고 Diff 를 인쇄한다
    changed = False
    for old, new in pairs:
        if patch_message(old, new, verbose=verbose):
            changed = True
        print()
        print_diff(old, new)

    # 변경된 after 를 저장한다
    if changed:
        f = io.BytesIO()
        write_po(f, after)
        data = f.getvalue()
        with open(filename, "wb") as f:
            f.write(data)
