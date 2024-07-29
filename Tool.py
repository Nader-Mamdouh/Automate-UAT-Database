import pyodbc
import datetime
import smtplib
from email.mime.text import MIMEText

# Database connection setup
server = 'your_server_name'
database = 'your_database_name'
username = 'your_username'
password = 'your_password'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Email setup
smtp_server = 'smtp.your_email_provider.com'
smtp_port = 587
smtp_username = 'your_email@example.com'
smtp_password = 'your_email_password'
recipient_email = 'recipient@example.com'

# Connect to the database
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Define the UAT retention period (in days)
uat_retention_period = 14

# Current date
current_date = datetime.datetime.now()

# Query to fetch UAT databases older than retention period
query = """
SELECT database_name, creation_date 
FROM your_database_table 
WHERE environment = 'UAT'
"""

cursor.execute(query)
databases = cursor.fetchall()

databases_to_delete = []

for database in databases:
    database_name, creation_date = database
    age_in_days = (current_date - creation_date).days
    if age_in_days > uat_retention_period:
        databases_to_delete.append(database_name)

# Function to delete databases
def delete_database(db_name):
    delete_query = f"DROP DATABASE {db_name}"
    cursor.execute(delete_query)
    conn.commit()
    log_deletion(db_name)

# Function to log deletions
def log_deletion(db_name):
    with open('deletion_log.txt', 'a') as log_file:
        log_file.write(f"{current_date}: Deleted database {db_name}\n")

# Function to send email notification
def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = recipient_email
    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, recipient_email, msg.as_string())

# Main process
if databases_to_delete:
    for db_name in databases_to_delete:
        delete_database(db_name)
    
    # Send notification email
    subject = "UAT Database Deletion Notification"
    body = f"The following UAT databases have been deleted:\n\n" + "\n".join(databases_to_delete)
    send_email(subject, body)

cursor.close()
conn.close()
