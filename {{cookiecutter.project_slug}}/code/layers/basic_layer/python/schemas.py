import re
from datetime import datetime

from marshmallow import (
    Schema, fields, validate, validates, EXCLUDE, ValidationError,
)

from constants import DATE_FORMAT
from db_manager import EntityDatabaseManager


db = EntityDatabaseManager()


class EntitySchema(Schema):
    """Validation schema for custom entity."""

    uid = fields.UUID(required=False)
    email = fields.Email(required=True)
    birthdate = fields.String(required=True)
    message = fields.String(
        required=True, validate=validate.Length(min=1, max=250)
    )
    rating = fields.Integer(
        required=True, validate=validate.Range(min=1, max=10)
    )
    need_feedback = fields.Boolean(required=True, default=False)
    # Auto-generated fields
    created_at = fields.String(required=False, dump_only=True)
    updated_at = fields.String(required=False, dump_only=True)
    is_active = fields.Boolean(required=False, dump_only=True)

    class Meta:
        unknown = EXCLUDE
        fields = (
            "uid", "email", "birthdate", "message", "rating", "need_feedback",
            "created_at", "updated_at", "is_active",
        )
        ordered = True

    @validates("birthdate")
    def validate_birthdate(self, value):
        date_regex = r"^\d\d\d\d-(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])"
        if not re.match(date_regex, value):
            raise ValidationError(
                "String does not match expected pattern: YYYY-MM-DD"
            )
        try:
            datetime.strptime(value, DATE_FORMAT)
        except ValueError:
            raise ValidationError(
                "String does not match existed date"
            )

    @validates("email")
    def validate_email(self, value):
        items = db.find_by_email(value)
        if items:
            raise ValidationError(
                f"Record with email '{value}' already exists"
            )
