from time import sleep

from includes.config import *
from util.connect import resize_volume_linnode, resize_volume_digital_ocean
from util.volume_utils import check_volume_size, resize_volume_linux
from util.send_alerts import send_success_alerts, send_error_alerts, send_space_left_alert


def run(provider_info: tuple) -> None:
    func, provider = provider_info
    while True:
        resize_msg = ""
        try:
            # get VOLUME size %
            org_volume_sizes = check_volume_size(envs.VOLUME_NAME)
            volume_size_remaining = 100 - org_volume_sizes["percent"]
            log.info(f"VOLUME Size  ::  {volume_size_remaining}% Remaining..")

            if envs.SPACE_LEFT_ALERT == True:
                send_space_left_alert(envs.VOLUME_NAME, volume_size_remaining)


            # Check if it is < envs.BELOW_THIS_PERCENT_TO_RESIZE
            if volume_size_remaining <= envs.BELOW_THIS_PERCENT_TO_RESIZE:
                log.info(
                    f"VOLUME Size [ {volume_size_remaining}% ] is <= {envs.BELOW_THIS_PERCENT_TO_RESIZE}%.. Increasing size on {provider} volume {envs.VOLUME_NAME}"
                )
                # resize VOLUME on Digital Ocean
                full, flat, resize_msg = func(
                    envs.INCREASE_BY_PERCENTAGE, envs.VOLUME_NAME, envs.TOKEN, ENDPOINT
                )
                if flat.get("status") in ("done", "resizing"):
                    log.info(f"VOLUME Size increased.. Increasing size on System")
                    # resize on Linux
                    res, msg = resize_volume_linux(envs.VOLUME_NAME, org_volume_sizes)
                    if res:
                        log.info("VOLUME Resize Successful.. ")
                        # send email success
                        send_success_alerts(msg, envs.VOLUME_NAME, resize_msg)
                        log.info(f"sleeping for {envs.HOURS} Hour(s)..")

                    else:
                        log.error(f"Failed to resize volume on System..")
                        send_error_alerts(msg, envs.VOLUME_NAME, resize_msg)
                else:
                    log.error(
                        f"Failed to resize volume on {provider}\n{full}\n{flat}.."
                    )
                    send_error_alerts(full, envs.VOLUME_NAME, resize_msg)

            else:
                log.info(f"VOLUME Size is healthy, sleeping for {envs.HOURS} Hour(s)..")
        except Exception as e:
            send_error_alerts(e, envs.VOLUME_NAME, resize_msg)
            log.error(e)
            log.error(
                f"Error email sent, sleeping for {envs.HOURS} Hour(s).. Please fix me!"
            )
        sleep(DELAY)
        # Hot reload Env
        envs.load_envs()


providers = {
    "DO": (resize_volume_digital_ocean, "Digital Ocean"),
    "LN": (resize_volume_linnode, "LinNode"),
}

run(providers[envs.PROVIDER])

# For testing messages..
# send_to_vstats(f'Beans  ( volume-sfo3-11 )', 'On toast with Cheese', 'success')
