import psutil
from includes.config import PROVIDER, linnode_resize_instructions
from util.tools import process
import logging as log

# check HDD size
def check_hdd_size(hdd_name: str) -> psutil:
    hdd_name = hdd_name.replace("-", "_")
    hdd_name = f"/mnt/{hdd_name}"
    obj_Disk = psutil.disk_usage(hdd_name)
    # log.info(obj_Disk.total / (1024.0 ** 3))
    # log.info(obj_Disk.used / (1024.0 ** 3))
    # log.info(obj_Disk.free / (1024.0 ** 3))
    return int(round(obj_Disk.percent, None))


# resize HDD in Linux
def resize_hdd_linux(hdd_name: str) -> tuple:
    hdd_name = hdd_name.replace("-", "_")
    try:
        get_device = f"df -P /mnt/{hdd_name}" + " | awk 'END{print $1}'"
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
                    if PROVIDER == 'LN':
                        linnode_error = f'{error_msg}\n\n Please follow these instructions from Linnode\n{linnode_resize_instructions.format(hdd_name,hdd_name,hdd_name,hdd_name,hdd_name)}'
                        log.error(linnode_error)
                        return False, linnode_error
                    log.error(error_msg)
                    return False, error_msg
            except IndexError as e:
                log.error(f"Resizing Did not complete on System\n{e}")
                return False, error_msg
        return True, resized
    except FileNotFoundError as e:
        return False, f"Resizing Did not complete on System\n\n{e}"


if __name__ == "__main__":
    volume = "volume_sfo3_02"
    space_left = check_hdd_size(volume)
    log.info(space_left)

    resize_hdd_linux(volume)
