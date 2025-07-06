from marshmallow import Schema, fields


class TodoCreateDTO(Schema):
    task = fields.String(required=True)


class TodoUpdateDTO(Schema):
    task = fields.String()
    completed = fields.Boolean(required=True)


class TodoQueryParams(Schema):
    limit = fields.Integer(load_default=10)
    search = fields.String(required=False)
