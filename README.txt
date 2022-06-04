##############################################################################################################
These directions are for MacOS users. Windows has its own commands,
which I trust that you know. Otherwise, the steps are the same.
###############################################################################################################

IP Address of hosted site: <IP Address>

App Name: Where's My Book?

(This will only last for two weeks after the end of the semester)

DROPPING/CREATING THE DATABASE MANUALLY via Console and Python shell:
----------------------------------------------------------------------
- create the sqlite3 database:
    - Navigate to the project directory.
        - sqlite3 <database name>.db
        - .tables
        - .exit
- Use dbsetup.py python script:
    - python dbsetup.py -u <username> -p <password>
    - NOTE: The username and password that you use in the command above will be granted the admin user role.

- Now you can run the app, and login under the admin account you just setup.
- You can create and manage regular users via the admin account.


SETUP THE APPLICATION (No repo clone process)
---------------------------------------------
    - create a project directory
    - create a virtual environment (MacOS):
        - virtualenv <environment name>
    - activate your environment (MacOS):
        - source <environment name>/bin/activate
    - install all libraries using the requirements.txt file provided:
        - pip install -r requirements.txt
    - Your environment is setup and now you can run your app.
        - python app.py


- DATABASE USERS CREATED (if you use the database provided in the repo, these users are already rows in the DB):
-----------------------------------------------------------------------------------------------------------------
  (Note: Only regular non-admin users can be created via the registration page).
    - Admin:
        - username: admin
        - password: <password>

    - Regular user 1:
        - username: test_person
        - password: <password>

- HOW TO DELETE / REBUILD SQLAlchemy DATABASE, AND RUN A FRESH DATABASE (via console if not using the dbsetup.py script):
------------------------------------------------------------------------------------------
    - rm <database name>.db
    - sqlite3 <database name>.db
    - check the database is empty
        - sqlite3 <database name>.db
        - .tables
        - .exit
    - Enter Python shell in console:
        - python
        - >>> from app import db
        - >>> db.create_all()     *** Note: If you need to drop the tables: db.drop_all() ***
        - >>> exit()
    - Check all the tables are present via console:
        - sqlite3 <database name>.db
        - .tables
        - (You should see all the tables created)
        - .exit
    - Restart the app via console:
        - python app.py


- HOW TO REFERENCE EXTERNAL SOURCES:
------------------------------------
You can find our external sources listed in the SRS and SDD documents.
