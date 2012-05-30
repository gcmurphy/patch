import re
import os

class TextChunk:

    def __init__(self, **kwargs):
        self.original = kwargs.get('original', [])
        self.changed = kwargs.get('changed', [])
        self.filename = kwargs.get('filename', "unknown")

    def add(self, line):
        self.changed.append(line)

    def remove(self, line):
        self.original.append(line)

    def common(self, line):
        self.original.append(line)
        self.changed.append(line)

    def old_version(self):
        if len(self.changed) > 0:
            return "\n".join(self.original)
        return ""

    def new_version(self):
        if len(self.changed) > 0:
            return "\n".join(self.changed)
        return ""

    def get_filename(self):
        return self.filename

    def __str__(self):
        return """%s:\n %s""" % (self.filename, self.new_version())


class TextDiff:

    def __init__(self):
        self.chunks = []

    def add(self, chunk):
        self.chunks.append(chunk)

    def changes(self):
        return self.chunks

    def __str__(self):
        strval = "{"
        for chunk in self.chunks:
            strval += str(chunk)

        strval += "\n}"
        return strval


def parse(filename, patch):
    textdiff = TextDiff()
    chunks = re.split(pattern="^@@ -", string=patch, flags=re.MULTILINE)
    header = chunks.pop(0)

    for chunk in chunks:

        textchunk = TextChunk(filename=filename)
        lines = chunk.split("\n")
        chunk_header = lines.pop(0)

        for line in lines:

            if line.startswith('+'):
                textchunk.add(line[1:])

            elif line.startswith('-'):
                textchunk.remove(line[1:])

            elif line.startswith(' '):
                textchunk.common(line[1:])

            elif line == None or line == "":
                continue

            else:
                raise RuntimeError("""Syntax Error:\
                    Unexpected chunk (%s)""" % line)

        textdiff.add(textchunk)

    return textdiff
