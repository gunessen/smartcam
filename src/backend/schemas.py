from marshmallow import Schema, fields


class EventSchema(Schema):
    """Serialize and deserialize the Event object."""

    id = fields.Int()
    video_path = fields.Str()
    objects = fields.Str()
    event_time = fields.DateTime()
    video_length = fields.Int()


class StatsSchema(Schema):
    """Serialize and deserialize the Stats object."""

    cpu_percent = fields.Int()
    ram_used_mb = fields.Int()
    ram_total_mb = fields.Int()
    ram_percent = fields.Int()
    disk_used_gb = fields.Int()
    disk_total_gb = fields.Int()
    disk_percent = fields.Int()
