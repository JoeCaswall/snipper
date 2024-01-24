from flask import Flask, request, abort, make_response, jsonify
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
    for snippet in snippets:
        snippet.code = fernet.decrypt(snippet.code).decode()
    return jsonify([each_snippet.to_json() for each_snippet in snippets])

# User can get snippet by ID 
@app.route("/snippets/<int:id>/", methods=["GET"])
def show_snippet_by_id(id):
    snippet = Snippet.query.get_or_404(id)
    snippet.code = fernet.decrypt(snippet.code).decode()
    return jsonify(snippet.to_json())

# User can add a new snippet
@app.route("/snippets/new/", methods=["POST"])
def add_new_snippet():
    request_data = request.get_json()
    request_data["code"] = fernet.encrypt(request_data["code"].encode())
    new_snippet = Snippet(code=request_data["code"], language=request_data["language"])
    db.session.add(new_snippet)
    db.session.commit()
    return "Snippet added successfully!"

# User can get snippet by language
@app.route("/snippets/<string:language>/", methods=["GET"])
def show_snippets_by_language(language):
    snippets = Snippet.query.all()
    for snippet in snippets:
        snippet.code = fernet.decrypt(snippet.code).decode()
    correct_languages = Snippet.query.filter(Snippet.language == language.lower())
    return jsonify([snippet.to_json() for snippet in correct_languages])

