import sys
import os
from dotenv import load_dotenv, find_dotenv
import logging


def create_data_path(pth: str, data_path: str = "logs") -> os.path:
    cwd = os.getcwd()
    p = os.path.join(cwd, data_path, pth)
    if not os.path.exists(p):
        os.mkdir(p)
    return p


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

d = load_dotenv(find_dotenv())
log.info(f"Env file Found?  ::  {d}")

DELAY = 3600  # seconds
HOURS = DELAY // 60 // 60

DO_API = "https://api.digitalocean.com/v2/"
LN_API = "https://api.linode.com/v4/"

ENDPOINT = "volumes"

PROVIDER = os.environ["PROVIDER"]
TOKEN = os.environ["TOKEN"]
VOLUME_NAME = os.environ["VOLUME_NAME"]
INCREASE_BY_PERCENTAGE = int(os.environ["INCREASE_BY_PERCENTAGE"])
BELOW_THIS_PERCENT_TO_RESIZE = int(os.environ["BELOW_THIS_PERCENT_TO_RESIZE"])

SEND_EMAIL = True if os.environ["SEND_EMAIL"].lower() == "true" else False
EMAIL_SMTP = os.environ["EMAIL_SMTP"]
EMAIL_PASS = os.environ["EMAIL_PASS"]
EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]

SEND_ALERT_TO_VSTATS = (
    True if os.environ["SEND_ALERT_TO_VSTATS"].lower() == "true" else False
)
VSTATS_TOKEN = os.environ["VSTATS_TOKEN"]
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