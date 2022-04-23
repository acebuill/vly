from log import log_ok, log_err, log
import typing
import pexpect
from root_access import (
    acquire_root_privileges,
    request_root_pass,
    PASSWORD_REQUIRED_MSG,
)


def execute_with_root_privileges(operation: str) -> pexpect.pty_spawn.spawn:
    root_child = acquire_root_privileges(
        request_root_pass(PASSWORD_REQUIRED_MSG)
    )
    root_child.sendline(operation)
    return root_child


def was_successfull(
    child: pexpect.pty_spawn.spawn,
    error_msg: str,
    timeout_limit: int,
    operation_name: str,
    kill_child: bool = False,
) -> bool:
    log("verifying operation success")
    child.sendline(r"echo $32\n")
    if child.expect([error_msg, "2n"], timeout=timeout_limit) > 0:
        if kill_child:
            child.terminate(True)
        log_ok(f"{operation_name} success")
        return True
    log_err(f"{operation_name} fail")
    return False
