# -*- coding: utf-8 -*-

from framework import LinguistTestBase, main
from libs.md5 import MD5


class TestMD5(LinguistTestBase):

    def test_hexdigest_string(self):
        assert '51d5ab3bb6ceacfd28fb3435b44df469' == MD5.hexdigest('foo')
        assert 'ed7dd53c428168f872ff18e1a4e7a0cb' == MD5.hexdigest('bar')

    def test_hexdigest_integer(self):
        assert 'ae3b28cde02542f81acce8783245430d' == MD5.hexdigest(1)
        assert '23e7c6cacb8383f878ad093b0027d72b' == MD5.hexdigest(2)

    def test_hexdigest_boolean(self):
        assert 'e62f404a21c359f79b2fac2c7a433eaf' == MD5.hexdigest(True)
        assert '9fa6d44ce6c9c565572d7b5a89e8205f' == MD5.hexdigest(False)

        assert MD5.hexdigest("True") != MD5.hexdigest(True)
        assert MD5.hexdigest("False") != MD5.hexdigest(False)

    def test_hexdigest_none(self):
        assert 'a4179d01d58ec2f9c54faeb814a6a50c' == MD5.hexdigest(None)
        assert MD5.hexdigest("None") != MD5.hexdigest(None)

    def test_hexdigest_list(self):
        assert '10ae9fc7d453b0dd525d0edf2ede7961' == MD5.hexdigest([])
        assert '5b89237adcc067a06bdf636d70d15335' == MD5.hexdigest([1])
        assert '60bbd1bf2ba7b4d7e9306969d693422d' == MD5.hexdigest([1, 2, 3])
        assert '57a3796c2e2be53df52f0731054e2b9c' == MD5.hexdigest([1, 2, [3]])

    def test_hexdigest_dict(self):
        assert 'bb4c374392133719a324ab1ba2799cd6' == MD5.hexdigest({})
        assert '1de63be82bec8f13e58d5b2370846df1' == MD5.hexdigest({'a': 1})
        assert '27fbbe666112c19d5d30a3f39f433649' == MD5.hexdigest({'a': 1, 'b': 2})
        assert MD5.hexdigest({'a': 1, 'b': 2}) == MD5.hexdigest({'b': 2, 'a': 1})


if __name__ == '__main__':
    main()
