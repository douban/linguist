# -*- coding: utf-8 -*-

import re
from framework import LinguistTestBase, main
from libs.generated import Generated, XCODE_PROJECT_EXT_NAMES

TEST_FILE = "../samples/%s"

class TestGenerated(LinguistTestBase):

    # def setUp(self):
    #     super(TestGenerated, self).setUp()

    # def generate(self, name, data):
    #     return Generated(name, data)

    def test_is_xcode_project_file(self):
        for ext in XCODE_PROJECT_EXT_NAMES:
            assert True == Generated('t'+ext, '').is_xcode_project_file
        assert False == Generated('t.py', '').is_xcode_project_file

    def test_is_minified_javascript(self):
        js_mini_name = 'jquery-1.6.1.min.js'
        js_mini_path = TEST_FILE % ('JavaScript/%s' % js_mini_name)
        js_mini_file = lambda : open(js_mini_path).read()
        g = Generated(js_mini_name, js_mini_file)
        assert True == g.is_minified_javascript

        g = Generated(js_mini_name, js_mini_file())
        assert True == g.is_minified_javascript

        js_name = 'jquery-1.6.1.js'
        js_path = TEST_FILE % ('JavaScript/%s' % js_name)
        js_file = lambda : open(js_path).read()
        g = Generated(js_name, js_file)
        assert False == g.is_minified_javascript


if __name__ == '__main__':
    main()
