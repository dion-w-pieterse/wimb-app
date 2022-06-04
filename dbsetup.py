import sys, getopt

def setupdb(argv):

    username = None
    password = None

    usage = 'usage: python dbsetup.py -u <username> -p <password>'

    try:
        options, args = getopt.getopt(argv, "hu:p:", ['username=', 'password='])
    except getopt.GetoptError:
        print(usage)
        sys.exit()

    for option, arg in options:
        if option == '-h':
            print(usage)
            sys.exit()
        elif option in ('-u', '--username'):
            username = arg
        elif option in ('-p', '--password'):
            password = arg

    if username == None or password == None:
        print('Could not perform action. Please follow usage directions. "python dbsetup.py -h" for usage example.')
        sys.exit()

    from app import db

    db.drop_all()
    db.create_all()

    from app import User
    from werkzeug.security import generate_password_hash, check_password_hash

    username = 'admin'
    password = '<password>'
    admin_pw_hash = generate_password_hash(password, method='sha256')
    admin_role = 'Admin'
    new_admin =User(username=username, password=admin_pw_hash, user_role='Admin')
    db.session.add(new_admin)
    db.session.commit()

    print('Successfully created database with specified administrator username and password.')


if __name__ == '__main__':
    setupdb(sys.argv[1:])
