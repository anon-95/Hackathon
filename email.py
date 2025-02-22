import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email Configuration
EMAIL = "mohillshackathon@gmail.com"
PASSWORD = "HACKMOHILLs123!"  
TO_EMAIL = "jiyafeby@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Function to send the email
def send_email(subject, body):
    try:
        # Set up the MIME
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = TO_EMAIL
        msg['Subject'] = subject
        
        # Add the body to the email
        msg.attach(MIMEText(body, 'plain'))

        # Connect to the server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(EMAIL, TO_EMAIL, text)
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print(f"Error: {e}")

# Reminder function
def send_reminder():
    subject = "Reminder: Take your ADHD meds!"
    body = "This is a reminder to take your ADHD meds. Don't forget!"
    send_email(subject, body)

# Scheduling the reminder
schedule.every().day.at("10:55).do(send_reminder)  # Change time as needed

# Running the scheduler
while True:
    schedule.run_pending()
    time.sleep(60)  # Wait a minute between checkss