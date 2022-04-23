from getpass import getpass
import pexpect
import typing
import lazyout
from log import log
import operations


PASSWORD_REQUIRED_MSG = "password is needed for this operation "


def acquire_root_privileges(password: str) -> pexpect.pty_spawn.spawn:
    log("acquiring root privilege")
    child = pexpect.spawn("sudo su", encoding="utf-8")
    child.logfile = lazyout.VlyPacmanLog()
    child.expect("password for")
    child.sendline(password)
    if operations.was_successfull(
        child, "Sorry, try again.", 3.1, "root acquisition"
    ):
        return child
    raise Exception("wrong password or sudo timout")


def request_root_pass(request_msg: str) -> str:
    return getpass(request_msg + ":\t")
