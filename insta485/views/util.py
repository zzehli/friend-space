import insta485
import os
import pathlib
import uuid
import hashlib

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

def query_user_following(user):
    """
    Query ppl the user is following, not including themselves, also their photos
    """
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT users.username, users.filename \
        FROM users \
        INNER JOIN (SELECT DISTINCT username2 \
            FROM following \
            WHERE username1 = :user) AS f \
            ON users.username = f.username2", {"user": user}
    )
    users = cur.fetchall()
    return users

def query_user_post(user):
    """
    Query all post of the user, without comments and likes; for user page
    """
    error = None
    try:
        connection = insta485.model.get_db()
        cur = connection.execute(
            "SELECT * \
                FROM posts \
                WHERE owner = (?)", (user,)
        )
        posts = cur.fetchall()
    except sqlite3.Error as e:
        print(f"{type(e)}, {e}")
        error = e
    insta485.model.close_db(error)
    return posts

def query_user_follower(user):
    """
    Query ppl the user's followers, also their photos
    """
    error = None

    try:
        connection = insta485.model.get_db()
        cur = connection.execute(
            "SELECT users.username, users.filename \
            FROM users \
            INNER JOIN (SELECT DISTINCT username1 \
                FROM following \
                WHERE username2 = :user) AS f \
                ON users.username = f.username1", {"user": user}
        )
        users = cur.fetchall()

    except sqlite3.Error as e:
        print(f"{type(e)}, {e}")
        error = e
    insta485.model.close_db(error)
    return users
