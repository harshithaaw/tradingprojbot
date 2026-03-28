from bot.log_config import get_logger

log = get_logger("test")

log.info("Logger is working fine")
log.warning("This is a warning")
log.error("This is a fake error for testing")
log.debug("This debug line only goes to the file, not terminal")