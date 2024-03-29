"""REST API for comments."""
import flask
import friendspace
import sqlite3
from friendspace.api.custom_error import CustomError
from friendspace.api.posts import check_permission

@friendspace.app.route('/api/v1/comments/<int:commentid>/', methods = ['DELETE'])
def api_get_comment_one(commentid):
    username = check_permission()
    connection = friendspace.model.get_db()
    error = None
    try:
        cur = connection.execute(
            "SELECT owner \
            FROM comments \
            WHERE commentid = :commentid",  
            {"commentid":commentid}
        )
        verify_comment = cur.fetchall()
        if len(verify_comment) == 0:
            return '',404
        if verify_comment[0]['owner'] != username:
            return '',403
        connection.execute(
            "DELETE FROM comments \
            WHERE commentid = (?)", (commentid,)
        )
    except sqlite3.Error as e:
        print(f"{type(e)}, {e}")
        error = e
    friendspace.model.close_db(error)
    return '', 204 

@friendspace.app.route('/api/v1/comments/', methods = ['POST'])
def api_post_comment():
  postid = flask.request.args.get('postid')
  text = flask.request.json.get('text')

  if text == '':
    raise CustomError('No empty comment allowed', 403)
  username = check_permission()
  connection = friendspace.model.get_db()
  error = None
  try:
    cur = connection.execute(
                "INSERT INTO comments (text, postid, owner) \
                VALUES (:text, :postid, :owner)", 
                {'text': text,
                'postid': postid,
                'owner': username}
            )
    commentid = cur.lastrowid
  except sqlite3.Error as e:
        print(f"{type(e)}, {e}")
        error = e
  friendspace.model.close_db(error)
  context = {
    "commentid": commentid,
    "lognameOwnsThis": True,
    "owner": username,
    "ownerShowUrl": flask.url_for('user', user_url_slug = username),
    "text": text,
    "url": flask.url_for('api_get_comment_one', commentid = commentid)
  }
  return flask.jsonify(**context), 201