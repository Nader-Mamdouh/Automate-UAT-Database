# UAT Database Retention Script

This script is designed to manage and automate the deletion of User Acceptance Testing (UAT) databases that have exceeded a specified retention period. It connects to a SQL Server database, identifies UAT databases older than the retention period, deletes them, logs the deletions, and sends an email notification summarizing the deletions.

## Features

- Connects to a SQL Server database using ODBC.
- Identifies UAT databases older than a specified retention period.
- Deletes the identified databases.
- Logs the deletions to a file.
- Sends an email notification with details of the deleted databases.

## Requirements

- Python 3.x
- pyodbc
- smtplib
- email

## Setup

1. **Install Dependencies**

    ```sh
    pip install pyodbc
    ```

2. **Database Configuration**

    Update the database connection details in the script:
    
    ```python
    server = 'your_server_name'
    database = 'your_database_name'
    username = 'your_username'
    password = 'your_password'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    ```

3. **Email Configuration**

    Update the email server details:
    
    ```python
    smtp_server = 'smtp.your_email_provider.com'
    smtp_port = 587
    smtp_username = 'your_email@example.com'
    smtp_password = 'your_email_password'
    recipient_email = 'recipient@example.com'
    ```

4. **Retention Period**

    Define the UAT retention period in days:
    
    ```python
    uat_retention_period = 14
    ```

## Usage

1. **Run the Script**

    Execute the script to delete old UAT databases:
    
    ```sh
    python delete_older_uat_databases.py
    ```

2. **Logging**

    The deletions will be logged to a file named `deletion_log.txt` in the same directory.

3. **Email Notification**

    An email notification will be sent to the specified recipient with details of the deleted databases.

## Script Details

- **Database Query**

    The script fetches UAT databases using the following query:
    
    ```sql
    SELECT database_name, creation_date 
    FROM your_database_table 
    WHERE environment = 'UAT'
    ```

- **Deletion and Logging**

    For each database older than the retention period, the script executes a `DROP DATABASE` command and logs the deletion to `deletion_log.txt`.

- **Email Notification**

    The script sends an email with the subject "UAT Database Deletion Notification" and the body containing a list of deleted databases.

