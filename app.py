from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv(".env.development")

from flask import Flask, Response, request
from flask_cors import CORS
from pymongo.errors import DuplicateKeyError

from admin import admin
from config import PORT
from database import forms, results
from schemas import Form
from schemas.validator import validate_json

app = Flask(__name__)

app.register_blueprint(admin)

CORS(app)


@app.route("/form/<email>", methods=["GET"])
def get_form(email: str):
    """Returns a form by email.

    Responses:
        200: Form retrieved successfully.
        404: Form not found.
    """

    form = forms.find_one({"_id": email.lower()})

    if form is None:
        return Response(status=404)

    return form


@app.route("/form", methods=["POST"])
@validate_json(Form)
def new_form():
    """Inserts a new form into the database.

    Responses:
        200: Form inserted successfully.
        400: Invalid JSON.
        409: Form already exists.
    """

    form = request.json
    form["_id"] = form["email"].lower()
    del form["email"]

    try:
        forms.insert_one(form)
    except DuplicateKeyError:
        return Response(status=409)

    return Response(status=200)

@app.route("/results/<email>", methods=["GET"])
def get_results(email: str):
    """Returns the results for an user.

    Route Params:
        `email`: The email of the user.

    Responses:
        200: Results retrieved successfully.
        404: Results not found for the user.
    """

    r = results.find_one({"_id": email.lower()})

    if r is None:
        return Response(status=404)
    
    return r
    

if __name__ == "__main__":
    app.run(port=PORT, debug=True)
