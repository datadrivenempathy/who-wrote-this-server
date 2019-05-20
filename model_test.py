"""Copyright 2019 Data Driven Empathy LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import unittest

import model
import util


class ModelTest(unittest.TestCase):

    def setUp(self):
        self.__keep = model.ArticleKeep([
            model.ArticleRecord('title 1 a', '', 'NPR', 0.75),
            model.ArticleRecord('title 2 b', '', 'NPR', 0.5),
            model.ArticleRecord('title 3 a', '', 'CNN', 0.25),
            model.ArticleRecord('title 4 b', '', 'CNN', 0.1)
        ])

    def test_query(self):
        prototypical_articles = self.__keep.query('b')
        self.assertEquals(len(prototypical_articles), 2)

        if prototypical_articles[0].get_source() == 'NPR':
            prototypical_npr = prototypical_articles[0]
            prototypical_cnn = prototypical_articles[1]
        else:
            prototypical_npr = prototypical_articles[1]
            prototypical_cnn = prototypical_articles[0]

        self.assertEquals(prototypical_npr.get_title(), 'title 2 b')
        self.assertEquals(prototypical_cnn.get_title(), 'title 4 b')

    def test_get_prototypical(self):
        prototypical_articles = self.__keep.get_prototypical()
        self.assertEquals(len(prototypical_articles), 2)

        if prototypical_articles[0].get_source() == 'NPR':
            prototypical_npr = prototypical_articles[0]
            prototypical_cnn = prototypical_articles[1]
        else:
            prototypical_npr = prototypical_articles[1]
            prototypical_cnn = prototypical_articles[0]

        self.assertEquals(prototypical_npr.get_title(), 'title 1 a')
        self.assertEquals(prototypical_cnn.get_title(), 'title 3 a')
