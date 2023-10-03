from flask import Blueprint, request

import database as db
from config import ADMIN_TOKEN
from database.trees import motels, motels_tree
from kdtree import KDTree
from utils.calc import form_to_point

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.before_request
def authenticate():
    """Authenticates the request.

    Responses:
        401: Unauthorized.
    """

    token = request.args.get("token")

    if token is None or token != ADMIN_TOKEN:
        return "Unauthorized", 401

@admin.route("/calculate")
def calculate():
    """Calculates the best match for each form.

    Responses:
        200: Calculated successfully.
    """

    points = []

    forms = db.forms.find({})
    all_forms = {}

    for form in forms:
        points.append(form_to_point(form))
        all_forms[form["_id"]] = form

    tree = KDTree(points, ignore_first_axis=True)

    for i, form_id in enumerate(all_forms):
        nn = tree.nearest_neighbor(points[i]).point
        bm_id = nn[0]
        bm = {
            "name": all_forms[bm_id]["name"],
            "age": all_forms[bm_id]["age"],
            "gender": all_forms[bm_id].get("gender", None),
        }

        nearest_motel = motels_tree.nearest_neighbor(
            [
                None,
                all_forms[bm_id]["mapPoint"]["lat"],
                all_forms[bm_id]["mapPoint"]["lng"],
            ]
        ).point[0]

        for m in motels:
            if m["name"] == nearest_motel:
                nearest_motel = m
                break

        db.results.update_one(
            {"_id": form_id},
            {
                "$set": {
                    "bestMatch": bm,
                    "perfectMatch": bool(tree.distance_sqr(points[i], nn) < 0.1),
                    "nearestEstablishment": nearest_motel,
                },
            },
            upsert=True,
        )

    return "OK"


@admin.route("/reset")
def reset():
    """Resets the database.

    Responses:
        200: Reset successfully.
    """

    db.forms.drop()
    db.results.drop()

    return "OK"
