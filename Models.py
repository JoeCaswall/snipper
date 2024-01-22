from flask import Flask, request, abort, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    __tablename__ = "users"
    id: id = db.Column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password:Mapped[str]

class Snippet(db.Model):
    __tablename__ = "snippets"
    id:Mapped[int] = mapped_column(primary_key=True)
    code:Mapped[str]
    language:Mapped[str]

    def to_json(self):
        return {
            'id': self.id,
            'code': self.code,
            'language': self.language
        }

