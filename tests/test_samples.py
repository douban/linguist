# -*- coding: utf-8 -*-

from framework import LinguistTestBase, main
from libs.samples import Samples, DATA

class TestSamples(LinguistTestBase):

    def test_verify(self):
        data = DATA
        def _inject(d):
            return reduce(lambda x,y: x + y[1], d.items(), 0)
        assert data['languages_total'] == _inject(data['languages'])
        assert data['tokens_total'] == _inject(data['language_tokens'])
        assert data['tokens_total'] == reduce(lambda x, y: x + _inject(dict(y[1])), data['tokens'].items(), 0)

if __name__ == '__main__':
    main()
