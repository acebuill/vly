import logging


logging.basicConfig(level=logging.INFO, format="%(message)s")


def bold_str(str_):
    return "\033[1m" + str_


def color_str(str_, color):
    return {"red": "\033[1;31m", "green": "\033[92m"}[color] + str_ + "\033[0m"


def log_ok(message):
    logging.info(color_str(bold_str("ok: "), "green") + message)


def log_err(message):
    logging.info(color_str(bold_str("error: "), "red") + message)


def log(message):
    logging.info(message)
