"""
env:
  media:
    refresh: true
    required_repository: multilib
    packages:
      mpv ffmpeg
      feh
"""
import yaml
import os
from pathlib import Path


def get_config_path(effective_user: str) -> str:
    return f"/home/{effective_user}/.config/vly/vly.yaml"


def config_exists(effective_user: str) -> str:
    return os.access(f"/home/{effective_user}/.config/vly/vly.yaml", os.F_OK)


def create_default_config(effective_user: str) -> bool:
    Path(f"/home/{effective_user}/.config/vly").mkdir(
        parents=True, exist_ok=True
    )
    open(get_config_path(effective_user), "w").write(__doc__)


def retrieve_group(group_name: str) -> dict:
    logname = os.getlogin()
    if config_exists(logname):
        with open(get_config_path(logname), "r") as config_file:
            return yaml.safe_load(config_file)["env"][group_name]
    else:
        raise Exception("Configuration file not found")
