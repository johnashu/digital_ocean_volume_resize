import sys
import logging
import socket
from includes.config_utils import *

hostname = socket.gethostname()

create_data_path((""))

file_handler = logging.FileHandler(filename=os.path.join("logs", "data.log"))
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] <%(funcName)s> %(message)s",
    handlers=handlers,
    datefmt="%d-%m-%Y %H:%M:%S",
)

log = logging.getLogger()

envs = Envs()

DELAY = 3600 * envs.HOURS

DO_API = "https://api.digitalocean.com/v2/"
LN_API = "https://api.linode.com/v4/"

ENDPOINT = "volumes"

VSTATS_API = "https://vstats.one/api/volume-increase"

linnode_resize_instructions = """
you'll need to restart your Linode for the changes to take effect.

Once your Linode has restarted, make sure the volume is unmounted for safety:

Make sure the volume is unmounted for safety
umount /dev/disk/by-id/scsi-0Linode_Volume_{}

Assuming you have an ext2, ext3, or ext4 partition, first run a file system check, then resize it to fill the new volume size:

Run a file system check
e2fsck -f /dev/disk/by-id/scsi-0Linode_Volume_{}

Resize file system to fill the new volume
resize2fs /dev/disk/by-id/scsi-0Linode_Volume_{}

Now mount it back onto the filesystem:

Mount back onto the filesystem
mount /dev/disk/by-id/scsi-0Linode_Volume_{} /mnt/{}

"""
