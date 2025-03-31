import datetime as dt
import json
import os
import subprocess
import time

UPDATE_STEPS = {
    "docker": {
        "stop": ["docker", "compose", "down"],
        "update": ["docker", "compose", "pull"],
        "start": ["docker", "compose", "up", "-d"],
    },
    "podman": {
        "stop": ["podman-compose", "down"],
        "update": ["podman-compose", "pull"],
        "start": ["podman-compose", "up", "-d"],
    },
}


def get_location_of_script() -> str:
    """
    Returns the absolute location of the script
    With that location, we can locate the path of other required files.
    """
    return os.path.dirname(os.path.abspath(__file__))


def get_config() -> dict:
    """
    Reads and returns the config file
    """
    config_location_file = os.path.join(get_location_of_script(), "path_to_config.json")
    
    with open(config_location_file, "r") as config_location_file:
        config_location = json.load(config_location_file).get("path_to_config")
        assert config_location, "Path to config not specified. Please create one as per `path_to_config.json.example"

    with open(config_location, "r") as config_file:
        config = json.load(config_file)

    # Check that the config file has the necessary items
    assert (
        config.get("stack_definitions") is not None
    ), "Config is missing `stack_definitions`"
    assert (
        config.get("templates_root_directory") is not None
    ), "Config is missing `templates_root_directory`"
    assert (
        config.get("volumes_root_directory") is not None
    ), "Config is missing `volumes_root_directory`"
    assert (
        config.get("backup_root_directory") is not None
    ), "Config is missing `backup_root_directory`"

    return config


def status_notification(status: bool, message: str) -> None:
    """
    Send notification based on outcome of other steps
    """
    # Not implemented yet
    if status is False:
        print(f"Notification would have been sent")


def stop_stack(steps):
    print(f"{dt.datetime.now().isoformat()} - Stop Stack")
    stop_step = steps.get("stop")
    subprocess.call(stop_step)
    print(f"{dt.datetime.now().isoformat()} - Stopped Stack")
    return True

    
def back_up_dir(stack_details: dict, volumes_root_directory: str, backup_dir: str) -> None:
    print(f"{dt.datetime.now().isoformat()} - Start Backup process")
    if stack_details.get("skip_backup") == "True":
        # If the stack is not meant to be backed up, return and do nothing
        return
    volume_parent_location: str = stack_details.get(
        "volume_dir", volumes_root_directory
    )
    source_dir = stack_details["folder"]
    dir_path = os.path.join(volume_parent_location, source_dir)
    backup_path = os.path.join(backup_dir, f"{source_dir}_{dt.datetime.now().strftime('%Y%m%d%H%M%S')}.zip")
    print(backup_path)
    print(dir_path)
    os.chdir(dir_path)
    subprocess.call(["ls", "-l"])
    subprocess.call(["zip", "-rq", backup_path, dir_path])
    print(f"{dt.datetime.now().isoformat()} - Finished Backup process")


def update_stack(steps, template_directory):
    print(f"{dt.datetime.now().isoformat()} - Start Update Stack")
    os.chdir(template_directory)
    update_step = steps.get("update")
    subprocess.call(update_step)
    print(f"{dt.datetime.now().isoformat()} - Finished Update Stack")
    return True


def start_stack(steps):
    print(f"{dt.datetime.now().isoformat()} - Starting Stack")
    start_step = steps.get("start")
    subprocess.call(start_step)
    print(f"{dt.datetime.now().isoformat()} - Started Stack")


def update_docker_stack(
    stack_details: dict, templates_root_directory: str
) -> tuple[bool, str]:
    template_parent_location: str = stack_details.get(
        "template_dir", templates_root_directory
    )
    template_directory = os.path.join(template_parent_location, stack_details["folder"])

    stop_completed: bool = False
    update_completed: bool = False
    success: bool = False
    errors: str = ""
    try:
        os.chdir(template_directory)
    except Exception as e:
        print(f"Could not change directory {e}")
        errors += str(e)

    stack_type = stack_details.get("stack_type", "docker")
    steps = UPDATE_STEPS[stack_type]
    try:
        stop_completed = stop_stack(steps)

        back_up_dir(stack_details, config["volumes_root_directory"], config["backup_root_directory"])

        update_completed = update_stack(steps, template_directory)
        
        start_stack(steps)
    except Exception as e:
        # Continue updating other stack if failed
        # Maybe add some kind of notification
        print(f"Failed to update stack {e}")
        errors += str(e)

        if stop_completed is False and update_completed is False:
            # No need to do anything
            pass
        elif stop_completed is True and update_completed is False:
            print("Should just start the container again")
        elif stop_completed is True and update_completed is True:
            print("Something might be wrong with the start command or config")

    else:
        success = True

    return success, errors


def get_pause_duration() -> int:
    """
    Docker hub has got some restrictions on how many pulls can happen in an hour now.
    For now, just return a static wait.

    Maybe in the future can make it configurable depending on where the image is from
    """
    pause_duration = 60 * 60  # Seconds in an hour
    print(f"{dt.datetime.now().isoformat()} - Waiting for {pause_duration} seconds before moving on")
    return pause_duration


if __name__ == "__main__":
    config = get_config()

    for stack in config["stack_definitions"]:        
        update_status, errors = update_docker_stack(
            stack, config["templates_root_directory"]
        )
        
        status_notification(update_status, message=f"Stack update failed")
        time.sleep(get_pause_duration())
