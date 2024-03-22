from flask import Blueprint, render_template, request
from jsonschema import validate, ValidationError
from datetime import datetime
from .models import AutoEmail, Recipients, email_schema
from .db_and_mail import db


main_bp = Blueprint('main_bp', __name__)

@main_bp.route("/")
@main_bp.route("/home")
def home():
    email_data = AutoEmail.query.filter_by(sent=False).order_by(AutoEmail.timestamp).limit(15).all()    
    parsed_data = list(map(lambda x: x.to_json(), email_data))
    
    return render_template("index.html", query=parsed_data)

@main_bp.route("/save_emails", methods=["POST"])
def save_emails():
    event_id = request.args.get('event_id', type=int)
    email_subject = request.args.get('email_subject', type=str) 
    email_content = request.args.get('email_content', type=str)
    timestamp = request.args.get('timestamp', type=str)

    data = {
        "event_id": event_id, 
        "email_subject": email_subject, 
        "email_content": email_content, 
        "timestamp": timestamp
    }
    
    try:
        validate(instance=(data), schema=email_schema)

        current_timestamp = datetime.now().timestamp()
        email_timestamp = datetime.fromisoformat(timestamp).timestamp()
        if email_timestamp < current_timestamp:
            raise ValidationError("the timestamp must be set for the future")

        if request.method == "POST":
            saved_data = AutoEmail(
                event_id=event_id,
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
        elif "message" in e.__dir__():
            error_message = e.message
        else:
            error_message = e
        return {
            "message": str(error_message),
        }, 400

    return {
        "data": data
    }


@main_bp.route("/recipients", methods=["POST", "DELETE"])
def save_recipients():
    email = request.args.get('email', type=str) 
    if request.method == "POST":
        saved_data = Recipients(
            email=email,
        )
        db.session.add(saved_data)
        db.session.commit()
        return {
            "message": "save recipient successful"
        }
