from marshmallow import Schema, fields, validate

from schemas.constants import ALLOWED_MUSIC_GENRES, PERSON_CHARACTERISTICS


class Form(Schema):
    email = fields.Email(required=True, validate=validate.Length(min=1, max=50))
    name = fields.String(required=True, validate=validate.Length(min=1, max=30))
    age = fields.Integer(required=True, validate=validate.Range(min=0))
    gender = fields.String(validate=validate.OneOf(("f", "m")))
    moviesTaste = fields.Integer(required=True, validate=validate.Range(min=0, max=10))
    concertsTaste = fields.Integer(
        required=True, validate=validate.Range(min=0, max=10)
    )
    partiesTaste = fields.Integer(required=True, validate=validate.Range(min=0, max=10))
    favMusicGenres = fields.List(
        fields.String(validate=validate.OneOf(ALLOWED_MUSIC_GENRES)),
        required=True,
        validate=validate.Length(min=0, max=4),
    )
    mostImportantAttr = fields.String(validate=validate.OneOf(PERSON_CHARACTERISTICS))
    catsOrDogs = fields.Integer(required=True, validate=validate.OneOf((0, 1)))
    messiOrCristiano = fields.Integer(required=True, validate=validate.OneOf((0, 1)))
    backOrFront = fields.Integer(required=True, validate=validate.OneOf((0, 1)))
    marvelOrDC = fields.Integer(required=True, validate=validate.OneOf((0, 1)))
    mapPoint = fields.Dict(
        fields.String(validate=validate.OneOf(("lat", "lng"))),
        fields.Float(),
        validate=validate.Length(equal=2),
        required=True,
    )
