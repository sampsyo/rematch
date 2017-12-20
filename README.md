# Cornell Research Matching System

## Local installation

0. Install Python. This application uses version 2.7.X. You can get it [here](https://www.python.org/downloads/) for your operating system.
1. Install pip:
    * download [get-pip.py](https://bootstrap.pypa.io/get-pip.py)
    * Then run ```python get-pip.py```
2. Intall virtualenv: `pip install virtualenv`
3. Create a virtual environment: `virtualenv venv`
4. Activate the virtualenv: `source venv/bin/activate`
5. Install packages from the requirements.txt file: `pip install -r requirements.txt`
7. Create the database: `python ./db_create.py`
8. Start the local server: `python ./run.py [debug]`
9. Populate the local database: `bash populate_data.sh` will create sample student and professor profiles and populate the database with sample posts.
10. Deactivate the virtualenv with `deactivate`.

If you update the [Sass][] source files, use this to update the CSS:

    sass --watch server/static/scss:server/static/css

[sass]: http://sass-lang.com/install
