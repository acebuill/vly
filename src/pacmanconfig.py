import os
import sys
import typing
import fileinput
import re
from log import log, log_err, log_ok


rgx = typing.NewType("rgx", re.Pattern)


def get_env_var(variable_name: str) -> str:
    return os.getenv(variable_name.upper())


def has_write_permissions(file: str) -> bool:
    return os.access(file, os.W_OK)


def get_artix_arch_mirror_path(mirror_name: str) -> str:
    available_mirrors = [
        "multilib",
        "extra",
        "community",
        "testing",
        "community-testing",
        "multilib-testing",
    ]
    if mirror_name in available_mirrors:
        return "/etc/pacman.d/mirrorlist-arch"
    raise Exception(f"{mirror_name} is not an artix arch supported mirror")


def get_mirror_include_path(mirror_name: str) -> str:
    artix_arch_mirror_path = "/etc/pacman.d/mirrorlist-arch"
    if os.path.exists(artix_arch_mirror_path):
        return get_artix_arch_mirror_path(mirror_name)
    else:
        raise Exception(f"{mirror_name} include path not implemented")


def mirror_is_enabled(
    mirror_name: str, pacman_config_path: str = "/etc/pacman.conf"
) -> bool:
    with open(pacman_config_path, "r") as file_:
        return bool(
            re.compile(f"[^#]\\[{mirror_name}\\]").search(file_.read())
        )


def enable_repository(
    mirror_name: str, pacman_config_path: str = "/etc/pacman.conf"
) -> bool:
    is_root = get_env_var("user") == "root"
    if mirror_is_enabled(mirror_name, pacman_config_path):
        log_ok(f"{mirror_name} is already enabled")
        return True
    if has_write_permissions(pacman_config_path):
        with open(pacman_config_path, "a") as pconfig:
            log(f"enabling {mirror_name}")
            pconfig.write(
                f"\n[{mirror_name}]\nInclude = {get_mirror_include_path(mirror_name)}\n"
            )
        log_ok(f"enabled {mirror_name}")
        return True
    else:
        raise Exception(
            f"not enoght permissions to write to {pacman_config_path}"
        )
        return False


def delete_repository_line(
    repository_name: str, pacman_config_path: str = "/etc/pacman.conf"
) -> bool:
    if has_write_permissions(pacman_config_path):
        repository_regex = re.compile(
            f"(?:\n)?\\[{repository_name}\\]\nInclude(?: )?=(?: )?/.*(?:\n)?",
            re.IGNORECASE,
        )
        with open(pacman_config_path, "r+") as file_:
            new_file = re.sub(repository_regex, "", file_.read())
            file_.seek(0)
            file_.write(new_file)
            file_.truncate()
            return True
    else:
        raise Exception(
            f"root access is required in order to write to {pacman_config_path}"
        )
        return False


def disable_repository(
    repository_name: str, pacman_config_path: str = "/etc/pacman.conf"
) -> bool:
    log(f"disabling {repository_name}")
    delete_repository_line(repository_name, pacman_config_path)
    log_ok(f"disabled {repository_name}")
    return True


def set_number_of_parallel_downloads(n: int, pacman_config_path: str) -> bool:
    is_root = get_env_var("user") == "root"
    if not is_root:
        return False
    for line in fileinput.input(pacman_config_path, inplace=1):
        if "ParallelDownloads" in line:
            line = f"ParallelDownloads = {n}"
        sys.stdout.write(line)
    return True


def check_include_path(path: str) -> bool:
    return os.path.exists(path)
