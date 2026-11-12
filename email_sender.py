import os
import smtplib


from email.message import EmailMessage

def send_management_email(summary):

    sender = os.getenv("SENDER_EMAIL")
    password = os.getenv("SENDER_APP_PASSWORD")
    recipient = os.getenv("RECIPIENT_EMAIL")

    if not sender or not password or not recipient:
        raise ValueError("Email configuration missing in .env")

    message = EmailMessage()

    message["Subject"] = (
        "Harbour View Hotel - Daily Operations Management Report"
    )

    message["From"] = sender
    message["To"] = recipient

    message.set_content(summary)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:

        server.starttls()

        server.login(sender, password)

        server.send_message(message)

    print("Management email sent successfully!")
    print(f"Recipient: {recipient}")