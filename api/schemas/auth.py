from marshmallow import Schema, fields

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    name = fields.String(required=True)

class LogoutSchema(Schema):
    refresh_token = fields.String(required=True)

class RefreshSchema(Schema):
    access_token = fields.String(required=True)
