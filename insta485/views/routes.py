import flask
import insta485
import sqlite3
import uuid
import arrow
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

# @insta485.app.route('/comments/')
# def view_comments():
#   return "comments"

# @insta485.app.route('/comments/<int:commentid>/')
# def view_comment_one(commentid):
#   return "comment"

# @insta485.app.route('/likes/<int:likeid>/')
# def view_like(likeid):
#   return "like"

# @insta485.app.route('/posts/<postid>/')
# def view_post(postid):
#   return "post"

# @insta485.app.route('/users/<user_url_slug>/')
# def view_user(user_url_slug):
#   return "user"

@insta485.app.route('/users/<user_url_slug>/')
def user(user_url_slug):
    #check url is valid against exiting users
    cur = insta485.model.get_db().execute(
        "SELECT fullname \
            FROM users \
            WHERE username = (?)", (user_url_slug,)
    )
    user = cur.fetchone()
    if user == None:
        flask.abort(404)    
    own_post = query_user_post(user_url_slug)
    followers = query_user_follower(user_url_slug)
    logname_follows_username = False
    for u in followers:
        if u['username'] == flask.session['user']:
            logname_follows_username = True

    context = {"logname": flask.session['user'],
               "username": user_url_slug,
               "total_posts": len(own_post),
               "followers": len(followers),
               "following": len(query_user_following(user_url_slug)),
               "logname_follows_username": logname_follows_username,
               "fullname": user['fullname'],
               "posts": own_post}
    return flask.render_template("user.html", **context)

@insta485.app.route('/users/<user_url_slug>/followers/')
def followers(user_url_slug):
    followers = query_user_follower(user_url_slug)
    loguser_following_list = query_user_following(flask.session['user'])
    loguser_following = {x['username']:x for x in loguser_following_list}
    for u in followers:
        if u['username'] in loguser_following.keys():
            u['logname_follows_username'] = True
        else:
            u['logname_follows_username'] = False
    context = {"followers": followers,
               "username": user_url_slug,
               "logname": flask.session['user']}
    return flask.render_template("followers.html", **context)


@insta485.app.route('/users/<user_url_slug>/following/')
def following(user_url_slug):
    following = query_user_following(user_url_slug)
    loguser_following_list = query_user_following(flask.session['user'])
    loguser_following = {x['username']:x for x in loguser_following_list}
    for u in following:
        if u['username'] in loguser_following.keys():
            u['logname_follows_username'] = True
        else:
            u['logname_follows_username'] = False
    context = {"following": following,
               "username": user_url_slug,
               "logname": flask.session['user']}
    return flask.render_template("following.html", **context)

@insta485.app.route('/posts/<postid_url_slug>/')
def post(postid_url_slug):
    if 'user' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    error = None
    #image
    try:
        connection = insta485.model.get_db()
        cur = connection.execute(
            "SELECT postid, owner, u.userimage, p.filename, created \
             FROM posts p\
             LEFT JOIN (SELECT username, filename as userimage \
                        FROM users) u \
             ON username = owner \
             WHERE postid = (?)", (postid_url_slug,)
        )
        post = cur.fetchall()

    except sqlite3.Error as e:
        print(f"{type(e)}, {e}")
        error = e
    
    #likes
    try:
        
        cur = connection.execute(
            "SELECT COUNT(*) as c from likes \
            WHERE postid = (?)", (postid_url_slug,)
        )
        likes = cur.fetchall()

    except sqlite3.Error as e:
        print(f"{type(e)}, {e}")
        error = e
   
    #comments
    try:
        
        cur = connection.execute(
            "SELECT text, owner, commentid \
            FROM comments \
            WHERE postid = (?) \
            ORDER BY commentid", (postid_url_slug,)
        )
        comments = cur.fetchall()

    except sqlite3.Error as e:
        print(f"{type(e)}, {e}")
        error = e

    try:
        cur = connection.execute(
            "SELECT count(*) as c \
            FROM likes \
            WHERE postid = :postid AND owner = :owner",  
            {"postid":postid_url_slug,
             "owner" :flask.session['user']}
        )
        liked = cur.fetchone()
    except sqlite3.Error as e:
        print(f"{type(e)}, {e}")
        error = e
    insta485.model.close_db(error)
    formated_time = arrow.get(post[0]["created"], 'YYYY-MM-DD HH:mm:ss')
    timestamp = formated_time.humanize()
    context = {"postid": post[0]["postid"],
               "owner": post[0]["owner"],
               "owner_img_url": post[0]["userimage"],
               "img_url": post[0]["filename"],
               "timestamp": timestamp,
               "likes": likes[0]['c'],
               "liked": liked['c'],
               "comments": comments}
    return flask.render_template("post.html", **context)

