from time import sleep

from util.connect import *
from util.hdd_utils import check_hdd_size, resize_hdd_linux
from util._email import send_email


def send_error_email(e: str) -> None:
    subject = f"[VALIDATOR ERROR] Problem Resizing HDD {VOLUME_NAME}"
    msg = f"There was a problem resizing your HDD\n\tThe following Error occured\n\t{e}\n\tPlease Check your node for more information"
    send_email(subject, msg)


def run() -> None:
    while True:
        try:
            # get HDD size %
            hdd_size_remaining = 100 - check_hdd_size(VOLUME_NAME)
            log.info(f"HDD Size  ::  {hdd_size_remaining}")

            # Check if it is < PERCENTAGE_TO_INCREASE
            if hdd_size_remaining <= PERCENTAGE_TO_INCREASE:
                log.info(
                    f"HDD Size is <= PERCENTAGE_TO_INCREASE.. Increasing size on Digital Ocean"
                )
                # resize HDD on Digital Ocean
                full, resize = resize_volume(
                    INCREASE_BY_PERCENTAGE, VOLUME_NAME, TOKEN, ENDPOINT
                )
                if resize["status"] == "done":
                    log.info(f"HDD Size increased.. Increasing size on System")
                    # resize on Linux
                    res, msg = resize_hdd_linux(VOLUME_NAME)
                    if res:
                        log.info("HDD Resize Successful.. ")
                        # send email success
                        if SEND_EMAIL:
                            log.info("Sending Email..")
                            success_subject = (
                                f"[VALIDATOR INFO] HDD {VOLUME_NAME} resized"
                            )
                            success_msg = f"HDD {VOLUME_NAME} has been resized\n\t{msg}\n\tsleeping for {DELAY // 60 // 60} Hour(s).."
                            send_email(success_subject, success_msg)
                    else:
                        log.error(f"Failed to rezie on System..")
                        send_error_email(msg)
                else:
                    log.error(f"Failed to rezie on Digital Ocean..")
                    send_error_email(full)

            else:
                log.info(
                    f"HDD Size is healthy, sleeping for {DELAY // 60 // 60} Hour(s).."
                )
        except Exception as e:
            send_error_email(e)
            log.error(e)
            log.error(
                f"Error email sent, sleeping for {DELAY // 60 // 60} Hour(s).. Please fix me!"
            )
        sleep(DELAY)


run()
