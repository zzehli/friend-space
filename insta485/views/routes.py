import flask
import insta485
import sqlite3
import uuid
from insta485.views.util import *

@insta485.app.route('/accounts/login/')
def login():
    # error = None
    if 'user' in flask.session:
        return flask.redirect(flask.url_for('index'))

    return flask.render_template("login.html")

    
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

    elif operation == 'create':
        username = flask.request.form['username']
        fullname = flask.request.form['fullname']
        password = flask.request.form['password']
        salt = uuid.uuid4().hex
        password_hd = password_hash(salt, password)
        email = flask.request.form['email']
        file = flask.request.files['file']
        
        
        filename = serialize_save(file)

        try:
            connection.execute(
                "INSERT INTO users (username, fullname, email, filename, password)\
                VALUES (:u, :full, :email, :file, :p)", 
                {'u': username,
                'full': fullname,
                'email': email,
                'file': filename,
                'p': password_hd}
            )
        
        
        except sqlite3.Error as e:
            print(f"{type(e)}, {e}")
            error = e 
            if type(e) == sqlite3.IntegrityError:
                flask.abort(409)
        flask.session['user'] = username

    elif operation == 'delete':
        if 'user' not in flask.session:
            return flask.abort(403)
        
        user = flask.session['user']
        try:
            cur = connection.execute(
                "SELECT filename \
                FROM posts \
                WHERE owner = (?)", (user,)
            )
            post_file_list = cur.fetchall()
            #TODO delete user photo
            connection.execute(
                "DELETE FROM users \
                WHERE username = (?)", (user,)
            )
        except sqlite3.Error as e:
            print(f"{type(e)}, {e}")
            error = e
        for file in post_file_list:
            delete_image(file['filename'])
        flask.session.pop('user')
        
    elif operation == 'edit_account':
        if 'user' not in flask.session:
            return flask.abort(403)
        
        username = flask.session['user']
        fullname = flask.request.form['fullname']
        email = flask.request.form['email']
        file = flask.request.files['file']

        if fullname == None or email == None:
            flask.abort(400)

        if file != None:
            #replace existing photo and save
            new_name = serialize_save(file)
            try:
                cur = connection.execute(
                    "SELECT filename \
                    FROM users \
                    WHERE username = (?)", (username,)
                )
                old_photo = cur.fetchone()
                
                delete_image(old_photo['filename'])
                connection.execute(
                    "UPDATE users SET filename = :f \
                    WHERE username = :u", 
                                          {'f': new_name,
                                           'u': username}
                )
                
            except sqlite3.Error as e:
                print(f"{type(e)}, {e}")
                error = e 
        
        try:
                cur = connection.execute(
                    "UPDATE users \
                     SET fullname = :f, email = :e\
                    WHERE username = :u", {'f': fullname,
                                           'e': email,
                                           'u': username}
                )

        except sqlite3.Error as e:
                print(f"{type(e)}, {e}")
                error = e 

    elif operation == 'update_password':
        if 'user' not in flask.session:
            return flask.abort(403)
        
        user = flask.session['user']
        old_pw = flask.request.form['password']
        pw1 = flask.request.form['new_password1']
        pw2 = flask.request.form['new_password2']

        if None in [old_pw, pw1, pw2]:
            flask.abort(400)
        if pw1 != pw2:
            flask.abort(401)
        try:
            cur = connection.execute(
                "SELECT username, password \
                FROM users \
                WHERE username = (?)", (user,)
            )
            user_info = cur.fetchone()
        except sqlite3.Error as e:
            print(f"{type(e)}, {e}")
            error = e
        if user_info == None:
            flask.abort(403)

        
        old_salt = user_info['password'].split('$')[1]
        password_attempt = password_hash(old_salt, old_pw)
        if password_attempt != user_info['password']:
            flask.abort(403)

        salt = uuid.uuid4().hex
        new_pw = password_hash(salt, pw1)
        try:
            cur = connection.execute(
                "UPDATE users \
                SET password = :pw \
                WHERE username = :user", {'pw': new_pw,
                                          'user': user}
            )
           
        except sqlite3.Error as e:
            print(f"{type(e)}, {e}")
            error = e

    insta485.model.close_db(error)
    url = flask.request.args.get('target')
    if url == None:
        return flask.redirect(flask.url_for('index'))
    else:
        return flask.redirect(url)


@insta485.app.route('/accounts/logout/', methods = ['POST'])
def logout():
    flask.session.pop('user', None)
    return flask.redirect(flask.url_for('login'))

@insta485.app.route('/accounts/create/')
def create_account():
    if 'user' in flask.session:
        return flask.redirect(flask.url_for('edit_account'))
    
    return flask.render_template('create_account.html')

@insta485.app.route('/accounts/delete/')
def delete_account():
    if 'user' in flask.session:
        return flask.render_template('delete_account.html')
    return flask.redirect(flask.url_for('login'))

@insta485.app.route('/accounts/edit/')
def edit_account():
    if 'user' in flask.session:
        error = None
        try:
            connection = insta485.model.get_db()
            cur = connection.execute(
                "SELECT fullname, email, filename \
                FROM users\
                WHERE username = (?)", (flask.session['user'],)
            )
            file = cur.fetchone()

        except sqlite3.Error as e:
            error = e
        insta485.model.close_db(error)
        return flask.render_template('edit_account.html', **file)
    return flask.redirect(flask.url_for('login'))

@insta485.app.route('/accounts/password/')
def password():
    if 'user' in flask.session:
        return flask.render_template('password.html')
    return flask.redirect(flask.url_for('login'))

@insta485.app.route('/')
def index():
  if 'user' in flask.session:

    return flask.render_template("index.html")
  return flask.redirect(flask.url_for('login'))

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