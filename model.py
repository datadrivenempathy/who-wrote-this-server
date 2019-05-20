"""Utilities to manage model predictions and indicies into those predictions.

----

Copyright 2019 Data Driven Empathy LLC

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

import csv

import util


class ArticleRecord:
    """Data structure describing a single article."""

    def __init__(self, title, link, source, score):
        """Create a new article record.

        Args:
            title: The text of the title.
            link: The URL to which the article record should be linked.
            source: The name of the publishing agency like NPR.
            score: The float score for the agency predicted.
        """
        self.__title = title
        self.__link = link
        self.__source = source
        self.__score = score

        if self.__link == '':
            self.__link = util.determine_search_link(self)
            self.__link_will_search = True
        else:
            self.__link_will_search = False

    def get_title(self):
        """Get the title of this article.

        Returns:
            The text of the title.
        """
        return self.__title

    def get_title_words(self, dedupe=True):
        """Get the words (lowercase) from the title.

        Args:
            dedupe: Flag indicating if only unique words should be returned. If True, only unique
                words will be returned (in no particular order). If False, all words found will
                be returned in original order with duplicates.
        Returns:
            Iterable over strings representing the words found in the title.
        """
        return util.get_words(self.get_title(), dedupe=dedupe)

    def get_source(self):
        """Get the agency that published this article.

        Returns:
            The name of the news agency that published this article.
        """
        return self.__source

    def get_score(self):
        """Get the score associated with this article.

        Returns:
            The float score for the agency predicted.
        """
        return self.__score

    def get_link(self):
        """Get the link associated with this article.

        Returns:
            The URL to which the article record should be linked.
        """
        return self.__link

    def get_link_will_search(self):
        """Get flag indicating if the link is to a search or the article itself.

        Returns:
            True if the link is to a search because the original URL was not available. False
            otherwise.
        """
        return self.__link_will_search


class ArticleKeep:
    """Utility which indexes articles and supports querying for records."""

    def __init__(self, records):
        """Create a new keep around the given records.

        Args:
            records: Iterable over records to be indexed.
        """
        self.__index = {}
        self.__prototypical = {}

        for record in records:
            self.__ingest_record(record)

    def query(self, keywords):
        """Query for a set of keywords.

        Args:
            keywords: Iterable over keywords on which articles should be filtered.
        Returns:
            List of ArticleRecords matching the input query. May be empty if no articles found.
        """
        sets = map(lambda keyword: self.__index.get(keyword, set()), keywords)
        unique_articles = set.intersection(*sets)

        ret_collection = {}

        for article in unique_articles:
            source = article.get_source()

            new_source = not source in ret_collection

            if new_source or ret_collection[source].get_score() < article.get_score():
                ret_collection[source] = article

        return list(ret_collection.values())

    def get_prototypical(self):
        """Get the list of prototypical articles (articles with highest scores).

        Returns:
            List of prototypical articles (articles with highest scores) as ArticleRecords that
            have the highest scores across the full dataset per news agency.
        """
        return list(self.__prototypical.values())

    def __ingest_record(self, record):
        """Index a new record into this keep.

        Args:
            record: The record to be registered in this keep.
        """
        for word in record.get_title_words():
            self.__register_record(word, record)

        source = record.get_source()
        if not source in self.__prototypical:
            self.__prototypical[source] = record
        elif self.__prototypical[source].get_score() < record.get_score():
            self.__prototypical[source] = record

    def __register_record(self, word, record):
        """Register a record in this keep for a specific word.

        Args:
            word: The text word with which this record should be indexed.
            record: The record to be indexed.
        """
        if not word in self.__index:
            self.__index[word] = set()
        self.__index[word].add(record)


def serialize_record_to_dict(record):
    """Serialize an article record into a dictionary.

    Args:
        record: The article as an ArticleRecord to be serialized.
    Returns:
        Dictionary serialization of the input record.
    """
    return {
        'title': record.get_title(),
        'link': record.get_link(),
        'source': record.get_source(),
        'score': record.get_score(),
        'linkWillSearch': record.get_link_will_search()
    }


def load_keep_from_dicts(record_dicts):
    """Create a new ArticleKeep from a list of dictionaries describing articles.

    Args:
        record_dicts: List of dictionaries describing articles.
    Returns:
        Newly created ArticleKeep.
    """
    return ArticleKeep(map(
        lambda x: ArticleRecord(x['title'], x['link'], x['actualSource'], float(x['score'])),
        record_dicts
    ))


def load_keep_from_disk(path_to_records='predictions.csv'):
    """Create an ArticleKeep from a CSV file on disk.

    Args:
        path_to_records: The path to a local csv file from which an ArticleKeep should be built.
    Returns:
        Newly created ArticleKeep.
    """
    with open(path_to_records, 'r', encoding='utf-8-sig') as f:
        record_dicts = list(csv.DictReader(f))

    return load_keep_from_dicts(record_dicts)
