from log import log, log_ok, log_err
import operations
from root_access import acquire_root_privileges, request_root_pass
import typing
import pexpect


install_command = (
    lambda packages, refresh_repositories: f"pacman -S{'yyy' if refresh_repositories else ''} --noconfirm {packages}"
)


uninstall_command = (
    lambda packages, remove_unnecessary_deps: f"pacman -R{'s' if remove_unnecessary_deps else ''} --noconfirm {packages}"
)


def install_packages(
    packages: str, refresh_repositories: bool = False
) -> bool:
    log(f"Installing {packages}")
    return operations.was_successfull(
        child=operations.execute_with_root_privileges(
            install_command(packages, refresh_repositories)
        ),
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
            uninstall_command(packages, remove_unnecessary_dependencies)
        ),
        error_msg="error:",
        timeout_limit=240,
        operation_name="package removal",
        kill_child=True,
    )
