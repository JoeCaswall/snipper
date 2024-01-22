import json
from Models import Snippet, User, db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy import Index
from sqlalchemy.orm import relationship, backref, sessionmaker

from cryptography.fernet import Fernet

import os
from dotenv import load_dotenv

load_dotenv()
my_key = os.getenv("KEY")

fernet = Fernet(my_key)

with open("snippets.json", "r") as file:
    data=json.load(file)

def seed(dataset):
    for snippet in dataset:
        snippet["code"] = snippet["code"].encode()
        print(snippet)
        new_snippet = Snippet(code = fernet.encrypt(snippet["code"]), language=snippet["language"])
        db.session.add(new_snippet)
    db.session.commit()