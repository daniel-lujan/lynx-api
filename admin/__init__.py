from flask import Blueprint

import database as db
from kdtree import KDTree
from utils.calc import form_to_point

admin = Blueprint("admin", __name__, url_prefix="/admin")


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

        db.results.insert_one(
            {
                "_id": form_id,
                "bestMatch": bm,
                "perfectMatch": tree.distance_sqr(points[i], nn) < 0.1,
                "nearestEstablishment": {},
            }
        )

    return "OK"
