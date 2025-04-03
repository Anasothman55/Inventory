import logging

LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"

class LogLevels(str):
  info = "INFO"
  warn = "WARNING"
  error = "ERROR"
  debug = "DEBUG"

def configure_logging(log_level: str = LogLevels.error):
  log_level = log_level.upper()
  log_levels = [level.upper() for level in vars(LogLevels).values() if isinstance(level, str)]

  if log_level not in log_levels:
    log_level = LogLevels.error  # Default to ERROR

  numeric_level = getattr(logging, log_level, logging.ERROR)

  logging.basicConfig(level=numeric_level, format=LOG_FORMAT_DEBUG, force=True)

  logger = logging.getLogger("FastAPIApp")  # Named Logger
  logger.setLevel(numeric_level)

  if not logger.hasHandlers():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT_DEBUG))
    logger.addHandler(handler)

  logger.debug("Logging configured successfully!")
  return logger  # Return logger instance

# Initialize and store the logger globally
logger = configure_logging(LogLevels.debug)
