import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from .utils import background_task



def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_object("config")
    app.config.from_pyfile("config.py")
    
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SECRET_API_KEY'] = os.environ.get('SECRET_API_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')


    from .db_and_mail import db, mail
    db.init_app(app)
    mail.init_app(app)

    from .views import main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

        # Add task/scheduler for handling checking email from database
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=background_task, args=(app, mail), trigger='interval', seconds=1, max_instances=10)
        scheduler.start()

    return app