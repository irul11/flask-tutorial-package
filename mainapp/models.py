from datetime import datetime
from .db_and_mail import db

# db Model
class AutoEmail(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    email_subject = db.Column(db.String, nullable=False)
    email_content = db.Column(db.String, nullable=False)
    sent = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        return {
            "event_id": self.event_id,
            "email_subject": self.email_subject,
            "email_content": self.email_content,
            "timestamp": self.timestamp,
        }

class Recipients(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)

    def to_json(self):
        return {
            "email": self.email,
        }
    
    def to_string(self):
        return self.email

# schema validate json
email_schema = {
    "type": "object",
    "properties": {
        "event_id": {"type": "integer"},
        "email_sender": {"type": "string", "format": "email"},
        "email_receiver": {"type": "string", "format": "email"},
        "email_subject": {"type": "string"},
        "email_content": {"type": "string"},
        "sent": {"type": "boolean"},
        "timestamp": {
            "type": "string", 
            # patter for date-time with format='%Y-%m-%dT%H:%M'
            "pattern": "^\\d{4}-[01]\\d-[0-3]\\dT[0-2]\\d:[0-5]\\d:[0-5]\\d$" 
        },
    },
    "required": ["event_id", "email_subject", "email_content", "timestamp"]
}

