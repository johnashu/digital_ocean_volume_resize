import psutil
from util.tools import flatten, process
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
def resize_hdd_linux(hdd_name):
    hdd_name = hdd_name.replace("-", "_")
    try:
        get_device = f"df -P /mnt/{hdd_name}" + " | awk 'END{print $1}'"
        device = process(get_device)
        log.info(device)
        resize = f"resize2fs {device}"
        resized = process(resize)
        log.info(resized)
        return True, resized
    except FileNotFoundError as e:
        return False, e


if __name__ == "__main__":
    volume = "volume_sfo3_02"
    space_left = check_hdd_size(volume)
    log.info(space_left)

    resize_hdd_linux(volume)
