from marshmallow import Schema, fields


class ProfileSchema(Schema):
    access_token = fields.String(required=True)

