import requests
import json

from util.tools import flatten
from includes.config import *


def connect_to_api(
    token: str,
    api: str,
    endpoint: str,
    call: requests = requests.get,
    j: dict = {},
    key: str = "",
    rtn_data: tuple = (),
    resize_msg="",
) -> dict:

    rtn = {}

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        r = call(api + endpoint, json=j, headers=headers)
        if r.status_code == 401:
            auth = "Authorisation failed [401] Please check your Token and regenerate a new one if required"
            log.error(auth)
            return auth, r.text, resize_msg
        data = r.json()
    except json.decoder.JSONDecodeError as e:
        data = r.text
        log.error(f"Problem with API {e}")

    try:
        if data.get("errors"):
            return data, data, resize_msg
        if data.get("id"):
            if data["id"] == "unprocessable_entity":
                return data, data, resize_msg
    except AttributeError as e:
        log.error(e)
        return data, data, e

    rtn = data

    if rtn_data:
        try:
            rtn = {k: v for k, v in data[key].items() if k in rtn_data}
        except (KeyError, AttributeError) as e:
            try:
                rtn = {k: v for k, v in data.items() if k in rtn_data}
            except AttributeError:
                pass

    return rtn, flatten(rtn), resize_msg


def resize_volume_digital_ocean(
    percentage_increase: int, volume_name: str, token: str, endpoint: str
) -> connect_to_api:
    # replace incase user takes the name from Ubuntu and not Provider..
    volume_name = volume_name.replace("_", "-")

    get_volume_data, _, _ = connect_to_api(
        token, DO_API, f"{endpoint}?name={volume_name}"
    )
    volumes = get_volume_data["volumes"]
    if not volumes:
        msg = f"No Volumes Found with the name  {volume_name}!"
        return get_volume_data, {}, msg

    volume = flatten([x for x in volumes if x["name"] == volume_name][0])
    size = volume["size_gigabytes"]
    volume_id = volume["id"]
    region = volume["slug"]
    new_size = size + round((size / 100 * int(percentage_increase)), None)

    j = {"type": "resize", "size_gigabytes": new_size, "region": region}  # slug
    e = f"{endpoint}/{volume_id}/actions"

    resize_msg = f"Digital Ocean Volume ( {volume_name} ) resizing from {size} GB -> {new_size} GB"
    log.info(f"Resizing {resize_msg}")

    return connect_to_api(
        token,
        DO_API,
        e,
        j=j,
        call=requests.post,
        key="action",
        rtn_data=("type", "id", "status"),
        resize_msg=resize_msg,
    )


def resize_volume_linnode(
    percentage_increase: int, volume_name: str, token: str, endpoint: str
) -> connect_to_api:

    # replace incase user takes the name from Ubuntu and not Provider..
    volume_name = volume_name.replace("_", "-")

    get_volume_data, _, _ = connect_to_api(token, LN_API, endpoint)
    volumes = get_volume_data["data"]
    if not volumes:
        msg = f"No Volumes Found with the name  {volume_name}!"
        return get_volume_data, {}, msg
    volume = flatten([x for x in volumes if x["label"] == volume_name][0])
    size = int(volume["size"])
    volume_id = volume["id"]
    new_size = size + round((size / 100 * int(percentage_increase)), None)

    j = {"size": new_size}  # slug
    e = f"{endpoint}/{volume_id}/resize"

    resize_msg = (
        f"Lin Node Volume ( {volume_name} ) resizing from {size} GB -> {new_size} GB"
    )
    log.info(f"Resizing {resize_msg}")

    return connect_to_api(
        token,
        LN_API,
        e,
        resize_msg=resize_msg,
        j=j,
        call=requests.post,
        rtn_data=("size", "id", "status"),
    )
