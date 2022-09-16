import insta485
import os
import pathlib
import uuid
import hashlib
import flask
import sqlite3
from insta485.api.custom_error import CustomError

@insta485.app.route('/accounts/', methods = ['POST'])
def account():

    connection = insta485.model.get_db()
    error = None

   
    operation = flask.request.form['operation']
    if operation == 'login':
        username = flask.request.form['username']
        password = flask.request.form['password']
        try:
            cur = connection.execute(
                "SELECT username, password \
                FROM users \
                WHERE username = (?)", (username,)
            )
            user = cur.fetchone()
        except sqlite3.Error as e:
            print(f"{type(e)}, {e}")
            error = e
        if user == None:
            flask.abort(403)
        password_atempt = password_hash(user['password'].split('$')[1],password)
        if password_atempt == user['password']:
            flask.session['user'] = username
        else:
            flask.abort(403)
    insta485.model.close_db(error)
    return ""


def serialize_save(fileobj):
    """
    Use the file object from flask request, computer UUID and save file under 
    its uuid in UPLOAD_FOLDER, return uuid
    """
    filename = fileobj.filename
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix
    uuid_basename = f"{stem}{suffix}"
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    return uuid_basename

def password_hash(salt, password):
    """
    Given a password and a salt, return hashed password
    """
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    return "$".join([algorithm, salt, password_hash])

def delete_image(filename):
    file_path = insta485.app.config["UPLOAD_FOLDER"]/filename
    os.remove(file_path)

def check_permission():
  """
  Check login information through request or session, return logged in username
  if authorization succeeds
  """
  if 'user' not in flask.session:
    if flask.request.authorization == None:
      raise CustomError("Forbidden", status_code=403)

    username = flask.request.authorization['username']
    password = flask.request.authorization['password']
    error = None
    #image
    try:
        connection = insta485.model.get_db()
        cur = connection.execute(
            "SELECT password \
            FROM users \
            WHERE username = (?)", (username,)
        )
        pwd_fetch = cur.fetchone()
        

    except sqlite3.Error as e:
        print(f"{type(e)}, {e}")
        error = e
    insta485.model.close_db(error)
    password_atempt = password_hash(pwd_fetch['password'].split('$')[1],password)

    if pwd_fetch['password'] != password_atempt:
      raise CustomError("Forbidden", 403)
  else:
    username = flask.session['user']
  
  return username