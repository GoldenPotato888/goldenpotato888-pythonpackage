import ssl, smtplib
from email.message import EmailMessage

def send_email(sender, app_pswd, reciever, SUBJECT, msg_body):
    sender_email = sender
    app_password = app_pswd
    receiver_email = reciever
    subject = SUBJECT
    body = msg_body

    smtp_server = "smtp.gmail.com"
    port = 465

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")