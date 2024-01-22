from flask import Flask, request, abort, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import json

from Models import db, User, Snippet
from seed import seed, fernet


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.sqlite"
db.init_app(app)

with open("snippets.json", "r") as file:
    data = json.load(file)

with app.app_context():
    db.drop_all()
    db.create_all()
    seed(data)

# User can get all snippets
@app.route("/snippets/", methods=["GET"])
def show_all_snippets():
    snippets = Snippet.query.all()
    some_snippets = jsonify([snippet.to_json() for snippet in snippets])
    for snippet in some_snippets:
        snippet["code"] = fernet.decrypt(snippet["code"])
    return jsonify([snippet.to_json() for snippet in some_snippets])

    

# User can get snippet by ID 
@app.route("/snippets/<int:id>/", methods=["GET"])
def show_snippet_by_id(id):
    snippet = Snippet.query.get_or_404(id)
    return jsonify(snippet.to_json())

# User can add a new snippet
@app.route("/snippets/new/", methods=["POST"])
def add_new_snippet():
    request_data = request.get_json()
    new_snippet = Snippet(code=request_data["code"], language=request_data["language"])
    db.session.add(new_snippet)
    db.session.commit()
    return jsonify(new_snippet.to_json())

# User can get snippet by language
@app.route("/snippets/<string:language>/", methods=["GET"])
def show_snippets_by_language(language):
    correct_languages = Snippet.query.filter(Snippet.language == language)
    return jsonify([snippet.to_json() for snippet in correct_languages])

