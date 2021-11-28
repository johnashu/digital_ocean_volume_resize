from smtplib import SMTPException, SMTPHeloError, SMTPAuthenticationError
from smtplib import SMTP_SSL as SMTP  # SSL connection
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from includes.config import *


def send_email(subject: str, message: str) -> None:
    if not envs.SEND_EMAIL:
        log.info("Email sending not turned on, no email sent!")
        return

    msg = MIMEMultipart()

    msg["From"] = envs.EMAIL_FROM

    msg["To"] = envs.EMAIL_TO
    msg["Subject"] = subject
    msg.attach(MIMEText(message))

    ServerConnect = False

    try:
        smtp_server = SMTP(envs.EMAIL_SMTP, "465")
        smtp_server.login(envs.EMAIL_FROM, envs.EMAIL_PASS)
        ServerConnect = True
    except SMTPHeloError as e:
        log.error(f"Server did not reply  ::  {e}")
    except SMTPAuthenticationError as e:
        log.error(f"Incorrect username/password combination ::  {e}")
    except SMTPException as e:
        log.error(f"Authentication failed ::  {e}")

    if ServerConnect:
        try:
            smtp_server.sendmail(envs.EMAIL_FROM, envs.EMAIL_TO, msg.as_string())
            log.info(msg.as_string())
            log.info("Successfully sent email")
        except SMTPException as e:
            log.error(f"Unable to send email  ::  {e}")
        finally:
            smtp_server.close()
            log.info("Email server connection closed")


# send_email('VOLUME Resized', 'HELLO TEST')
