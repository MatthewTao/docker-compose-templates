import datetime as dt
import json
import os
import subprocess


UPDATE_STEPS = {
    "docker": {
        1: ["docker", "compose", "down"],
        2: ["docker", "compose", "pull"],
        3: ["docker", "compose", "up", "-d"],
    },
    "podman": {
        1: ["podman-compose", "down"],
        2: ["podman-compose", "pull"],
        3: ["podman-compose", "up", "-d"],
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
    config_location = os.path.join(get_location_of_script(), "config.json")
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


def back_up_dir(stack_details: dict, volumes_root_directory: str, backup_dir: str) -> None:
    volume_parent_location: str = stack_details.get(
        "volume_dir", volumes_root_directory
    )
    source_dir = stack_details["folder"]
    dir_path = os.path.join(volume_parent_location, source_dir)
    backup_path = os.path.join(backup_dir, f"{source_dir}_{dt.datetime.now().strftime('%Y%m%d%H%M%S')}.zip")
    os.chdir(dir_path)
    subprocess.call(["ls", "-l"])
    subprocess.call(["zip", "-rq", backup_path, dir_path])


def update_docker_stack(
    stack_details: dict, templates_root_directory: str
) -> tuple[bool, str]:
    template_parent_location: str = stack_details.get(
        "template_dir", templates_root_directory
    )
    template_directory = os.path.join(template_parent_location, stack_details["folder"])

    success: bool = False
    errors: str = ""
    try:
        os.chdir(template_directory)
    except Exception as e:
        print(f"Could not change directory {e}")
        errors += str(e)

    steps = UPDATE_STEPS[stack_details.get("stack_type", "docker")]
    try:
        for _, step in steps.items():
            subprocess.call(step)
    except Exception as e:
        # Continue updating other stack if failed
        # Maybe add some kind of notification
        print(f"Failed to update stack {e}")
        errors += str(e)
    else:
        success = True

    return success, errors


if __name__ == "__main__":
    config = get_config()

    for stack in config["stack_definitions"]:
        back_up_dir(stack, config["volumes_root_directory"], config["backup_root_directory"])
        
        update_status, errors = update_docker_stack(
            stack, config["templates_root_directory"]
        )
        
        status_notification(update_status, message=f"Stack update failed")
