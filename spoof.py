import dkim

import smtplib

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

# catch socket errors when postfix isn't running...
from socket import error as socket_error


def send_email(
    to_email,
    sender_email,
    subject,
    message_text,
    message_html=None,
    relay="localhost",
    dkim_private_key_path="",
    dkim_selector="",
):
    sender_domain = sender_email.split("@")[-1]
    msg = MIMEMultipart("alternative")
    msg.attach(MIMEText(message_text, "plain"))
    #msg.attach(MIMEText(message_html, "html"))
    msg["To"] = to_email
    msg["From"] = sender_email
    msg["Subject"] = subject

    if dkim_private_key_path and dkim_selector:
        with open(dkim_private_key_path) as fh:
            dkim_private_key = fh.read()
        headers = ["To", "From", "Subject"]
        sig = dkim.sign(
            message=msg.as_string(),
            selector=str(dkim_selector),
            domain=sender_domain,
            privkey=dkim_private_key,
            include_headers=headers,
        )
        msg["DKIM-Signature"] = sig.lstrip("DKIM-Signature: ")

    # TODO: react if connecting to postfix is a socket error.
    s = smtplib.SMTP(relay)
    s.sendmail(sender_email, [to_email], msg.as_string())
    s.quit()
    return msg


if __name__ == "__main__":
    to = 'gary.frederick@students.makeschool.com'
    from_email = 'tania@makeschool.com'
    subject = 'Hello'
    path = '/Users/ghost/Tools/tiny/makeschool.com.20180605.pem'

    print(send_email(to, from_email, subject,
                     "biotch", "hi", dkim_private_key_path=path))
