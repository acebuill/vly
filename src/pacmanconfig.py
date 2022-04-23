import os, sys, typing, re
import fileinput
from log import log, log_err, log_ok


get_env = lambda varname: os.getenv(varname.upper())


repo_mirror_path = (
    lambda repo_name: "/etc/pacman.d/mirrorlist-arch"
    if repo_name
    in [
        "multilib",
        "extra",
        "community",
        "testing",
        "community-testing",
        "multilib-testing",
    ]
    else Exception(repo_name + " is not implemented yet ...")
)


repo_include_string = (
    lambda repo_name, include_path: f"\n[{repo_name}]\nInclude = {include_path}\n"
)


has_write_permissions = lambda file_name: os.access(file_name, os.W_OK)


pacman_conf_path = (
    lambda testing: "/etc/pacman.conf" if not testing else "pacman.conf"
)


append_to_configuration_file = lambda string: open(
    pacman_conf_path(False), "a"
).write(string)


repo_is_enabled = lambda repo_name, pacman_config_file: re.compile(
    f"[^#]\\[{repo_name}\\]"
).search(open(pacman_config_file, "r").read())


repository_rgx = lambda repo_name: re.compile(
    f"(?:\n)?\\[{repo_name}\\]\nInclude(?: )?=(?: )?/.*(?:\n)?"
)


set_inline_parallel_downloads = (
    lambda parallel_n: lambda line: print(f"ParallelDownloads = {parallel_n}")
    if "ParallelDownloads" in line
    else print(line, end="")
)


def enable_repository(repo_name):
    if repo_is_enabled(repo_name, pacman_conf_path(False)):
        log_ok(f"{repo_name} is already enabled")
    else:
        if has_write_permissions(pacman_conf_path(False)):
            append_to_configuration_file(
                repo_include_string(
                    repo_name, repo_mirror_path(repo_name)
                )
            )
        else:
            raise Exception("config file does not have write permissions")
        log_ok(f"enabled {repo_name}")


def delete_repository_line(repo_name, pacman_config_path="/etc/pacman.conf"):
    if has_write_permissions(pacman_config_path):
        with open(pacman_config_path, "r+") as file_:
            new_file = re.sub(repository_rgx(repo_name), "", file_.read())
            file_.seek(0)
            file_.write(new_file)
            file_.truncate()
    else:
        raise Exception(
            f"root access is required in order to write to {pacman_config_path}"
        )


def disable_repository(repo_name: str, pacman_config_path="/etc/pacman.conf"):
    log(f"disabling {repo_name}")
    delete_repository_line(repo_name, pacman_config_path)
    log_ok(f"disabled {repo_name}")
    return True


def set_number_of_parallel_downloads(n: int):
    if has_write_permissions(pacman_conf_path(False)):
        for line in fileinput.input(pacman_conf_path(False), inplace=1):
            set_inline_parallel_downloads(n)(line)
        log_ok(f"set to {n} parallel downloads at the same time")
    else:
        log_err(f"either not enough permissions or config doesn't exist")


def check_include_path(path: str) -> bool:
    return os.path.exists(path)
