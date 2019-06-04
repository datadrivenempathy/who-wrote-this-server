Who Wrote This Server
====================================================================================================
Simple Python-based Flask application which, serving a web-based tool, allows users to search for "prototypical articles" published by a news agency though the method described in "Machine Learning Techniques for Detecting Identifying Linguistic Patterns in the News Media" by [A Samuel Pottinger](https://gleap.org).

<br>

Purpose
----------------------------------------------------------------------------------------------------
This tiny web application uses an [inverted index](), allowing users to query a dataset for articles most like their publishing agency. For example, it can provide the most NPR-like NPR articles across all topics or the most CNN-like articles about climate change. The user can do this by providing optional search queries through a web-based UI to review coverage of a topic across many different media outlets.

<br>

Environment Setup
----------------------------------------------------------------------------------------------------
This application requires Python 3 and pip. Other dependencies can be installed via `$ pip install -r requirements.txt`. If using telemetry, provide the following env vars:

 - `TELEMETRY_DB_URL`
 - `TELEMETRY_DB_USERNAME`
 - `TELEMETRY_DB_PASSWORD`
 - `TELEMETRY_DB_NAME`
 - `TELEMETRY_DB_PORT`

<br>

Usage
----------------------------------------------------------------------------------------------------
The application is deployed publicly to https://whowrotethis.com. The application serves a UI for users at the root URL. Running locally, users can simply run `$ python application.py` and navigate to the URL printed.

<br>

Test
----------------------------------------------------------------------------------------------------
Automated tests are provided using the Python-standard `unittest` library. Users can execute via `$ nosetests`.

<br>

Development Standards
----------------------------------------------------------------------------------------------------
Please unit test and follow the [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html) where possible.

<br>

Related Projects
----------------------------------------------------------------------------------------------------
Note that this is in a series of related projects as linked:

 - [who-wrote-this-training](https://github.com/datadrivenempathy/who-wrote-this-training): logic for machine learning.
 - [who-wrote-this-server](https://github.com/datadrivenempathy/who-wrote-this-server): web application to demo the model.
 - [who-wrote-this-news-crawler](https://github.com/datadrivenempathy/who-wrote-this-news-crawler): crawler to record RSS feeds.

<br>

Open Source
----------------------------------------------------------------------------------------------------
This application's Python and JavaScript source is released under the [MIT License](https://opensource.org/licenses/MIT). All other contents including the `predictions.csv`, `who_wrote_this_data.zip`, and HTML files are released under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). The following libraries are used:

 - [Flask](http://flask.pocoo.org/) used under the [BSD License](http://flask.pocoo.org/docs/1.0/license/).
 - [itsdangerous](https://pythonhosted.org/itsdangerous/) used under the [BSD license](https://github.com/pallets/itsdangerous/blob/master/LICENSE.rst).
 - [Jinja2](http://jinja.pocoo.org/docs/2.10/) used under the [BSD license](https://github.com/pallets/jinja/blob/master/LICENSE).
 - [MarkupSafe](https://palletsprojects.com/p/markupsafe/) used under the [BSD license](https://palletsprojects.com/license/).
 - [pg8000](https://github.com/tlocke/pg8000) used under the [BSD license](https://github.com/tlocke/pg8000/blob/master/LICENSE).
 - [Werkzeug](https://www.palletsprojects.com/p/werkzeug/) used under the [BSD license](https://www.palletsprojects.com/license/).
