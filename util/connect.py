import requests
from json import dump

from util.hdd_utils import *
from includes.config import *


def api_v2(
    token: str,
    endpoint: str,
    call: requests = requests.get,
    d: dict = {},
    key: str = "",
    rtn_data: tuple = (),
) -> dict:

    rtn = {}

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        r = call(DO_API + endpoint, json=d, headers=headers)
        data = r.json()
    except KeyError:
        data = r.text

    rtn = data

    if rtn_data:
        try:
            rtn = {k: v for k, v in data[key].items() if k in rtn_data}
        except (KeyError, AttributeError) as e:
            log.info(f"problem with response key, see error {e}")

    return rtn, flatten(rtn)


def resize_volume(
    percentage_increase: int, volume_name: str, token: str, endpoint: str
) -> api_v2:

    volumes = api_v2(token, endpoint.format(f"?name={volume_name}"))[0]["volumes"]
    volume = flatten([x for x in volumes if x["name"] == volume_name][0])
    size = volume["size_gigabytes"]
    volume_id = volume["id"]
    region = volume["slug"]
    new_size = size + (size // 100 * percentage_increase)

    d = {"type": "resize", "size_gigabytes": new_size, "region": region}  # slug
    e = f"{endpoint}{volume_id}/actions"

    log.info(f"Resizing Volume {volume_name} from {size} GB -> {new_size} GB")

    return api_v2(
        token,
        e,
        d=d,
        call=requests.post,
        key="action",
        rtn_data=("type", "id", "status"),
    )
