from flask import Flask, request, abort, make_response, jsonify
import json

from Models import db, User, Snippet
from seed import seed, fernet, salt

import bcrypt

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
    correct_languages = Snippet.query.filter(Snippet.language == language.lower()).one()
    return [snippet.to_json() for snippet in correct_languages]

# Placeholder user page
@app.route("/snippets/users/")
def user_page():
    return "<h1>Send a request to login or signup</h1>"

# Can create a new user
@app.route("/snippets/users/signup/", methods=["POST"])
def user_sign_up():
    request_data = request.get_json()
    bytes = request_data["password"].encode("utf-8")
    hashed = bcrypt.hashpw(bytes, salt)

    new_user = User(email=request_data["email"], password=hashed)
    db.session.add(new_user)
    db.session.commit()
    return "Signup successful!"

# User can provide correct credentials and get a response containing their id and username
@app.route("/snippets/users/login/", methods=["GET"])
def user_login():
    request_data = request.get_json()
    target_email = request_data["email"]
    correct_user = User.query.filter(User.email == target_email).one()
    bytes = request_data["password"].encode("utf-8")
    hashed = bcrypt.hashpw(bytes, salt)
    stored_hash = correct_user.password
    if hashed == stored_hash:
        data_to_send = jsonify({"id": correct_user.id, "email": correct_user.email})
        response = make_response(data_to_send)
        response.status_code = 200
        return response
    else:
        response = make_response("<h1>Incorrect username or password</h1>")
        response.status_code = 401
        return response