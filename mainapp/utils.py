import redis
from flask_mail import Message
from datetime import datetime
from mainapp.models import AutoEmail, Recipients
from mainapp.db_and_mail import db, mail
import json

redis_client = redis.Redis(
                host='redis-16065.c1.ap-southeast-1-1.ec2.cloud.redislabs.com', 
                port=16065, 
                db=0,
                password='esHMYwEgxXZ3mmHA7F8WPK5H2wpZ5flO'
            )

def background_task(app, mail):
    with app.app_context():
        # datetime_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # email_data = AutoEmail.query.filter_by(timestamp=datetime_now, sent=False).all()  
        # recipients = Recipients.query.all()
        # recipients_parsed = list(map(lambda x: x.to_string(), recipients))

        # if not email_data:
        #     return 
        
        # email_parsed = list(map(lambda x: x.to_json(), email_data))
        # for i in range(len(email_parsed)) :
        #     email = email_parsed[i]
        #     # Update sent = True for data has been sent 
        #     email_data[i].sent = True
        #     db.session.commit()
        redis_client.lpush('email_queue', json.dumps({"test": "Ini test"}))


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