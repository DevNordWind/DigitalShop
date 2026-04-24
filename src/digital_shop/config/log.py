import logging
from dataclasses import dataclass
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Final

import colorlog

__all__ = ("LoggingConfig", "setup_root_logger")

_STDOUT_FORMAT: Final[str] = (
    "%(log_color)s%(levelname)-8s%(reset)s | "
    "%(cyan)s%(asctime)s%(reset)s | "
    "%(blue)s%(filename)s:%(lineno)d%(reset)s | "
    "%(white)s%(message)s"
)
_FILE_FORMAT: Final[str] = (
    "%(levelname)s | %(asctime)s | %(filename)s:%(lineno)d | %(message)s"
)
_DATE_FORMAT: Final[str] = "%d-%m-%Y %H:%M:%S"
_LEVEL_COLORS: Final[dict[str, str]] = {
    "DEBUG": "purple",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}


@dataclass(slots=True, frozen=True, kw_only=True)
class LoggingConfig:
    console_level: int = logging.INFO
    file_level: int = logging.WARNING
    path_log: Path | None = None

    def make_console_handler(self) -> logging.Handler:
        handler = logging.StreamHandler()
        handler.setLevel(self.console_level)
        handler.setFormatter(
            colorlog.ColoredFormatter(
                _STDOUT_FORMAT,
                datefmt=_DATE_FORMAT,
                log_colors=_LEVEL_COLORS,
                secondary_log_colors={},
                reset=True,
                style="%",
            )
        )
        return handler

    def make_file_handler(self, app_name: str) -> logging.Handler:
        if self.path_log is None:
            raise RuntimeError("LoggingConfig: path_log unfilled")

        log_dir: Path = self.path_log
        log_dir.mkdir(parents=True, exist_ok=True)

        file_path: Path = log_dir / f"{app_name}.log"

        handler = RotatingFileHandler(
            file_path,
            mode="a",
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )

        handler.setLevel(self.file_level)
        handler.setFormatter(
            logging.Formatter(_FILE_FORMAT, datefmt=_DATE_FORMAT)
        )

        return handler


def setup_root_logger(config: LoggingConfig, app_name: str) -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(config.console_level)
    logger.handlers.clear()
    logger.addHandler(config.make_console_handler())
    if config.path_log is not None:
        logger.addHandler(config.make_file_handler(app_name))
    logging.captureWarnings(True)

    for name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
        uvi_logger = logging.getLogger(name)
        uvi_logger.handlers.clear()
        uvi_logger.propagate = True

    return logger
