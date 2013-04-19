# -*- coding: utf-8 -*-
import re

from strscan import StringScanner

"""
Generic programming language tokenizer.

Tokens are designed for use in the language bayes classifier.
It strips any data strings or comments and preserves significant
language symbols.
"""

# Read up to 100KB
BYTE_LIMIT = 100000

# Start state on token, ignore anything till the next newline
SINGLE_LINE_COMMENTS = [
    '//', # C
    '#',  # Python, Ruby
    '%',  # Tex
]

# Start state on opening token, ignore anything until the closing
# token is reached.
MULTI_LINE_COMMENTS = [
    ['/*', '*/'],    # C
    ['<!--', '-->'], # XML
    ['{-', '-}'],    # Haskell
    ['(*', '*)'],    # Coq
    ['"""', '"""'],  # Python
]

START_SINGLE_LINE_COMMENT = re.compile('|'.join(map(lambda c: '\s*%s ' % re.escape(c), SINGLE_LINE_COMMENTS)))
START_MULTI_LINE_COMMENT = re.compile('|'.join(map(lambda c: re.escape(c[0]), MULTI_LINE_COMMENTS)))

class Tokenizer(object):

    def __repr__(self):
        return '<tokenizer>'

    @classmethod
    def tokenize(cls, data):
        """
        Public: Extract tokens from data

        data - String to tokenize

        Returns Array of token Strings.
        """
        return cls().extract_tokens(data)


    def extract_tokens(self, data):
        """
        Internal: Extract generic tokens from data.

        data - String to scan.

        Examples

          extract_tokens("printf('Hello')")
          # => ['printf', '(', ')']

        Returns Array of token Strings.
        """
        s = StringScanner(data)
        tokens = []
        while not s.is_eos:
            if s.pos >= BYTE_LIMIT: break
            token = s.scan(r'^#!.+')
            if token:
                name = self.extract_shebang(token)
                if name:
                    tokens.append('SHEBANG#!%s' % name)
                    continue

            # Single line comment
            if s.is_beginning_of_line and s.scan(START_SINGLE_LINE_COMMENT):
                s.skip_until(r'\n|\Z')
                continue

            # Multiline comments
            token = s.scan(START_MULTI_LINE_COMMENT)
            if token:
                close_token = dict(MULTI_LINE_COMMENTS).get(token)
                s.skip_until(re.compile(re.escape(close_token)))
                continue

            # Skip single or double quoted strings
            if s.scan(r'"'):
                if s.peek(1) == '"':
                    s.getch
                else:
                    s.skip_until(r'[^\\]"')
            if s.scan(r"'"):
                if s.peek(1) == "'":
                    s.getch
                else:
                    s.skip_until(r"[^\\]'")

            # Skip number literals
            if s.scan(r'(0x)?\d(\d|\.)*'):
                continue

            # SGML style brackets
            token = s.scan(r'<[^\s<>][^<>]*>')
            if token:
                for t in self.extract_sgml_tokens(token):
                    tokens.append(t)
                continue

            # Common programming punctuation
            token = s.scan(r';|\{|\}|\(|\)|\[|\]')
            if token:
                tokens.append(token)
                continue

            # Regular token
            token = s.scan(r'[\w\.@#\/\*]+')
            if token:
                tokens.append(token)
                continue

            # Common operators
            token = s.scan(r'<<?|\+|\-|\*|\/|%|&&?|\|\|?')
            if token:
                tokens.append(token)
                continue

            s.getch
        return tokens


    @classmethod
    def extract_shebang(cls, data):
        """
        Internal: Extract normalized shebang command token.

        Examples

          extract_shebang("#!/usr/bin/ruby")
          # => "ruby"

          extract_shebang("#!/usr/bin/env node")
          # => "node"

        Returns String token or nil it couldn't be parsed.
        """
        s = StringScanner(data)
        path = s.scan(r'^#!\s*\S+')
        if path:
            script = path.split('/')[-1]
            if script == 'env':
                s.scan(r'\s+')
                script = s.scan(r'\S+')
            if script:
                script = re.compile(r'[^\d]+').match(script).group(0)
            return script
        return

    def extract_sgml_tokens(self, data):
        """
        Internal: Extract tokens from inside SGML tag.

        data - SGML tag String.

            Examples

              extract_sgml_tokens("<a href='' class=foo>")
              # => ["<a>", "href="]

        Returns Array of token Strings.
        """
        s = StringScanner(data)
        tokens = []

        while not s.is_eos:
            # Emit start token
            token = s.scan(r'<\/?[^\s>]+')
            if token:
                tokens.append(token + '>')
                continue

            # Emit attributes with trailing =
            token = s.scan(r'\w+=')
            if token:
                tokens.append(token)

                # Then skip over attribute value
                if s.scan('"'):
                    s.skip_until(r'[^\\]"')
                    continue
                if s.scan("'"):
                    s.skip_until(r"[^\\]'")
                    continue
                s.skip_until(r'\w+')
                continue

            # Emit lone attributes
            token = s.scan(r'\w+')
            if token:
                tokens.append(token)

            # Stop at the end of the tag
            if s.scan('>'):
                s.terminate
                continue

            s.getch

        return tokens
