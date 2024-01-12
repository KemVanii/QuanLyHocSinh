# Import smtplib for the actual sending function
import smtplib
from app import app

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def send_email(me="redok1706@gmail.com", family=["2151053066tu@ou.edu.vn"]):
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = 'Our family reunion'
    # me == the sender's email address
    # family = the list of all recipients' email addresses
    msg['From'] = me
    msg['To'] = ', '.join(family)
    msg.preamble = 'Our family reunion'

    # Send the email via our own SMTP server.
    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.starttls()  # Enable TLS encryption
        s.login(me, 'prke zwdg nkyt slnq')  # Log in to your Gmail account
        s.send_message(msg)  # Send the email
