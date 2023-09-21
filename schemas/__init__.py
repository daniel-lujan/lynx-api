from marshmallow import Schema, fields, validate

from schemas.constants import ALLOWED_MUSIC_GENRES


class Form(Schema):
    email = fields.Email(required = True)
    name = fields.String(required = True, validate = validate.Length(min = 1, max = 30))
    age = fields.Integer(required = True, validate = validate.Range(min = 1))
    gender = fields.String(validate = validate.OneOf(("f", "m")))
    favMusicGenres = fields.List(
        fields.String(validate = validate.OneOf(ALLOWED_MUSIC_GENRES)),
        required = True
    )
    moviesTaste = fields.Integer(required = True, validate = validate.Range(min = 0, max = 10))
    # ...
    mapPoint = fields.Dict(
        fields.String(validate = validate.OneOf(("latitude", "altitude"))),
        fields.Float(),
        required = True
    )