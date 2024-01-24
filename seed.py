import json
from Models import Snippet, User, db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy import Index
from sqlalchemy.orm import relationship, backref, sessionmaker

from cryptography.fernet import Fernet
import bcrypt

import os
from dotenv import load_dotenv

load_dotenv()
my_key = os.getenv("KEY")

fernet = Fernet(my_key)

with open("snippets.json", "r") as file:
    data=json.load(file)

salt = bcrypt.gensalt()

def seed(dataset):
    """creates initial data in database for testing purposes"""
    for snippet in dataset:
        snippet["code"] = snippet["code"].encode()
        snippet["code"] = fernet.encrypt(snippet["code"])
        new_snippet = Snippet(code=snippet["code"], language=snippet["language"].lower())
        db.session.add(new_snippet)
    test_password = "".encode("utf-8") #TODO: enter your test password here
    hash = bcrypt.hashpw(test_password, salt)
    test_user = User(email="anemail@gmail.com", password=hash)
    db.session.add(test_user)
    db.session.commit()