# Cornell Research System 

## Local installation
0. Install python

    This application uses version 2.7.X. You can get it [here](https://www.python.org/downloads/) for your operating system

1. Install pip
    * download [get-pip.py](https://bootstrap.pypa.io/get-pip.py)
    * Then run ```python get-pip.py```

2. Download virtual env.py to create a virtual environment

    ```sudo easy_install virtualenv```

3. create virtual env

    ```virtualenv venv```

4. Start up the venv enviornment

    ```source venv/bin/activate```

5. Install packages from the requirements.txt file

    ```pip install -r requirements.txt```
    
    It includes the following libraries / commands
    
    ```
    pip install flask
    pip install flask-login
    pip install flask-openid
    pip install flask-mail
    pip install flask-sqlalchemy
    pip install sqlalchemy-migrate
    pip install flask-whooshalchemy
    pip install flask-wtf
    pip install flask-babel
    pip install guess_language
    pip install flipflop
    pip install coverage
    pip install argparse
    pip install rauth
    pip install apscheduler
    ```

7. Create the db locally if not connected to a server
    
    ```chmod a+x db_create.py``` 

    then excecute it 
    
    ```python ./db_create.py```

8. Start the local server

    ```python ./run.py``` 

    or 

    ```python ./run.py debug```

    to enter debug mode. Debug mode restarts the server upon file changes associated with the server

9. Populate the local database

    ```bash populate_data.sh``` 

    will create sample student and professor profiles and populate the database with sample posts

10. Stoping the enviornment

    ```deactivate```
    
*Optional*

```sass --watch server/static/scss:server/static/css``` 

if updating SASS, must also have SASS installed. You can install that [here](http://sass-lang.com/install)

