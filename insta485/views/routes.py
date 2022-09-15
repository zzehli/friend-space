import flask
import insta485
import sqlite3
from insta485.api.util import password_hash

@insta485.app.route('/uploads/<path:file>')
def image(file):
    if 'user' in flask.session:
        return flask.send_from_directory(insta485.app.config['UPLOAD_FOLDER'], file)
    else:
        flask.abort(403)

@insta485.app.route('/comments/')
def view_comments():
  return "comments"

@insta485.app.route('/comments/<int:commentid>/')
def view_comment_one(commentid):
  return "comment"

@insta485.app.route('/likes/<int:likeid>/')
def view_like(likeid):
  return "like"

@insta485.app.route('/posts/<postid>/')
def view_post(postid):
  return "post"

@insta485.app.route('/users/<user_url_slug>/')
def view_user(user_url_slug):
  return "user"