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

    cpu_percent = fields.Decimal()
    ram_used_mb = fields.Int()
    ram_total_mb = fields.Int()
    ram_percent = fields.Int()
    disk_used_gb = fields.Int()
    disk_total_gb = fields.Int()
    disk_percent = fields.Int()


class SettingsSchema(Schema):
    """Serialize and deserialize the Settings object."""

    motion_sensitivity = fields.Str()
    object_detection_model = fields.Str()
    camera_resolution = fields.Str()
    camera_fps = fields.Str()
    recording_length = fields.Str()
    notifications_active = fields.Bool()
    mailjet_api_key = fields.Str()
    mailjet_secret_key = fields.Str()
