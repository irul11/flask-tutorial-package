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
