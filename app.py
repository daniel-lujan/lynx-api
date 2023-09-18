from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()

from flask import Flask, Response, request
from pymongo.errors import DuplicateKeyError

from config import ALLOWED_EMAILS
from database import forms
from schemas import Form
from schemas.validator import validate_json

app = Flask(__name__)

@app.route("/form", methods = ["POST"])
@validate_json(Form)
def new_form():
    """Inserts a new form into the database.

    Responses:
        200: Form inserted successfully.
        400: Invalid JSON.
        403: Email not allowed.
        409: Form already exists.
    """
    
    if request.json["email"] not in ALLOWED_EMAILS:
        return Response(status = 403)
    
    form = request.json
    form["_id"] = form["email"].lower()
    del form["email"]

    try:
        forms.insert_one(form)
    except DuplicateKeyError:
        return Response(status = 409)

    return Response(status = 200)

if __name__ == "__main__":
    app.run(debug = True)