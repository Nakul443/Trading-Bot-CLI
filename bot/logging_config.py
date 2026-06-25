# system that intercepts every notification
# and splits it into two different formats
# one for terminal (user view) and one for log file (developer view)
# user view: keeps things clean and simple, only shows the log level and message
# developer view: shows the log level, message, module, and timestamp for debugging purposes

import logging
import sys

def setup_logging():
    """
    Configures the root logger to output to both a file and the console
    with different formatting styles.
    """
    # root logger with minimum threshold level
    logger = logging.getLogger()
    logger.setLevel(logging.INFO) # this tells the system what messages to listen to
    # INFO means it will capture warnings and errors

    # avoid adding duplicate handlers if the function is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    # define the Formatter for the log file (includes precise time, module, and log level)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # define the Formatter for the console (cleaner, less cluttered for the user)
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )

    # Create the File Handler (appends all logs to 'bot.log')
    file_handler = logging.FileHandler("bot.log", mode="a")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)

    # Create the Stream Handler (prints logs directly to the standard output terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Attach both handlers back to the root logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger