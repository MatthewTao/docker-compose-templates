import dataclasses
import datetime as dt
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
SECONDS_IN_HOUR = 60 * 60

device_name = os.environ.get("DEVICE_NAME", "testing")
topic = os.environ.get("ALERT_NTFY_TOPIC")
low_threshold = int(os.environ.get("LOW_THRESHOLD", 20))
check_frequency = int(os.environ.get("CHECK_FREQUENCY", FIVE_MINUTES))
log_progress = int(os.environ.get("LOG_PROGRESS", 1))
if log_progress > 1:
    raise Exception("LOG_PROGRESS must be 1 or 0")

on_battery = False
three_quarters_battery = False
half_battery = False
low_battery = False

dead_letter_queue = []


def show_appropriate_value(seconds_left) -> str:
    if not isinstance(seconds_left, int) and not isinstance(seconds_left, float):
        # Not an int or float ... psutil can use their custom representation for infinite
        # Just the string of it will do while I haven't quite seen it in real life yet.
        return repr(seconds_left)
    
    if seconds_left > SECONDS_IN_HOUR:
        value = seconds_left / 3600
        unit = "hrs"
    elif seconds_left > FIVE_MINUTES:
        value = seconds_left / 60
        unit = "mins"
    else:
        value = seconds_left
        unit = "s"
    return f"{value:.2f} {unit}"


@dataclasses.dataclass
class DeadMessage:
    message: str
    first_emitted: dt.datetime


if __name__ == "__main__":
    logging.info(
        f"Begin checking status of device ({device_name=}, {topic=}, {check_frequency=})"
    )
    if not topic:
        err_msg = "No NTFY topic defined, add ALERT_NTFY_TOPIC to env vars"
        logging.exception(err_msg)
        raise Exception(err_msg)
    ntfy_connector = NtfyConnectorStd(topic)

    seconds_left = 0
    while True:
        battery_status = psutil.sensors_battery()
        plugged_in = battery_status.power_plugged
        previous_seconds_left = seconds_left
        seconds_left = battery_status.secsleft
        percent = battery_status.percent

        if log_progress == 1 and percent < 95:
            logging.debug(f"{battery_status=}, {plugged_in=}, {seconds_left=}, {percent=}")

        if not plugged_in and not on_battery:
            on_battery = True
            message = f"{device_name} on battery power now. Battery at {percent}%"
            logging.info(message)
        
        elif on_battery and not three_quarters_battery and percent < 75:
            three_quarters_battery = True
            message = f"{device_name} is on less than 75% battery now ({percent=}"
            try:
                message += f", {show_appropriate_value(seconds_left)} left)"
            except:
                message += ")"
            logging.info(message)

        elif on_battery and not half_battery and percent < 50:
            half_battery = True
            message = f"{device_name} is on less than half battery now ({percent=}"
            try:
                message += f", {show_appropriate_value(seconds_left)} left)"
            except:
                message += ")"
            logging.info(message)
        
        elif on_battery and not low_battery and percent < low_threshold:
            low_battery = True
            message = f"{device_name} is on low battery now ({percent=}"
            try:
                message += f", {show_appropriate_value(seconds_left)} left)"
            except:
                message += ")"
            logging.info(message)

        elif plugged_in and on_battery:
            on_battery = False
            three_quarters_battery = False
            half_battery = False
            low_battery = False
            message = f"{device_name} on AC power now. Was at {percent}%"
            try:
                message += f", {show_appropriate_value(previous_seconds_left)} left."
            except:
                message += "."
            logging.info(message)
        else:
            message = None

        if message:
            try:
                ntfy_connector.push_notification(message)
            except Exception as e:
                logging.error(f"Failed to send message {repr(e)}")
                dead_letter_queue.append(
                    DeadMessage(message=message, first_emitted=dt.datetime.now())
                )

        if dead_letter_queue:
            logging.warning(f"Dead letter queue length: {len(dead_letter_queue)}")
            for i in range(len(dead_letter_queue)):
                item = dead_letter_queue.pop(0)
                try:
                    ntfy_connector.push_notification(
                        f"{item.first_emitted.isoformat()} - {item.message}"
                    )
                except Exception as e:
                    logging.error(f"Failed to resend message {repr(e)}")
                    # For now, I believe the only method of failure is when the Wi-Fi is down.
                    # Therefore, I'll keep the simpler infinite loop retry
                    dead_letter_queue.append(item)
                else:
                    logging.info(f"successfully resent message: {item.message}")


        time.sleep(check_frequency)
