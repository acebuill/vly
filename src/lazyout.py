import time
import sys
import re
from log import bold_str


def includes_pattern(string: str, pattern):
    return True if pattern.search(string) else False


def handle_error_output(input_: str):
    if re.compile(".*error:.*").search(input_):
        print("\r", end="")
        print(self.error_rgx.findall(input_)[0])
        self.finished = True


def get_action_match(input_: str):
    action_rgx = re.compile("::.*\\.\\.\\.")
    if includes_pattern(input_, action_rgx):
        return action_rgx.findall(input_)


def handle_action_output(input_: str):
    amatch = get_action_match(input_)
    if amatch:
        sys.stdout.write("\n" + amatch[0] + "\n")


def handle_progress_output(input_: str):
    progress_rgx = re.compile("\\(\d/\d\\)")
    if includes_pattern(input_, progress_rgx):
        sys.stdout.write(".")


def at_post_transaction(input_: str) -> bool:
    if get_action_match(input_):
        return "post-transaction" in get_action_match(input_)[0]
    return False


def handle_start_procedure_output(input_: str):
    procedure_rgx = re.compile("::.*\\]")
    if includes_pattern(input_, procedure_rgx):
        sys.stdout.write(
            bold_str("\n:: Poceeding with installation\n") + "\033[0m"
        )


class VlyPacmanLog:
    def __init__(self):
        sys.stdout.write("[Executing]".center(40, "-"))
        self.finished = False

    def write(self, input_: str):
        handle_start_procedure_output(input_)
        handle_error_output(input_)
        handle_action_output(input_)
        handle_progress_output(input_)
        if at_post_transaction(input_):
            self.__del__()

    def flush(_):
        return

    def __del__(self):
        if not self.finished:
            sys.stdout.write("-" * 40 + "\n")
        self.finished = True
