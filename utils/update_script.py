import json
import os
import subprocess


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

    return config


def status_notification(status: bool, message: str) -> None:
    """
    Send notification based on outcome of other steps
    """
    # Not implemented yet
    if status is False:
        print(f"Notification would have been sent")


def back_up_dir(dir: str, volumes_root_dir: str) -> None:
    dir_path = os.path.join(volumes_root_dir, dir)
    os.chdir(dir_path)
    subprocess.call(["ls", "-l"])


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

    try:
        subprocess.call(["docker", "compose", "down"])
        subprocess.call(["docker", "compose", "pull"])
        subprocess.call(["docker", "compose", "up", "-d"])
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
        update_status, errors = update_docker_stack(
            stack, config["templates_root_directory"]
        )
        status_notification(update_status, message=f"Stack update failed")
