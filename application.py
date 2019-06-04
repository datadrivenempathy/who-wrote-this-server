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
import os

import flask
import pg8000

import model
import telemetry
import util


def create_app(app, records_keep, reporter):
    """Create a new exemplar exploration application.

    Args:
        app: The flask.Flask application into which endpoints should be registered.
        records_keep: The records to be served by this application.
        reporter: Optional telemetry.UsageReporter with with to report usage information. If None,
            telemetry is not reported.
    Return:
        The flask.Flask applicatino after registering endpoints.
    """

    def report_maybe(page, query):
        """Report telemetry if reporter is given.

        Args:
            page: String page name.
            query: String query or empty string if not applicable.
        """
        if reporter == None:
            return

        ip_address = flask.request.remote_addr
        user_agent = flask.request.headers.get('User-Agent')
        reporter.report_usage(ip_address, user_agent, page, query)

    @app.route('/')
    def home():
        """Render the homepage.

        Returns:
            String rendered app page.
        """
        report_maybe('home', '')
        return flask.render_template('app.html', page='app')

    @app.route('/code')
    def code():
        """Render the page about code.

        Returns:
            String rendered code page.
        """
        report_maybe('code', '')
        return flask.render_template('code.html', page='code')

    @app.route('/data')
    def data():
        """Render the page about data.

        Returns:
            String rendered data page.
        """
        report_maybe('data', '')
        return flask.render_template('data.html', page='data')

    @app.route('/download')
    def download():
        """Redirect to the download.

        Returns:
            Redirect to the sqlite download.
        """
        report_maybe('download', '')
        return flask.redirect('/static/zip/who_wrote_this_data.zip')

    @app.route('/privacy')
    def privacy():
        """Render the page about privacy.

        Returns:
            String rendered data page.
        """
        report_maybe('privacy', '')
        return flask.render_template('privacy.html', page='privacy')

    @app.route('/terms')
    def terms():
        """Render the page about terms.

        Returns:
            String rendered data page.
        """
        report_maybe('terms', '')
        return flask.render_template('terms.html', page='terms')

    @app.route('/paper')
    def paper():
        """Render the page about the paper.

        Returns:
            String rendered paper page.
        """
        report_maybe('paper', '')
        return flask.render_template('paper.html', page='paper')

    @app.route('/prototypical.json')
    def get_prototypical():
        """Query for the prototypical articles across all topics.

        Returns:
            JSON listing of prototypical records.
        """
        report_maybe('prototypical', '')
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
        query_string = flask.request.args.get('search')
        keywords = util.get_words(query_string)
        report_maybe('query', query_string)
        records = records_keep.query(keywords)
        records_serial = list(sorted(
            map(model.serialize_record_to_dict, records),
            key=lambda x: x['source']
        ))
        return json.dumps({'records': records_serial})

    return app


def create_connection_generator(db_url, username, password, db_name, db_port):
    """Create a new closure over the given parameters to generate postgres connections.

    Args:
        db_url: The string hostname of the database.
        password: The string password of the database.
        db_name: The database name.
        db_port: The string or integer db port.
    Returns:
        Function which, taking no paramters, will return a new database connection.
    """
    def connect():
        """Inner closure.

        Returns:
            New DB API v2 compliant connection.
        """
        return pg8000.connect(
            host=db_url,
            user=username,
            password=password,
            port=int(db_port),
            database=db_name,
            ssl=True
        )

    return connect


def create_default_app():
    """Setup this application using defaults.

    Returns:
        The flask.Flask application.
    """
    records_keep = model.load_keep_from_disk()

    reporter = None
    if 'TELEMETRY_DB_URL' in os.environ:
        db_url = os.environ['TELEMETRY_DB_URL']
        username = os.environ['TELEMETRY_DB_USERNAME']
        password = os.environ['TELEMETRY_DB_PASSWORD']
        db_name = os.environ['TELEMETRY_DB_NAME']
        db_port = os.environ['TELEMETRY_DB_PORT']
        connection_generator = create_connection_generator(
            db_url,
            username,
            password,
            db_name,
            db_port
        )

        connection = connection_generator()
        connection.close()

        reporter = telemetry.UsageReporter(connection_generator)

    app = create_app(flask.Flask(__name__), records_keep, reporter)
    return app


application = create_default_app()

if __name__ == '__main__':
    application.run()
