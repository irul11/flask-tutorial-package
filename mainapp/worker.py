import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import time
import redis
from mainapp.utils import send_email


redis_client = redis.Redis(
                host='redis-16065.c1.ap-southeast-1-1.ec2.cloud.redislabs.com', 
                port=16065, 
                db=0,
                password='esHMYwEgxXZ3mmHA7F8WPK5H2wpZ5flO'
            )

def process_tasks():
    while True:
        # Dequeue task from Redis queue
        task_data = redis_client.rpop('email_queue')

        # Check if queue is empty
        if not task_data:
            print("No tasks remaining in the queue. Exiting...")
            time.sleep(1)
            continue

        # Process task (e.g., send email)
        email = json.loads(task_data)
        # send_email(email['email_subject'], email['email_content'], email['recipients'])
        print("Processed task:", email)

if __name__ == '__main__':
    process_tasks()
    print("Worker script has finished processing all tasks.")