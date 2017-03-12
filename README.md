# Cornell Research System 

## Local installation

1. Install pip
    * download [get-pip.py](https://bootstrap.pypa.io/get-pip.py)
    * Then run ```python get-pip.py```

2. Install packages from the requirements.txt file

    ```pip install -r requirements.txt```

3. Download virtual env.py to create a virtual environment

    ```sudo easy_install virtualenv```

4. create virtual env

	```virtualenv venv```

    *Note* If using python 2.7, make sure its <= 2.7.10. There seems to be a known issue with venv on higher versions.

5. install flask and extensions

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
    ```

6. Create the db locally - not connected to a server!
	* If you must give the permission to the file-
    
    ```chmod a+x db_create.py``` then excecute it ```./db_create.py```

7. ```./run.py``` ("./run.py debug" is needed for templates to update without restarting the server)

8. ```sass --watch app/assets/scss:app/static/css``` (if updating SASS, must also have SASS installed)

Start up the venv enviornment

```source venv/bin/activate```

Stoping

```deactivate```

