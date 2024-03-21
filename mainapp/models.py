from wtforms import Form, StringField, IntegerField, EmailField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Email, NumberRange
from .db_and_mail import db

# db Model
class AutoEmail(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    email_sender = db.Column(db.String, nullable=False)
    email_receiver = db.Column(db.String, nullable=False)
    email_subject = db.Column(db.String, nullable=False)
    email_content = db.Column(db.String, nullable=False)
    sent = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        return {
            "event_id": self.event_id,
            "email_subject": self.email_subject,
            "email_content": self.email_content,
            "timestamp": self.timestamp
        }

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


# WTForm model
class EmailForm(Form):
    event_id = IntegerField('Event Id', validators=[DataRequired()])
    email_subject = StringField('Email Subject', validators=[DataRequired()])
    email_content = StringField('Email Content', validators=[DataRequired()])
    timestamp = DateTimeField('Timestamp', format='%Y-%m-%dT%H:%M')


