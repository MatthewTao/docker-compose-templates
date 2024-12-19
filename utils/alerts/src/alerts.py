import logging
import os
import psutil
import time

from ntfy_connector import NtfyConnectorStd


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
    ],
)

FIVE_MINUTES = 60 * 5

device_name = os.environ.get("DEVICE_NAME", "testing")
topic = os.environ.get("ALERT_NTFY_TOPIC")
check_frequency = int(os.environ.get("CHECK_FREQUENCY", FIVE_MINUTES))

on_battery = False
half_battery = False

if __name__ == "__main__":
    logging.info(f"Begin checking status of device ({device_name=}, {topic=}, {check_frequency=})")
    if not topic:
        err_msg = "No NTFY topic defined, add ALERT_NTFY_TOPIC to env vars"
        logging.exception(err_msg)
        raise Exception(err_msg)
    ntfy_connector = NtfyConnectorStd(topic)
    while True:
        battery_status = psutil.sensors_battery()
        plugged_in = battery_status.power_plugged
        seconds_left = battery_status.secsleft
        percent = battery_status.percent
        # print(f"Checked {battery_status=}, {plugged_in=}, {seconds_left=}, {percent=}")
        if not plugged_in and not on_battery:
            on_battery = True
            message = f"{device_name} on battery power now, {seconds_left}s left"
            logging.info(message)
            ntfy_connector.push_notification(message)
        elif on_battery and not half_battery and percent < 50:
            half_battery = True
            message = f"{device_name} is on less than half battery now ({percent=}"
            try:
                message += f", {int(seconds_left)}s left)"
            except:
                message += ")"
            logging.info(message)
            ntfy_connector.push_notification(message)
        elif plugged_in and on_battery:
            on_battery = False
            half_battery = False
            message = f"{device_name} on AC power now"
            logging.info(message)
            ntfy_connector.push_notification(message)

        time.sleep(check_frequency)
