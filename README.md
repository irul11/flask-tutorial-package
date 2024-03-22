# [Email Scheduler](https://flask-email-scheduler.vercel.app/)

Email scheduler is endpoint for scheduling an email to someone.

## Packages
All package installed to do this application available in [`/main/requirement.txt`](https://github.com/irul11/flask-tutorial-package/blob/main/requirements.txt).

## Database and ORM
### Database
The database used in this application is PostgreSQL which is hosted on [Supabase](https://supabase.com/).\
I use two tables, named `autoemail` and `recipients`. The `autoemail` table functions to store event_id, email_subject, email_content, timestamp, and sent, while the recipients table functions to store the emails of recipients who will receive scheduled emails.
### ORM
The ORM used in this application is [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/), because Flask-SQLAlchemy is an orm commonly used in python.

## Packaging the web app
Because I am still not an expert in manual deployment, therefore I tried using a free deployment provider service. However, most of the free deploy providers ask for a credit card and I don't have one so I can't use it :(\
So in the end I used [Vercel](https://vercel.com/) to deploy this application which this app can be accessed [here](https://flask-email-scheduler.vercel.app/).

## Main Core of Automation
### Script
In this application, there is a script that continuously checks the time from the database and then sends an email if the timestamp is the same as the current time. I use the `APScheduler` library to handle this, so the app can handle requests from other people and check scheduled emails.\
The script that continuously checks and adds tasks to the queue is contained in the code [`/mainapp/__init__.py`](https://github.com/irul11/flask-tutorial-package/blob/main/mainapp/__init__.py). For more details, the script can be seen below 
```python

...
from apscheduler.schedulers.background import BackgroundScheduler
from .utils import background_task


def create_app():
        ...
        # Add task/scheduler for handling checking email from database
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=background_task, args=(app, mail), trigger='interval', seconds=1, max_instances=10)
        scheduler.start()
        ...

```
From the code above, `scheduler` variable will run in background of app and always do the `background_task()` function from [`.utils`](https://github.com/irul11/flask-tutorial-package/blob/main/mainapp/utils.py). The following is the `background_task()` code in the `.utils` module
```python

...
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
            ...

```
The purpose of this function is to check the data in the autoemail table every second, if there is data whose timestamp is the same as current datetime then this function will send email data related to that timestamp to the recipients in the recipients table.

### Obstacle
Vercel is a serverless platform and has limited control over configuration. So for applications that require a specific server configuration or runtime environment, this limitation can be a drawback. This causes tasks or functions that run on the background scheduler to not run, so the script to carry out continuous checks and add tasks to the queue does not run, and sending scheduled emails cannot be done automatically.
