"""Main entrypoint into the application.

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
import json

import flask

import model
import util


def create_app(app, records_keep):
    """Create a new exemplar exploration application.

    Args:
        app: The flask.Flask application into which endpoints should be registered.
        records_keep: The records to be served by this application.
    Return:
        The flask.Flask applicatino after registering endpoints.
    """

    @app.route('/')
    def home():
        """Render the homepage.

        Returns:
            String rendered app page.
        """
        return flask.render_template('app.html', page='app')

    @app.route('/prototypical.json')
    def get_prototypical():
        """Query for the prototypical articles across all topics.

        Returns:
            JSON listing of prototypical records.
        """
        records = records_keep.get_prototypical()
        records_serial = list(sorted(
            map(model.serialize_record_to_dict, records),
            key=lambda x: x['source']
        ))
        return json.dumps({'records': records_serial})

    @app.route('/query.json')
    def query():
        """Query for prototypical articles within a topic (using "search" url param).

        Returns:
            JSON listing of prototypical records for the given topic.
        """
        keywords = util.get_words(flask.request.args.get('search'))
        records = records_keep.query(keywords)
        records_serial = list(sorted(
            map(model.serialize_record_to_dict, records),
            key=lambda x: x['source']
        ))
        return json.dumps({'records': records_serial})

    return app


def create_default_app():
    """Setup this application using defaults.

    Returns:
        The flask.Flask application.
    """
    records_keep = model.load_keep_from_disk()
    app = create_app(flask.Flask(__name__), records_keep)
    return app


application = create_default_app()

if __name__ == '__main__':
    application.run()
