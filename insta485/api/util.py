import insta485
import os
import pathlib
import uuid
import hashlib
import flask
import sqlite3
from insta485.api.custom_error import CustomError

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