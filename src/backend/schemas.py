from marshmallow import Schema, fields


class EventSchema(Schema):
    """Serialize and deserialize the Event object."""

    id = fields.Int()
    video_path = fields.Str()
    objects = fields.Str()
    event_time = fields.DateTime()
    video_length = fields.Int()
