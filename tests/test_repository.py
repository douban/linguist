# -*- coding: utf-8 -*-

from pygments.lexers import find_lexer_class
from framework import LinguistTestBase, main, ROOT_DIR
from libs.repository import Repository
from libs.language import Language

class TestRepository(LinguistTestBase):

    def repo(self, base_path):
        return Repository.from_directory(base_path)

    def linguist_repo(self):
        return self.repo(ROOT_DIR)

    def test_linguist_language(self):
        assert self.linguist_repo().language == Language.find_by_name('Python')

    def test_linguist_languages(self):
        assert self.linguist_repo().languages[Language.find_by_name('Python')] > 2000

    def test_linguist_size(self):
        assert self.linguist_repo().size > 3000

    def test_binary_override(self):
        assert self.repo(ROOT_DIR + '/samples/Nimrod').language == Language.find_by_name('Nimrod')


if __name__ == '__main__':
    main()
