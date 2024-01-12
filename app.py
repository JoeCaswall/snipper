from flask import Flask
from flask import request, abort, make_response, jsonify
import json

app = Flask(__name__)

with open("snippets.json", "r") as file:
    data = json.load(file)

languages = []

# List of languages in snippet dictionaries
for dictionary in data:
    if dictionary["language"] not in languages:
        languages.append(dictionary["language"])

# User can get all snippets
@app.route("/snippets/", methods=["GET"])
def show_all_snippets():
    return data

# User can get snippet by ID or add a new snippet with that ID
@app.route("/snippets/<int:id>", methods=["GET"])
def show_or_add_snippet_by_id(id):
    if request.method == "GET":
        for snippet in data:
            if snippet["id"] == id:
                return snippet

@app.route("/snippets/new/", methods=["POST"])
def add_new_snippet():
        request_data = request.get_json()
        # Checks formatting
        if "code" not in request_data or "language" not in request_data:
            response = make_response(jsonify({"error": "Bad Request - use code and language as keys"}), 400)
            return response
        else:
            ids = []
            for snippet in data:
                ids.append(snippet["id"])
            # Applies new ID based on highest existing one
            request_data["id"] = int(ids[-1]) + 1
            data.append(request_data)
            with open("snippets.json", "w") as outfile:
                outfile.write(json.dumps(data, indent=4))
            return data

# User can get snippet by language
@app.route("/snippets/<string:language>/", methods=["GET"])
def show_snippets_by_language(language):
    chosen = []
    language = language.lower()

    if language == "javascript":
        language = "JavaScript"
    else: language = language.title()

    if language in languages:
        for snippet in data:
            if snippet["language"] == language:
                chosen.append(snippet)
    return chosen
