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
