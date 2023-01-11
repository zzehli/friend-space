"""REST API for likes."""
import flask
import friendspace
import sqlite3
from friendspace.api.custom_error import CustomError
from friendspace.api.posts import check_permission

@friendspace.app.route('/api/v1/likes/<int:likeid>/', methods = ['DELETE'])
def api_get_like_one(likeid):
    username = check_permission()
    connection = friendspace.model.get_db()
    error = None
    try:
        cur = connection.execute(
            "SELECT owner \
            FROM likes \
            WHERE likeid = :likeid",  
            {"likeid":likeid}
        )
        verify_like = cur.fetchall()
        if len(verify_like) == 0:
            return '',404
        if verify_like[0]['owner'] != username:
            return '',403
        connection.execute(
            "DELETE FROM likes \
            WHERE likeid = (?)", (likeid,)
        )
    except sqlite3.Error as e:
        print(f"{type(e)}, {e}")
        error = e
    friendspace.model.close_db(error)
    return '', 204

@friendspace.app.route('/api/v1/likes/', methods = ['POST'])
def api_post_like():
    username = check_permission()
    postid = flask.request.args.get('postid')
    connection = friendspace.model.get_db()

    error = None
    try:
        cur = connection.execute(
            "SELECT likeid \
            FROM likes \
            WHERE postid = :postid AND owner = :owner",  
            {"postid":postid,
             "owner" :username}
        )
        prior_like = cur.fetchall()
        if len(prior_like) == 0:
            cur = connection.execute(
                "INSERT INTO likes (owner, postid) \
                VALUES (:owner, :postid)", 
                {'owner': username,
                'postid': postid}
            )
            likeid = cur.lastrowid
        else:
            likeid = prior_like[0]['likeid']
    except sqlite3.Error as e:
        if type(e) == sqlite3.IntegrityError:
            raise CustomError('Post Nonexist', 403)
        print(f"{type(e)}, {e}")
        error = e 
    friendspace.model.close_db(error)
    context = {
        'likeid': likeid,
        'url': flask.url_for('api_get_like_one', likeid = likeid)
    }
    if len(prior_like) == 0:
        return flask.jsonify(**context), 201
    else:
        return flask.jsonify(**context), 200

