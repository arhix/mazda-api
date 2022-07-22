from apiflask import Schema
from apiflask.fields import String, Boolean
from apiflask.validators import OneOf


class MazdaAuth(Schema):
    email = String(required=True)
    password = String(required=True)
    region = String(required=False, validate=OneOf(['MNAO', 'MME', 'MJO']), default="MNAO")

class DoorsStatus(Schema):
    doorsClosed = Boolean(required=True, default=True)
    doorsLocked = Boolean(required=True, default=True)
    windowsClosed = Boolean(required=True, default=True)
