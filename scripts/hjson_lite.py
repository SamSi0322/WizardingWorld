"""Minimal reader for tModLoader localization files (.hjson).

Handles the subset those files use: nested objects, dotted keys
("A.B.C: value"), unquoted / quoted / '''multi-line''' strings and
# or // comments. Returns a flat dict of "Mods.WizardingWorld.Items.X.Tooltip"
style keys, which is how the game itself looks the strings up.
"""

import re

_KEY = re.compile(r'^\s*("(?:[^"\\]|\\.)*"|[^:{}\s][^:{}]*?)\s*:\s*(.*)$')


def _unquote(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] == '"':
        return bytes(s[1:-1], "utf-8").decode("unicode_escape").encode("latin-1").decode("utf-8")
    return s


def load(path):
    with open(path, encoding="utf-8-sig") as f:
        lines = f.read().splitlines()

    flat = {}
    stack = []  # list of key-path segments
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.strip()
        i += 1
        if not line or line.startswith("#") or line.startswith("//"):
            continue
        if line.startswith("}"):
            if stack:
                stack.pop()
            continue
        if line == "{" and not stack:
            continue
        m = _KEY.match(line)
        if not m:
            continue
        key, rest = _unquote(m.group(1)), m.group(2).strip()
        if rest == "{":
            stack.append(key)
            continue
        if rest.endswith("{") and rest[:-1].strip() == "":
            stack.append(key)
            continue
        if rest.startswith("'''"):
            body = rest[3:]
            if body.endswith("'''"):
                value = body[:-3]
            else:
                parts = [body] if body else []
                while i < len(lines):
                    nxt = lines[i]
                    i += 1
                    if nxt.strip().endswith("'''"):
                        tail = nxt.strip()[:-3]
                        if tail:
                            parts.append(tail)
                        break
                    parts.append(nxt.strip())
                value = "\n".join(parts)
        else:
            value = _unquote(rest)
        flat[".".join(stack + [key])] = value
    return flat


_TAG = re.compile(r"\[(?:c|i|g|n|a)(?:/[^:\]]*)?:([^\]]*)\]")


def clean(text):
    """Strip Terraria chat tags ([c/FF0000:text] -> text) and tidy whitespace."""
    if not text:
        return ""
    text = _TAG.sub(r"\1", text)
    return re.sub(r"[ \t]+", " ", text).strip()
