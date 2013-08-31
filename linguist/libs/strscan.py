# -*- coding: utf-8 -*-
from re import compile, _pattern_type


class StringScanner(object):

    def __init__(self, string, dup=False):
        self.string = string
        self.pos_history, self._pos = [0], 0
        self.match_history, self._match = [None], None

    def __repr__(self):
        return '<StringScanner pos: %s, match: %s>' % (self.pos, self.match)

    @property
    def is_eos(self):
        """
        Return true if the scan pointer is at the end of the string.
        """
        return self.pos >= len(self.string)

    @property
    def getch(self):
        """
        Get a single character and advance the scan pointer.
        """
        self.pos += 1
        return self.string[self.pos - 1:self.pos]

    def peek(self, length):
        """
        Get a number of characters without advancing the scan pointer.
        """
        return self.string[self.pos:self.pos + length]

    @property
    def rest(self):
        """
        Return true if the scan pointer is at the end of the string.
        """
        return self.string[self.pos:]

    @property
    def coords(self):
        """
        Return the current scanner position as `(lineno, columnno, line)`.

        This method is useful for displaying the scanner position in a human-
        readable way. For example, you could use it to provide friendlier
        debugging information when writing parsers.
        """
        return text_coords(self.string, self.pos)

    @property
    def is_tainted(self):
        return False

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        # The current position of the scan pointer.
        self._pos = pos
        self.pos_history.append(pos)

    @property
    def prev(self):
        # The last position of the scan pointer.
        return self.pos_history[-2]

    @property
    def match(self):
        return self._match

    @match.setter
    def match(self, match):
        # The latest scan match.
        self._match = match
        self.match_history.append(match)

    @property
    def matched(self):
        """
        Get the whole of the current match.
        This method returns whatever would have been returned by the latest
        :meth:`scan()` call.
        """
        return self.match.group(0)

    @property
    def pre_match(self):
        """
        Get whatever comes before the current match.
        """
        return self.string[:self.match.start()]

    @property
    def post_match(self):
        """
        Get whatever comes after the current match.
        """
        return self.string[self.match.end():]

    @property
    def unscan(self):
        """
        Undo the last scan, resetting the position and match registers.
        """
        self.pos_history.pop()
        self._pos = self.pos_history[-1]
        self.match_history.pop()
        self._match = self.match_history[-1]

    @property
    def is_beginning_of_line(self):
        """
        Return true if the scan pointer is at the beginning of a line.
        """
        if self.pos > len(self.string):
            return False
        elif self.pos == 0:
            return True
        return self.string[self.pos - 1] == "\n"

    @property
    def terminate(self):
        """
        Set the scan pointer to the end of the string;
        clear match data.
        """
        self.pos = len(self.string)
        self.match = None

    def scan_full(self, regex, return_string=True, advance_pointer=True):
        """
        Match from the current position.

        If `return_string` is false and a match is found, returns the number of
        characters matched.
        """
        regex = get_regex(regex)
        self.match = regex.match(self.string, self.pos)
        if not self.match:
            return
        if advance_pointer:
            self.pos = self.match.end()
        if return_string:
            return self.match.group(0)
        return len(self.match.group(0))

    def search_full(self, regex, return_string=True, advance_pointer=True):
        """
        Search from the current position.

        If `return_string` is false and a match is found, returns the number of
        characters matched (from the current position *up to* the end of the
        match).
        """
        regex = get_regex(regex)
        self.match = regex.search(self.string, self.pos)
        if not self.match:
            return
        start_pos = self.pos
        if advance_pointer:
            self.pos = self.match.end()
        if return_string:
            return self.string[start_pos:self.match.end()]
        return (self.match.end() - start_pos)

    def scan(self, regex):
        """
        Match a pattern from the current position.

        If a match is found, advances the scan pointer and returns the matched
        string. Otherwise returns ``None``.
        """
        return self.scan_full(regex, return_string=True, advance_pointer=True)

    def scan_until(self, regex):
        """
        Search for a pattern from the current position.

        If a match is found, advances the scan pointer and returns the matched
        string, from the current position *up to* the end of the match.
        Otherwise returns ``None``.
        """
        return self.search_full(regex, return_string=True, advance_pointer=True)

    def scan_upto(self, regex):
        """
        Scan up to, but not including, the given regex.
        """
        pos = self.pos
        if self.scan_until(regex) is not None:
            self.pos -= len(self.matched)
            # Remove the intermediate position history entry.
            self.pos_history.pop(-2)
            return self.pre_match[pos:]

    def skip(self, regex):
        """
        Like :meth:`scan`, but return the number of characters matched.
        """
        return self.scan_full(regex, return_string=False, advance_pointer=True)

    def skip_until(self, regex):
        """
        Like :meth:`scan_until`, but return the number of characters matched.
        """
        return self.search_full(regex, return_string=False, advance_pointer=True)

    def check(self, regex):
        """
        See what :meth:`scan` would return without advancing the pointer.
        """
        return self.scan_full(regex, return_string=True, advance_pointer=False)

    def check_until(self, regex):
        """
        See what :meth:`scan_until` would return without advancing the pointer.
        """
        return self.search_full(regex, return_string=True, advance_pointer=False)

    def exists(self, regex):
        """
        See what :meth:`skip_until` would return without advancing the pointer.
        Returns the number of characters matched if it does exist, or ``None``
        otherwise.
        """
        return self.search_full(regex, return_string=False, advance_pointer=False)


def text_coords(string, position):
    """
    Transform a simple index into a human-readable position in a string.

    This function accepts a string and an index, and will return a triple
    of `(lineno, columnno, line)` representing the position through the
    text.

    It's useful for displaying a string index in a human-readable way.
    """
    line_start = string.rfind('\n', 0, position) + 1
    line_end = string.find('\n', position)
    lineno = string.count('\n', 0, position)
    columnno = position - line_start
    line = string[line_start:line_end]
    return (lineno, columnno, line)


def get_regex(regex):
    """
    Ensure we have a compiled regular expression object.
    """
    if isinstance(regex, basestring):
        return compile(regex)
    elif not isinstance(regex, _pattern_type):
        raise TypeError("Invalid regex type: %r" % (regex,))
    return regex
