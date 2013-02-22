# -*- coding: utf-8 -*-

import re
from framework import LinguistTestBase, main
from libs.strscan import StringScanner, get_regex, text_coords

class TestStringScanner(LinguistTestBase):

    def setUp(self):
        self.string = 'hello'
        self.strscan = StringScanner(self.string)
        super(TestStringScanner, self).setUp()

    def test_is_eos(self):
        assert self.strscan.is_eos == False
        self.strscan.terminate
        assert self.strscan.is_eos == True

    def test_getch(self):
        s = self.strscan
        pos = s.pos
        assert 'h' == s.getch
        assert s.pos == (pos + 1)
        s.getch
        assert 'l' == s.getch

    def test_peek(self):
        s = self.strscan
        r = s.peek(4)
        assert r == 'hell'

    def test_rest(self):
        s = self.strscan
        s.scan('hel')
        assert self.string == s.string

    def test_matched(self):
        s = self.strscan
        s.scan('hel')
        assert 'hel' == s.matched

    def test_pre_match(self):
        s = self.strscan
        assert 2 == s.skip('he')
        assert 'll' == s.scan('ll')
        assert 'he' == s.pre_match

    def test_post_match(self):
        s = self.strscan
        s.skip('he')
        s.scan('ll')
        assert 'o' == s.post_match

    def test_unscan(self):
        s = self.strscan
        s.skip('he')
        assert 'llo' == s.rest
        s.unscan
        assert 0 == s.pos
        assert self.string == s.string

    def test_is_beginning_of_line(self):
        s = self.strscan
        assert s.is_beginning_of_line == True

    def test_terminate(self):
        s = self.strscan
        s.getch
        s.terminate
        assert s.pos == len(self.string)
        assert s.match == None

    def test_scan_full(self):
        s = self.strscan
        assert None == s.scan_full("l")
        assert 'he' == s.scan_full("he")
        assert 2 == s.pos
        assert 'll' == s.scan_full('ll', advance_pointer=False)
        assert 2 == s.pos
        assert 2 == s.scan_full('ll', return_string=False, advance_pointer=False)
        assert 2 == s.pos

    def test_search_full(self):
        s = self.strscan
        assert 'he' == s.search_full('e')
        assert 2 == s.pos
        assert 'llo' == s.search_full('lo', advance_pointer=False)
        assert 2 == s.pos
        assert 3 == s.search_full('o', return_string=False, advance_pointer=False)

    def test_scan(self):
        s = self.strscan
        assert 0 == s.pos
        s.scan('world')
        s.scan('luo')
        assert 0 == s.pos
        assert 'hel' == s.scan('hel')
        assert 3 == s.pos

    def test_scan_until(self):
        s = self.strscan
        assert 'hel' == s.scan_until('el')
        assert 3 == s.pos 

    def test_scan_upto(self):
        s = self.strscan
        assert 'h' == s.scan('h')
        assert 'el' == s.scan_upto('lo')
        assert 3 == s.pos
        assert [0, 1, 3] == s.pos_history

    def test_skip(self):
        s = self.strscan
        assert 3 == s.skip('hel')

    def test_skip_unitl(self):
        s = self.strscan
        assert 3 == s.skip_until('l')

    def test_check(self):
        s = self.strscan
        assert 'hell' == s.check('hell')
        assert 0 == s.pos

    def test_check_until(self):
        s = self.strscan
        assert 'hell' == s.check('hell')
        assert 0 == s.pos

    def test_exists(self):
        s = self.strscan
        assert 3 == s.exists('l')
        assert 0 == s.pos

    def test_coords(self):
        s = StringScanner("abcdef\nghijkl\nmnopqr\nstuvwx\nyz")
        assert (0, 0, "abcdef") == s.coords
        s.pos += 4
        assert (0, 4, 'abcdef') == s.coords
        s.pos += 2
        assert (0, 6, 'abcdef') == s.coords
        s.pos += 1
        assert (1, 0, 'ghijkl') == s.coords
        s.pos += 8
        assert (2, 1, 'mnopqr') == s.coords

    def test_text_coords(self):
        s = "abcdef\nghijkl\nmnopqr\nstuvwx\nyz"
        assert (0, 0, 'abcdef') == text_coords(s, 0)
        assert (0, 4, 'abcdef') == text_coords(s, 4)
        assert (0, 6, 'abcdef') == text_coords(s, 6)
        assert (1, 0, 'ghijkl') == text_coords(s, 7)
        assert (1, 4, 'ghijkl') == text_coords(s, 11)
        assert (2, 1, 'mnopqr') == text_coords(s, 15)

    def test_get_regex(self):
        r1 = get_regex("x")
        assert isinstance(r1, re._pattern_type)

        r2 = get_regex(re.compile("x")) 
        assert isinstance(r2, re._pattern_type)

        self.assertRaises(TypeError, get_regex, 1)
        self.assertRaises(TypeError, get_regex, [])
        self.assertRaises(TypeError, get_regex, {})


if __name__ == '__main__':
    main()
