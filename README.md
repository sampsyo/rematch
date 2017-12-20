# Cornell Research Matching System

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

You will want to configure the production version of the server. Create a Python file with *at least* a value for `SECRET_KEY`. When starting the application, point the `REMATCH_CONFIG` environment variable at this file.
