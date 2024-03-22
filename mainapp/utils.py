from flask_mail import Message
from datetime import datetime
from .models import AutoEmail, Recipients
from .db_and_mail import db


def background_task(app, mail):
    with app.app_context():
        datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        email_data = AutoEmail.query.filter_by(timestamp=datetime_now, sent=False).all()  
        recipients = Recipients.query.all()
        recipients_parsed = list(map(lambda x: x.to_string(), recipients))

        if not email_data:
            return 
        
        email_parsed = list(map(lambda x: x.to_json(), email_data))
        for i in range(len(email_parsed)) :
            email = email_parsed[i]
            send_email(
                mail=mail,
                subject=email["email_subject"],
                body=email["email_content"],
                recipients=recipients_parsed
            )
            # Update sent = True for data has been sent 
            email_data[i].sent = True
            db.session.commit()


def send_email(mail, subject, body, recipients):
    try:
        # Create message object
        msg = Message(subject=subject,
                    sender=('Email Scheduler','your-email@example.com'),
                    recipients=recipients)
        # Add email body
        msg.body = body
        
        # Send email
        mail.send(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return str(e)