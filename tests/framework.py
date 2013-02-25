# -*- coding: utf-8 -*-

import os
import sys

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(TEST_DIR)
LIBS_DIR = os.path.join(ROOT_DIR, "linguist")
sys.path.insert(0, LIBS_DIR)

from unittest import main, TestCase


class LinguistTestBase(TestCase):
    def setUp(self):
        pass
