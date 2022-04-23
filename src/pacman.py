from log import log, log_ok, log_err
import operations
from root_access import acquire_root_privileges, request_root_pass
import typing
import pexpect


def get_install_command(
    packages: str, referesh_repositories: bool = False
) -> str:
    return (
        f"pacman -Syyy --noconfirm {packages}"
        if referesh_repositories
        else f"pacman -S --noconfirm {packages}"
    )


def get_uninstall_command(
    packages: str, remove_unnecessary_dependencies: bool = True
) -> str:
    return (
        f"pacman -Rs --noconfirm {packages}"
        if remove_unnecessary_dependencies
        else f"pacman -R --noconfirm {packages}"
    )


def install_packages(
    packages: str, refresh_repositories: bool = False
) -> bool:
    log(f"Installing {packages}")
    ch = operations.execute_with_root_privileges(
        get_install_command(packages, refresh_repositories)
    )
    return operations.was_successfull(
        child=ch,
        error_msg="error:",
        timeout_limit=3600,
        operation_name="package installation",
        kill_child=True,
    )


def uninstall_packages(
    packages: str, remove_unnecessary_dependencies: bool = True
) -> bool:
    log(f"uninstalling {packages}")
    return operations.was_successfull(
        operations.execute_with_root_privileges(
            get_uninstall_command(packages, remove_unnecessary_dependencies)
        ),
        error_msg="error:",
        timeout_limit=240,
        operation_name="package removal",
        kill_child=True,
    )
