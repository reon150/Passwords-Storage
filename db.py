import sqlite3
from cryptography.fernet import Fernet

key = "Be1PA8snHgb1DS6oaWek62WLE9nxipFw3o3vB4uJ8ZI="  # "secret key" This must be kept secret
cipher_suite = Fernet(key)  # This class provides both encryption and decryption facilities.

def conectionDB(func):
    """This is a decorator to open and close the database"""
    def wrapper(*args, **kwargs):
        global myConection
        global myCursor
        myConection = sqlite3.connect("PasswordsDB")
        myCursor = myConection.cursor()

        result = func(*args, **kwargs)

        myConection.commit()
        myConection.close()

        return result
    return wrapper


@conectionDB
def createDB():
    """This is a function to create the database if is not yet created"""
    try:
        myCursor.execute('''
            CREATE TABLE USERS (
            USER VARCHAR(17) UNIQUE,
            PASSWORD VARCHAR(17))
            ''')

        myCursor.execute('''
            CREATE TABLE PASSWORDS_DATA (
            USER VARCHAR(17),
            NAME VARCHAR (17),
            PASSWORD VARCHAR(17),
            NOTES VARCHAR(100))
            ''')

    except sqlite3.OperationalError:
        pass

@conectionDB
def loginUser(user, password):
    """ Function to login
        @Return: "yes" if the password is correct, "no" if it is incorrect, "error"  if it does not exist"""
    myCursor.execute("SELECT PASSWORD FROM USERS WHERE USER='"+user+"'")
    passwordDB = myCursor.fetchall()

    try:
        passwordDB = cipher_suite.decrypt(passwordDB[0][0])
        passwordDB = passwordDB.decode("utf-8")
        if passwordDB == password:
            return "yes"
        else:
            return "no"

    except IndexError:
        return "error"


@conectionDB
def createUser(user, password):
    """Function to create new user"""
    password = cipher_suite.encrypt(bytes(password, encoding='utf-8'))
    data = (user, password)
    myCursor.execute("INSERT INTO USERS VALUES(?,?)", data)


@conectionDB
def insertPasswordData(user, name, password, notes):
    """Function to save new password in the storage"""
    password = cipher_suite.encrypt(bytes(password, encoding='utf-8'))
    data = (user, name, password, notes)
    myCursor.execute("INSERT INTO PASSWORDS_DATA VALUES(?,?,?,?)", data)


@conectionDB
def readPasswords(user):
    """ Read all passwords from the user storage
        @return: A list, in each row there is a password with its corresponding name and notes"""
    myCursor.execute("SELECT NAME,PASSWORD,NOTES FROM PASSWORDS_DATA WHERE USER='"+user+"'")
    passwords = myCursor.fetchall()
    return passwords


@conectionDB
def deletePassword(user, name):
    """ Delete a password from the user storage
        @param: the user and the name associated with the password"""
    myCursor.execute("DELETE FROM PASSWORDS_DATA WHERE USER='"+user+"' AND NAME='"+name+"'")


@conectionDB
def readNotes(user, name):
    """ Read a password notes
        @param: the user and the name associated with the password"""
    myCursor.execute("SELECT NOTES FROM PASSWORDS_DATA WHERE USER='"+user+"' AND NAME='"+name+"'")
    notes = myCursor.fetchall()

    return notes
