# Cornell Research Matching System

This is a simple web app for advertising research projects to students. People can post short descriptions of what they're working on, and potential researchers can filter the list to find opportunities and contact information. The idea is to deploy it at [Cornell CS][] as a way to broaden participation in undergraduate research.

[cornell cs]: http://www.cs.cornell.edu


## Requirements

You will need [Python 2.7][python].

[python]: https://www.python.org/downloads/


## Development Setup

Here's how to get a copy of the server running on your machine.

1. First, make sure you have [pip][].

2. Then, install [virtualenv][] if you don't have it already:

       pip install virtualenv

3. Create a virtual environment:

       virtualenv venv

4. Install the dependencies:

       ./venv/bin/pip install -r requirements.txt

5. Initialize a database:

       ./venv/bin/python db_create.py

6. Now you can run the server:

       ./venv/bin/python ./run.py [debug]

[virtualenv]: https://virtualenv.pypa.io/
[pip]: https://pip.pypa.io/

Once the server is running (in debug mode), you might want to populate it with some sample data. The `populate_data.sh` script will add some of that.

If you update the [Sass][] source files, use this to update the CSS:

    sass --watch server/static/scss:server/static/css

[sass]: http://sass-lang.com/install


## Deployment

You will want to configure the production version of the server. Create a Python file with *at least* values for `SECRET_KEY` and `BASE_URL`. When starting the application, point the `REMATCH_CONFIG` environment variable at this file.

Here's a straightforward way to deploy using [Gunicorn][]. Install the dependencies into a virtualenv, as above, and then also install Gunicorn into the same virtualenv:

    ./venv/bin/pip install gunicorn

Then, start Gunicorn like so:

    REMATCH_CONFIG=config.py ./venv/bin/gunicorn server:app

Then you can put the Gunicorn server behind a proper public web server.

[gunicorn]: http://gunicorn.org


## Configuration

See `config_default.py` for some options you can override in the configuration.

The application also supports SAML-based single sign-on as an alternative to username/password authentication. Set the `SAML_METADATA_URL` to the URL of the XML file describing the SAML endpoint.


## Credits

The tool was originally developed as a [CS 5150][] project by a team consisting
of Michael White, Tiffany Zheng, Aishwarya Rameshkumar, Yu (Nancy) Gu, Simeon
Videnov, Kristian Langholm, Leon Zaruvinsky, and Brandon Giraldo. It is currently maintained by [Adrian Sampson][adrian]. The license is [MIT][].

[MIT]: https://opensource.org/licenses/MIT
[adrian]: https://www.cs.cornell.edu/~asampson/
[CS 5150]: http://www.cs.cornell.edu/courses/cs5150/2017sp/
