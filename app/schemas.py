from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

class TicketSchema(Schema):
    id = fields.Int(dump_only=True)
    eventName = fields.Str(required=True)
    location = fields.Str(required=True)
    time = fields.DateTime(required=True)
    isUsed = fields.Bool(dump_default=False)

    @validates('time')
    def validate_time(self, value, **kwargs):
        if value < datetime.now():
            raise ValidationError('waktu acara tidak boleh di masa lalu')