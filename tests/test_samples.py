# -*- coding: utf-8 -*-

from framework import LinguistTestBase, main
from libs.samples import DATA


class TestSamples(LinguistTestBase):

    def test_verify(self):
        data = DATA
        assert data['languages_total'] == sum(data['languages'].values())
        assert data['tokens_total'] == sum(data['language_tokens'].values())
        assert data['tokens_total'] == sum(reduce(lambda x, y: x + y,
                                                  [token.values() for token in data['tokens'].values()]))

if __name__ == '__main__':
    main()
