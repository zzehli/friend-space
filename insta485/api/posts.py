"""REST API for posts."""
import flask
import insta485
import sqlite3
from insta485.api.custom_error import CustomError
from insta485.api.util import check_permission

#custom error handling
@insta485.app.errorhandler(CustomError)
def invalid_credential(e):
  return flask.jsonify(e.to_dict()), e.status_code

@insta485.app.route('/api/v1/posts/')
def api_get_posts():

  #check permission/authentication
  error = None
  username = check_permission()

  lte = flask.request.args.get('postid_lte')
  size = flask.request.args.get('size', default=10, type = int)
  page = flask.request.args.get('page', default=1, type = int)
  connection = insta485.model.get_db()

  if lte != None:
    try:
          cur = connection.execute(
          "SELECT posts.postid \
          FROM posts \
          INNER JOIN (SELECT DISTINCT username2 \
              FROM following \
              WHERE username1 = :user OR username2 = :user) AS f \
          ON posts.owner = f.username2 \
          WHERE posts.postid <= :lte \
          ORDER BY posts.postid DESC \
          LIMIT :limit OFFSET :offset", {"lte": lte,
                                         "user": username,
                                         "limit": size,
                                         "offset": (page-1) * size }
          )
          postid_fetch = cur.fetchall()

          cur = connection.execute(
          "SELECT posts.postid \
          FROM posts \
          INNER JOIN (SELECT DISTINCT username2 \
              FROM following \
              WHERE username1 = :user OR username2 = :user) AS f \
          ON posts.owner = f.username2 \
          WHERE posts.postid <= :lte \
          ORDER BY posts.postid DESC \
          LIMIT :limit OFFSET :offset", {"lte": lte,
                                         "user": username,
                                         "limit": size,
                                         "offset": page * size }
          )
          next_fetch = cur.fetchall()
          print(next_fetch)
          next = True if len(next_fetch) > 0 else False
          if next == True:
            next_url = flask.url_for('api_get_posts', postid_lte = lte, page = page + 1, size = size)
          else:
            next_url = ""
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
                                         "offset": page * size }
          )
          next_fetch = cur.fetchall()
          next = True if len(next_fetch) > 0 else False
          if next == True:
            next_url = flask.url_for('api_get_posts', page = page + 1, size = size)
          else:
            next_url = ""          
          
    except sqlite3.Error as e:
        print(f"{type(e)}, {e}")
        error = e 
  
  for p in postid_fetch:
    id = p['postid']
    p['url'] = '/api/v1/posts/' + str(id) + '/'
  
  insta485.model.close_db(error)


  context = {
  "next": next_url,
  "results": postid_fetch,
    "url": flask.request.path
  }
  return flask.jsonify(**context)

@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
def api_get_post_one(postid_url_slug):
  username = check_permission()

  error = None
  try:
      connection = insta485.model.get_db()
      #image
      cur = connection.execute(
          "SELECT postid, owner, u.userimage, p.filename, created \
            FROM posts p\
            LEFT JOIN (SELECT username, filename as userimage \
                      FROM users) u \
            ON username = owner \
            WHERE postid = (?)", (postid_url_slug,)
      )
      post = cur.fetchall()
      if len(post) == 0:
        raise CustomError("Not Found", 404)
      #likes    
      cur = connection.execute(
          "SELECT COUNT(*) as c from likes \
          WHERE postid = (?)", (postid_url_slug,)
      )
      likes = cur.fetchall()   
  
      #comments  
      cur = connection.execute(
          "SELECT text, owner, commentid \
          FROM comments \
          WHERE postid = (?) \
          ORDER BY commentid", (postid_url_slug,)
      )
      comments = cur.fetchall()

      #logged user like post
      cur = connection.execute(
          "SELECT likeid \
          FROM likes \
          WHERE postid = :postid AND owner = :owner",  
          {"postid":postid_url_slug,
            "owner" :username}
      )
      liked = cur.fetchall()

  except sqlite3.Error as e:
      print(f"{type(e)}, {e}")
      error = e
  insta485.model.close_db(error)
  if len(liked) > 0:
    like_detail = {"lognameLikesThis": True,
                  "numLikes": likes[0]['c'],
                  "url": flask.url_for('api_get_like_one', likeid = liked[0]['likeid'])}
  else:
    like_detail = {"lognameLikesThis": True,
                  "numLikes": likes[0]['c'],
                  "url": None}
  for c in comments:
    c['lognameOwnsThis'] = c['owner'] == username
    c['ownerShowUrl'] = flask.url_for('view_user', user_url_slug = c['owner'])
    c['url'] = flask.url_for('api_get_comment_one', commentid = c['commentid'])
  
  
  context = {
    "comments_url": flask.url_for('api_get_comments', postid = postid_url_slug),
    "created": post[0]["created"],
    "imgUrl": flask.url_for('image', file = post[0]['filename']),
    "comments": comments,
    "likes": like_detail,
    "owner"  : post[0]["owner"],
    "ownerImgUrl": flask.url_for('image', file =  post[0]['userimage']),
    "ownerShowUrl": flask.url_for('view_user', user_url_slug = post[0]["owner"]),
    "postShowUrl": flask.url_for('view_post', postid = postid_url_slug),
    "postid" : postid_url_slug,
    #get the current url
    "url": flask.request.path
  }
  return flask.jsonify(**context)

@insta485.app.route('/api/v1/')
def get_source():
  context = {
  "comments": "/api/v1/comments/",
  "likes": "/api/v1/likes/",
  "posts": "/api/v1/posts/",
  "url": "/api/v1/",
  }
  return flask.jsonify(**context)