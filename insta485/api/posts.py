"""REST API for posts."""
from multiprocessing import context
import flask
import insta485
import sqlite3
from insta485.api.custom_error import InvalidCredential
from insta485.api.util import password_hash

#custom error handling
@insta485.app.errorhandler(InvalidCredential)
def invalid_credential(e):
  return flask.jsonify(e.to_dict()), e.status_code

@insta485.app.route('/api/v1/posts/')
def get_posts():

  #check permission/authentication
  error = None
  if 'user' not in flask.session:

    username = flask.request.authorization['username']
    password = flask.request.authorization['password']

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

    password_atempt = password_hash(pwd_fetch['password'].split('$')[1],password)

    if pwd_fetch['password'] != password_atempt:
      raise InvalidCredential("Forbidden")
  else:
    username = flask.session['user']
  #TODO get posts (by logged in user or users they follow) info from DB

  #TODO handle query string: page, postid_lte, size
  lte = flask.request.args.get('postid_lte')
  size = flask.request.args.get('size', default=10, type = int)
  page = flask.request.args.get('page', default=1, type = int)
  connection = insta485.model.get_db()

  if lte != None:
    try:
          cur = connection.execute(
          "SELECT posts.postid \
          FROM posts \
          WHERE postid <= :lte \
          INNER JOIN (SELECT DISTINCT username2 \
              FROM following \
              WHERE username1 = :user OR username2 = :user) AS f \
          ON posts.owner = f.username2 \
          LIMIT :limit OFFSET :offset", {"lte": lte,
                                         "user": username,
                                         "limit": size,
                                         "offset": (page-1) * size - 1}
          )
          postid_fetch = cur.fetchall()
          
          
    except sqlite3.Error as e:
        print(f"{type(e)}, {e}")
        error = e 
  else:
    try:
          cur = connection.execute(
          "SELECT posts.postid \
          FROM posts \
          INNER JOIN (SELECT DISTINCT username2 \
              FROM following \
              WHERE username1 = :user OR username2 = :user) AS f \
          ON posts.owner = f.username2 \
          ORDER BY posts.postid DESC \
          LIMIT :limit OFFSET :offset", {"user": username,
                                         "limit": size,
                                         "offset": (page-1) * size }
          )
          postid_fetch = cur.fetchall()
          
          
    except sqlite3.Error as e:
        print(f"{type(e)}, {e}")
        error = e 
  
  for p in postid_fetch:
    id = p['postid']
    p['url'] = '/api/v1/posts/' + str(id) + '/'
  
  print(postid_fetch)
  insta485.model.close_db(error)


 
  context = {
  "next": "",
  "results": [
      {
        "postid": 3,
        "url": "/api/v1/posts/3/"
      },
      {
        "postid": 2,
        "url": "/api/v1/posts/2/"
      },
      {
        "postid": 1,
        "url": "/api/v1/posts/1/"
      }
    ],
    "url": "/api/v1/posts/"
  }
  return flask.jsonify(**context)

@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post(postid_url_slug):
    """Return post on postid.
    Example:
    {
      "created": "2017-09-28 04:33:28",
      "imgUrl": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
      "owner": "awdeorio",
      "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
      "ownerShowUrl": "/users/awdeorio/",
      "postShowUrl": "/posts/1/",
      "url": "/api/v1/posts/1/"
    }
    """
    context = {
        "created": "2017-09-28 04:33:28",
        "imgUrl": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
        "owner": "awdeorio",
        "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
        "ownerShowUrl": "/users/awdeorio/",
        "postid": "/posts/{}/".format(postid_url_slug),
        "url": flask.request.path,
    }
    return flask.jsonify(**context)

@insta485.app.route('/api/v1/')
def get_source():
  context = {
  "comments": "/api/v1/comments/",
  "likes": "/api/v1/likes/",
  "posts": "/api/v1/posts/",
  "url": "/api/v1/"
  }
  return flask.jsonify(**context)