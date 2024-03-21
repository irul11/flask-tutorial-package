from flask import Blueprint, g, render_template, request, current_app
from flask_mail import Message
from jsonschema import validate, ValidationError
from .models import AutoEmail, email_schema
from .db_and_mail import mail, db

main_bp = Blueprint('main_bp', __name__)
@main_bp.route("/")
@main_bp.route("/home")
def home():
    email_data = AutoEmail.query.all()    
    parsed_data = list(map(lambda x: x.to_json(), email_data))
    
    return render_template("index.html", query=parsed_data)

@main_bp.route("/testing")
def testing():
    try:
        # Create message object
        msg = Message('Testing Flask-Mail',
                    sender='your-email@example.com',
                    recipients=['amtaqiy11@gmail.com'])
        # Add email body
        msg.body = 'This is a test email sent from Flask-Mail'
        
        # Send email
        mail.send(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return str(e)

@main_bp.route("/save_emails", methods=["POST", "GET"])
def save_emails():
    event_id = request.args.get('event_id', type=int)
    email_receiver = request.args.get('email_receiver', type=str) 
    email_sender = request.args.get('email_sender', type=str) 
    email_subject = request.args.get('email_subject', type=str) 
    email_content = request.args.get('email_content', type=str)
    timestamp = request.args.get('timestamp', type=str)

    # TODO: Below is just for testing
    email_sender = "sender@example.com"
    email_receiver = "receiver@example.com"

    data = {
        "event_id": event_id, 
        "email_sender": email_sender, 
        "email_receiver": email_receiver, 
        "email_subject": email_subject, 
        "email_content": email_content, 
        "timestamp": timestamp
    }
    
    try:
        validate(instance=(data), schema=email_schema)
        if request.method == "POST":
            saved_data = AutoEmail(
                event_id=event_id,
                email_sender=email_sender, 
                email_receiver=email_receiver, 
                email_subject=email_subject, 
                email_content=email_content, 
                timestamp=timestamp
            )
            db.session.add(saved_data)
            db.session.commit()
            return {
                "message": "save data successful"
            }
    except ValidationError as e:
        return {
            "message": e.message,
            "param_error": e.json_path,
        }, 400
    except Exception as e:
        error_message = ""
        if "message" not in e.__dir__() and "orig" in e.__dir__():
            error_message = e.orig
        else:
            error_message = e.message
        return {
            "message": str(error_message),
        }, 400

    return {
        "data": data
    }

# def checking_email():
#     with app.app_context():
#         while True:
#             try:
#                 # Use a separate database session within the thread
#                 with app.app_context():
#                     email_data = AutoEmail.query.all()
#                     app.logger.info(email_data)
#             except Exception as e:
#                 app.logger.error(f"Error in background task: {e}")
#             time.sleep(10)
    