@insta485.app.route("/explore/")
def explore():
    if 'user' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    error = None
    #image
    try:
        connection = insta485.model.get_db()
        cur = connection.execute(
            "SELECT username, filename \
             FROM users"
        )
        user_list = cur.fetchall()
    except sqlite3.Error as e:
        print(f"{type(e)}, {e}")
        error = e
    insta485.model.close_db(error)

    # user_dict = {x['username']: x['filename'] for x in all}

    following = query_user_following(flask.session['user'])
    following_list = [x['username'] for x in following]
    discover = []
    for u in user_list:
        if u['username'] not in following_list and u['username'] != flask.session['user']:
            discover.append(u)
    
    context = {"not_following": discover}
    return flask.render_template("explore.html", **context)

@insta485.app.route('/likes/', methods = ['POST'])
def post_likes():
    if 'user' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    url = flask.request.args.get('target')
    operation = flask.request.form['operation']
    postid = flask.request.form['postid']
    error = None

    
    connection = insta485.model.get_db()

    if operation == 'like':
        try:
            connection.execute(
                "INSERT INTO likes (owner, postid)\
                VALUES (:owner, :postid)", 
                {'owner': flask.session['user'],
                'postid': postid}
            )
        except sqlite3.Error as e:
            error = e 
    elif operation == 'unlike':
        try:
            connection.execute(
                "DELETE FROM likes\
                WHERE postid = :postid AND owner = :owner", 
                {'owner': flask.session['user'],
                 'postid': postid}
            )
        except sqlite3.Error as e:
            print(f"{type(e)}, {e}")
            error = e

    insta485.model.close_db(error)
    if url == None:
        return flask.redirect(flask.url_for('index'))
    else:
        return flask.redirect(url)

@insta485.app.route('/comments/', methods = ['POST'])
def post_comments():
    if 'user' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    url = flask.request.args['target']
    operation = flask.request.form['operation']

    error = None  
    connection = insta485.model.get_db()

    if operation == 'create':
        postid = flask.request.form['postid']
        text = flask.request.form['text']
        if text == "":
            flask.abort(400)
        try:
            connection.execute(
                "INSERT INTO comments (owner, postid, text)\
                VALUES (:owner, :postid, :text)", 
                {'owner': flask.session['user'],
                'postid': postid,
                'text': text}
            )
        except sqlite3.Error as e:
            print(f"{type(e)}, {e}")
            error = e 
    elif operation == 'delete':
        commentid = flask.request.form['commentid']
        try:
            connection.execute(
                "DELETE FROM comments\
                WHERE commentid = (?)", 
                (commentid,)
            )
        except sqlite3.Error as e:
            print(f"{type(e)}, {e}")
            error = e 
    
    insta485.model.close_db(error)
    if url == None:
        return flask.redirect(flask.url_for('index'))
    else:
        return flask.redirect(url)

@insta485.app.route('/posts/', methods = ['POST'])
def post_posts():
    if 'user' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    operation = flask.request.form['operation']

    error = None  
    connection = insta485.model.get_db()

    if operation == "create":
        file = flask.request.files['file']
        filename = serialize_save(file)
        #insert filename to DB
        try:
            connection.execute(
                "INSERT INTO posts (filename, owner)\
                VALUES (:filename, :owner)", 
                {'owner': flask.session['user'],
                'filename': filename}
            )
        except sqlite3.Error as e:
            print(f"{type(e)}, {e}")
            error = e 


    elif operation == "delete":
        postid = flask.request.form['postid']
        try:
            connection.execute(
                "DELETE FROM posts\
                WHERE postid = (?)", 
                (postid,)
            )
        except sqlite3.Error as e:
            print(f"{type(e)}, {e}")
            error = e 


    insta485.model.close_db(error)
    url = flask.request.args['target']
    if url == None:
        return flask.redirect('index')
    return flask.redirect(url)

@insta485.app.route('/following/', methods = ['POST'])
def post_follow():
    if 'user' not in flask.session:
        return flask.redirect(flask.url_for('login'))
    operation = flask.request.form['operation']
    username = flask.request.form['username']

    error = None  
    connection = insta485.model.get_db()
    if operation == 'follow':
        try:
            connection.execute(
                "INSERT INTO following (username1, username2)\
                VALUES (:usernam1, :username2)", 
                {'usernam1': flask.session['user'],
                'username2': username}
            )
        except sqlite3.Error as e:
            print(f"{type(e)}, {e}")
            error = e 
            flask.abort(409)
    elif operation == 'unfollow':
        print('unfollow')
        try:
            connection.execute(
                "DELETE FROM following \
                WHERE username1 = :username1 AND username2 = :username2",
                {'username1': flask.session['user'],
                'username2': username}
            )
        except sqlite3.Error as e:
            print(f"{type(e)}, {e}")
            error = e 
    insta485.model.close_db(error)
    url = flask.request.args['target']
    if url == None:
        return flask.redirect('index')
    return flask.redirect(url)