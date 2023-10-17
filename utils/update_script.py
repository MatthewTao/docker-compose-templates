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
    return config


def back_up_dir(dir: str, volumes_root_dir: str) -> None:
    dir_path = os.path.join(volumes_root_dir, dir)
    os.chdir(dir_path)
    subprocess.call(["ls", "-l"])


def update_docker_stack(stack_details: dict, templates_root_directory: str) -> None:
    template_parent_location: str = stack_details.get(
        "template_dir", templates_root_directory
    )
    template_directory = os.path.join(template_parent_location, stack_details["folder"])

    os.chdir(template_directory)
    subprocess.call(["docker", "compose", "down"])
    subprocess.call(["docker", "compose", "pull"])
    subprocess.call(["docker", "compose", "up", "-d"])


if __name__ == "__main__":
    config = get_config()

    for stack in config.get("stack_definitions"):
        update_docker_stack(stack, config["templates_root_directory"])
