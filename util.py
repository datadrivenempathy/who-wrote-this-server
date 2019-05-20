"""Utility or convienence functions.

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

import re


def get_words(text, dedupe=True):
    """Get the words from a piece of text.

    Args:
        text: The text from which words should be extracted.
        dedupe: Flag indicating if only unique words should be returned. Defaults to true.
    Returns:
        Iterable over string words found from the input text.
    """
    words = map(
        lambda x: x.lower(),
        re.findall(r'[\w\'\\-]+', text)
    )

    if dedupe:
        return set(words)
    else:
        return list(words)


def determine_search_link(article):
    """Generate a search link for an article.

    Args:
        article: The article (ArticleRecord) for which a URL should be returned.
    Returns:
        String URL at which more information about an article can be found.
    """
    query_source = article.get_source().replace(' ', '+')
    query_title = '+'.join(article.get_title_words(dedupe=False))
    return 'https://duckduckgo.com/?q=%s+%s' % (query_source, query_title)
