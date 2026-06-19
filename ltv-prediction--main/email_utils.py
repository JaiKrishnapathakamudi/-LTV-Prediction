import smtplib
from email.mime.text import MIMEText

# -----------------------------------
# SEND RESET EMAIL
# -----------------------------------
def send_reset_email(

    receiver_email,
    reset_code

):

    sender_email = "your_email@gmail.com"

    sender_password = "your_app_password"

    subject = "Password Reset Code"

    body = f"""

Your password reset code is:

{reset_code}

"""

    msg = MIMEText(body)

    msg['Subject'] = subject

    msg['From'] = sender_email

    msg['To'] = receiver_email

    server = smtplib.SMTP(
        'smtp.gmail.com',
        587
    )

    server.starttls()

    server.login(
        sender_email,
        sender_password
    )

    server.sendmail(

        sender_email,

        receiver_email,

        msg.as_string()

    )

    server.quit()