import os
import psutil
import time

from ntfy_connector import NtfyConnectorStd


FIVE_MINUTES = 60 * 5

device_name = os.environ.get("DEVICE_NAME", "testing")
topic = os.environ.get("ALERT_NTFY_TOPIC")
check_frequency = int(os.environ.get("CHECK_FREQEUNCY", FIVE_MINUTES))

on_battery = False
half_battery = False

if __name__ == "__main__":
    print(f"Begin checking status of device ({device_name=}, {topic=})")
    if not topic:
        raise Exception("No NTFY topic defined, add ALERT_NTFY_TOPIC to env vars")
    ntfy_connector = NtfyConnectorStd(topic)
    while True:
        battery_status = psutil.sensors_battery()
        plugged_in = battery_status.power_plugged
        seconds_left = battery_status.secsleft
        percent = battery_status.percent
        if not plugged_in and not on_battery:
            on_battery = True
            message = f"{device_name} on battery power now, {seconds_left}s left"
            ntfy_connector.push_notification(message)
        elif on_battery and not half_battery and percent < 50:
            half_battery = True
            message = f"{device_name} is on less than half battery now ({percent=}"
            try:
                message += f", {int(seconds_left)}s left)"
            except:
                message += ")"
            ntfy_connector.push_notification(message)
        elif plugged_in and on_battery:
            on_battery = False
            half_battery = False
            message = f"{device_name} on AC power now"
            ntfy_connector.push_notification(message)

        time.sleep(check_frequency)
