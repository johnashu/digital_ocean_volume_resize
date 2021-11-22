import psutil
from includes.config import PROVIDER, linnode_resize_instructions
from util.tools import process
import logging as log

# check VOLUME size
def check_volume_size(volume_name: str) -> dict:
    volume_name = volume_name.replace("-", "_")
    volume_name = f"/mnt/{volume_name}"
    obj_Disk = psutil.disk_usage(volume_name)
    # log.info(obj_Disk.total / (1024.0 ** 3))
    # log.info(obj_Disk.used / (1024.0 ** 3))
    # log.info(obj_Disk.free / (1024.0 ** 3))
    return {
        "total": int(round(obj_Disk.total / (1024.0 ** 3), None)),
        "used": int(round(obj_Disk.used / (1024.0 ** 3), None)),
        "free": int(round(obj_Disk.free / (1024.0 ** 3), None)),
        "percent": int(round(obj_Disk.percent, None)),
    }


# resize VOLUME in Linux
def resize_volume_linux(volume_name: str, org_volume_sizes: dict) -> tuple:
    volume_name = volume_name.replace("-", "_")
    try:
        get_device = f"df -P /mnt/{volume_name}" + " | awk 'END{print $1}'"
        device, error = process(get_device)
        log.info(device)
        resize = f"resize2fs {device}"
        resized, error = process(resize)
        log.info(resized)
        if error:
            not_resized_message = "do!"
            error_msg = f"Resizing Did not complete on System\nYou may need to restart your node.\n{error}"
            try:
                splits = error.split()
                if splits[-1].endswith(not_resized_message):
                    if PROVIDER == "LN":
                        linnode_error = f"{error_msg}\n\n Please follow these instructions from Linnode\n{linnode_resize_instructions.format(volume_name,volume_name,volume_name,volume_name,volume_name)}"
                        log.error(linnode_error)
                        return False, linnode_error
                    log.error(error_msg)
                    return False, error_msg
            except IndexError as e:
                log.error(f"Resizing Did not complete on System\n{e}")
                return False, error_msg

        # Check it is the correct size (ish)
        new_system_volume = check_volume_size(volume_name)
        new = new_system_volume["total"]
        org = org_volume_sizes["total"]
        for i in range(0, 1):
            if (new - i == org) or (new == org) or (new + 1 == org):
                return True, resized
        msg = f"Problem Resizing on the System.  Linux has told us it has been resized but the original and resized do not match. \nOriginal Size : {org} | New Size: {new}\n"
        log.error(msg)
        return False, msg
    except FileNotFoundError as e:
        return False, f"Resizing Did not complete on System\n\n{e}"


if __name__ == "__main__":
    volume = "volume_sfo3_02"
    space_left = check_volume_size(volume)
    log.info(space_left)

    # resize_volume_linux(volume)
