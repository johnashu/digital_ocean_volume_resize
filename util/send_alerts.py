from util._email import send_email
import logging as log
from includes.config import envs, VSTATS_API, hostname
from util.connect import connect_to_api


def send_to_vstats(
    subject: str, msg: str, alert_type: str, hostname: str = hostname
) -> None:
    if not envs.SEND_ALERT_TO_VSTATS:
        log.info("VSTATS not turned on, not sending Telegram Alerts")
        return
    j = {
        "api_token": envs.VSTATS_TOKEN,
        "alert-type": alert_type,
        "subject": subject,
        "message": msg,
        "hostname": hostname,
    }
    full, _, _ = connect_to_api("", VSTATS_API, "", j=j)
    log.info(full)


def send_error_alerts(e: str, volume_name: str, resize_msg: str) -> None:
    log.error("Sending Failed Alerts..")
    subject = f"Problem Resizing Volume ( {volume_name} ) on {hostname}"
    msg = f"There was a problem resizing your Volume\n\n\tAttempted to resize {resize_msg}\n\n\tThe following Error occured\n\n\t{e}\n\n\tPlease Check your node for more information"

    send_email(subject, msg)
    send_to_vstats(subject, msg, "error")


def send_success_alerts(msg: str, volume_name: str, resize_msg: str) -> None:
    log.info("Sending Success Alerts..")
    subject = f"Volume ( {volume_name} ) resized on {hostname}"
    msg = f"Volume ( {volume_name} ) has been resized successfully\n\n\t Resized {resize_msg}\n\n\t{msg}"

    send_email(subject, msg)
    send_to_vstats(subject, msg, "success")


def send_space_left_alert(
    volume_name: str, volume_percent_size_remaining: str, volume_size_remaining: str
) -> None:
    log.info("Sending Monitor Alerts..")
    subject = f"Volume Size Update -- {server_hostname}"
    msg = f"{volume_name} remaining space: <strong>{volume_size_remaining}GB ({volume_percent_size_remaining}%) </strong> \n\n\t"

    send_email(subject, msg)
    send_to_vstats(subject, msg, "space_left")
