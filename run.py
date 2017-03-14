#!venv/bin/python
from app import app
import sys

if __name__ == '__main__':
    if 'debug' in sys.argv:
        print('Running app in DEBUG mode.')
        app.run(debug=True)
    else:
        app.run()

