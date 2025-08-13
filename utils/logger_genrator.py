import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(log_file, max_bytes=10*1024*1024, backup_count=3, level=logging.INFO):
	"""
	Returns a logger with RotatingFileHandler and console output.
	"""
	logger = logging.getLogger(log_file)
	logger.setLevel(level)
	logger.propagate = False

	# Remove all handlers if already set (avoid duplicate logs)
	if logger.hasHandlers():
		logger.handlers.clear()

	# Ensure log directory exists
	os.makedirs(os.path.dirname(log_file), exist_ok=True)

	file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8')
	file_handler.setLevel(level)
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)

	console_handler = logging.StreamHandler()
	console_handler.setLevel(level)
	console_handler.setFormatter(formatter)
	logger.addHandler(console_handler)

	return logger
