"""REST API for posts."""
import flask
import friendspace
import sqlite3
from friendspace.api.custom_error import CustomError
from friendspace.api.util import check_permission

#custom error handling
@friendspace.app.errorhandler(CustomError)
def invalid_credential(e):
  return flask.jsonify(e.to_dict()), e.status_code

@friendspace.app.route('/api/v1/posts/')
def api_get_posts():

  #check permission/authentication
  error = None
  username = check_permission()

  lte = flask.request.args.get('postid_lte')
  size = flask.request.args.get('size', default=10, type = int)
  page = flask.request.args.get('page', default=0, type = int)
  connection = friendspace.model.get_db()
  if size <0 or page < 0:
    raise CustomError('Bad Request', 400)
  if lte != None:
    print('here')
    try:
          cur = connection.execute(
          "SELECT DISTINCT posts.postid \
          FROM posts \
          WHERE ((posts.owner IN (SELECT username2 \
                            FROM following \
                            WHERE username1 = :user) \
                  OR posts.owner = :user)\
          AND posts.postid <= :lte )\
          ORDER BY posts.postid DESC \
          LIMIT :limit OFFSET :offset", {"lte": lte,
                                         "user": username,
                                         "limit": size,
                                         "offset": page * size }
          )
          
          postid_fetch = cur.fetchall()

          if len(postid_fetch) < size:
            next_url = ""
          else:
            next_url = flask.url_for('api_get_posts', size = size, page = page + 1, postid_lte = lte)
    except sqlite3.Error as e:
        print(f"{type(e)}, {e}")
        error = e 
  else:
    try:
          cur = connection.execute(
          "SELECT DISTINCT posts.postid \
          FROM posts \
          WHERE (posts.owner IN (SELECT username2 \
                            FROM following \
                            WHERE username1 = :user) \
                  OR posts.owner = :user)\
          ORDER BY posts.postid DESC \
          LIMIT :limit OFFSET :offset", {
                                         "user": username,
                                         "limit": size,
                                         "offset": page * size }
          )
          postid_fetch = cur.fetchall()
          if len(postid_fetch) < size:
            next_url = ""
          else:
            newestid = postid_fetch[0]['postid']
            next_url = flask.url_for('api_get_posts', size = size, page = page + 1, postid_lte = newestid)
    except sqlite3.Error as e:
        print(f"{type(e)}, {e}")
        error = e 
        print('here')
  
  for p in postid_fetch:
    id = p['postid']
    p['url'] = '/api/v1/posts/' + str(id) + '/'
  
  friendspace.model.close_db(error)
  if flask.request.args == {}:
    url = flask.request.path
  else:
    url = flask.request.full_path
  context = {
  "next": next_url,
  "results": postid_fetch,
  "url": url
  }
  return flask.jsonify(**context)

@friendspace.app.route('/api/v1/posts/<int:postid_url_slug>/')
def api_get_post_one(postid_url_slug):
  username = check_permission()

  error = None
  try:
      connection = friendspace.model.get_db()
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
  friendspace.model.close_db(error)
  if len(liked) > 0:
    like_detail = {"lognameLikesThis": True,
                  "numLikes": likes[0]['c'],
                  "url": flask.url_for('api_get_like_one', likeid = liked[0]['likeid'])}
  else:
    # TODO: url is null when user doesn't like it
    like_detail = {"lognameLikesThis": False,
                  "numLikes": likes[0]['c'],
                  "url": None}
  for c in comments:
    c['lognameOwnsThis'] = c['owner'] == username
    c['ownerShowUrl'] = flask.url_for('user', user_url_slug = c['owner'])
    c['url'] = flask.url_for('api_get_comment_one', commentid = c['commentid'])
  
  
  context = {
    "comments_url": flask.url_for('api_post_comment', postid = postid_url_slug),
    "created": post[0]["created"],
    "imgUrl": flask.url_for('image', file = post[0]['filename']),
    "comments": comments,
    "likes": like_detail,
    "owner"  : post[0]["owner"],
    "ownerImgUrl": flask.url_for('image', file =  post[0]['userimage']),
    "ownerShowUrl": flask.url_for('user', user_url_slug = post[0]["owner"]),
    "postShowUrl": flask.url_for('post', postid_url_slug = postid_url_slug),
    "postid" : postid_url_slug,
    #get the current url
    "url": flask.request.path
  }
  return flask.jsonify(**context)

@friendspace.app.route('/api/v1/')
def get_source():
  context = {
  "comments": "/api/v1/comments/",
  "likes": "/api/v1/likes/",
  "posts": "/api/v1/posts/",
  "url": "/api/v1/",
  }
  return flask.jsonify(**context)