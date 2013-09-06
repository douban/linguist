# -*- coding: utf-8 -*-

from os.path import join
from framework import LinguistTestBase, main, ROOT_DIR
from libs.tokenizer import Tokenizer


class TestTokenizer(LinguistTestBase):

    def tokenize(self, data='', is_path=None):
        if is_path:
            data = open(join(join(ROOT_DIR, "samples"), str(data))).read()
        return Tokenizer.tokenize(data)

    def test_skip_string_literals(self):
        r = ["print"]
        assert r == self.tokenize('print ""')
        assert r == self.tokenize('print "Josh"')
        assert r == self.tokenize("print 'Josh'")
        assert r == self.tokenize('print "Hello \\"Josh\\""')
        assert r == self.tokenize("print 'Hello \\'Josh\\''")
        assert r == self.tokenize("print \"Hello\", \"Josh\"")
        assert r == self.tokenize("print 'Hello', 'Josh'")
        assert r == self.tokenize("print \"Hello\", \"\", \"Josh\"")
        assert r == self.tokenize("print 'Hello', '', 'Josh'")

    def test_skip_number_literals(self):
        assert ['+'] == self.tokenize('1 + 1')
        assert ['add', '(', ')'] == self.tokenize('add(123, 456)')
        assert ['|'] == self.tokenize('0x01 | 0x10')
        assert ['*'] == self.tokenize('500.42 * 1.0')

    def test_skip_comments(self):
        r1, r2, r3 = ['foo'], ['foo', 'bar'], ['%']
        assert r1 == self.tokenize("foo\n# Comment")
        assert r1 == self.tokenize("foo\n# Comment")
        assert r2 == self.tokenize("foo\n# Comment\nbar")
        assert r1 == self.tokenize("foo\n// Comment")
        assert r1 == self.tokenize("foo /* Comment */")
        assert r1 == self.tokenize("foo /* \nComment \n */")
        assert r1 == self.tokenize("foo <!-- Comment -->")
        assert r1 == self.tokenize("foo {- Comment -}")
        assert r1 == self.tokenize("foo (* Comment *)")
        assert r3 == self.tokenize("2 % 10\n% Comment")

    def test_sgml_tags(self):
        assert ["<html>", "</html>"] == self.tokenize("<html> </html>")
        assert ["<div>", "id", "</div>"] == self.tokenize("<div id></div>")
        assert ["<div>", "id=", "</div>"] == self.tokenize("<div id=foo></div>")
        assert ["<div>", "id", "class", "</div>"] == self.tokenize("<div id class></div>")
        assert ["<div>", "id=", "</div>"] == self.tokenize("<div id=\"foo bar\"></div>")
        assert ["<div>", "id=", "</div>"] == self.tokenize("<div id='foo bar'></div>")
        assert ["<?xml>", "version="] == self.tokenize("<?xml version=\"1.0\"?>")

    def test_operators(self):
        assert ["+"] == self.tokenize("1 + 1")
        assert ["-"] == self.tokenize("1 - 1")
        assert ["*"] == self.tokenize("1 * 1")
        assert ["/"] == self.tokenize("1 / 1")
        assert ["%"] == self.tokenize("2 % 5")
        assert ["&"] == self.tokenize("1 & 1")
        assert ["&&"] == self.tokenize("1 && 1")
        assert ["|"] == self.tokenize("1 | 1")
        assert ["||"] == self.tokenize("1 || 1")
        assert ["<"] == self.tokenize("1 < 0x01")
        assert ["<<"] == self.tokenize("1 << 0x01")

    def test_c_tokens(self):
        r1 = "#ifndef HELLO_H #define HELLO_H void hello ( ) ; #endif".split()
        assert r1 == self.tokenize("C/hello.h", True)
        r2 = "#include <stdio.h> int main ( ) { printf ( ) ; return ; }".split()
        assert r2 == self.tokenize("C/hello.c", True)

    def test_cpp_tokens(self):
        r1 = "class Bar { protected char *name ; public void hello ( ) ; }".split()
        assert r1 == self.tokenize("C++/bar.h", True)
        r2 = "#include <iostream> using namespace std ; int main ( ) { cout << << endl ; }".split()
        assert r2 == self.tokenize("C++/hello.cpp", True)

    def test_objective_c_tokens(self):
        r1 = "#import <Foundation/Foundation.h> @interface Foo NSObject { } @end".split()
        assert r1 == self.tokenize("Objective-C/Foo.h", True)
        r2 = "#import <Cocoa/Cocoa.h> int main ( int argc char *argv [ ] ) { NSLog ( @ ) ; return ; }".split()
        assert r2 == self.tokenize("Objective-C/hello.m", True)
        assert "#import @implementation Foo @end".split() == self.tokenize("Objective-C/Foo.m", True)

    def test_shebang(self):
        assert "SHEBANG#!sh" == self.tokenize("Shell/sh.script!", True)[0]
        assert "SHEBANG#!bash" == self.tokenize("Shell/bash.script!", True)[0]
        assert "SHEBANG#!zsh" == self.tokenize("Shell/zsh.script!", True)[0]
        assert "SHEBANG#!perl" == self.tokenize("Perl/perl.script!", True)[0]
        assert "SHEBANG#!python" == self.tokenize("Python/python.script!", True)[0]
        assert "SHEBANG#!ruby" == self.tokenize("Ruby/ruby.script!", True)[0]
        assert "SHEBANG#!ruby" == self.tokenize("Ruby/ruby2.script!", True)[0]
        assert "SHEBANG#!node" == self.tokenize("JavaScript/js.script!", True)[0]
        assert "SHEBANG#!php" == self.tokenize("PHP/php.script!", True)[0]
        assert "SHEBANG#!escript" == self.tokenize("Erlang/factorial.script!", True)[0]
        assert "echo" == self.tokenize("Shell/invalid-shebang.sh", True)[0]

    def test_javscript_tokens(self):
        r = ["(", "function", "(", ")", "{", "console.log", "(", ")", ";", "}", ")",
             ".call", "(", "this", ")", ";"]
        assert r == self.tokenize("JavaScript/hello.js", True)

    def test_json_tokens(self):
        assert "{ [ ] { } }".split() == self.tokenize("JSON/product.json", True)

    def test_ruby_tokens(self):
        assert "module Foo end".split() == self.tokenize("Ruby/foo.rb", True)
        assert "task default do puts end".split(), self.tokenize("Ruby/filenames/Rakefile", True)


if __name__ == '__main__':
    main()
