import logging
from main import app, LOG_FILE

logging.basicConfig(
    filename=app.env == "development" and LOG_FILE or "",
    filemode="w",
    level=logging.ERROR,
    format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
)


def logger(name: str) -> logging.Logger:
    lo = logging.getLogger(name)
    lo.setLevel(logging.DEBUG)
    return lo
